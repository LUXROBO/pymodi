import time
import json
import urllib.request as ur

from urllib.error import URLError
from base64 import b64decode
from enum import IntEnum
from typing import Callable, Dict
from queue import Empty
from modi.module.module import Module
from modi.util.msgutil import unpack_data, decode_data, parse_message
from modi.util.misc import get_module_from_name, get_type_from_uuid


class ExeTask:
    """
    :param queue send_q: Inter-process queue for writing serial
    message.
    :param queue recv_q: Inter-process queue for parsing json message.
    :param dict() module_ids: dict() of module_id : ['timestamp', 'uuid'].
    :param list() modules: list() of module instance.
    """
    def __init__(self, modules, module_ids, topology_data,
                 recv_q, send_q, init_event, nb_modules):

        self._modules = modules
        self._module_ids = module_ids
        self._topology_data = topology_data
        self._recv_q = recv_q
        self._send_q = send_q
        self._init_event = init_event
        self._nb_modules = nb_modules

        # Check if a user has been notified when firmware is outdated
        self.firmware_update_message_flag = False
        self.__user_code_checked = False
        self.__init_modules()
        print('Start initializing connected MODI modules')

    def run(self, delay: float):
        """ Run in ExecutorThread

        :param delay: time value to wait in seconds
        :type delay: float
        """
        try:
            raw_message = self._recv_q.get_nowait()
            message = json.loads(raw_message)
        except Empty:
            time.sleep(delay)
        except json.decoder.JSONDecodeError:
            print('current json message:', raw_message)
        else:
            self.__command_handler(message["c"])(message)

    def __command_handler(self,
                          command: int) -> Callable[[Dict[str, int]], None]:
        """ Execute task based on command message

        :param command: command code
        :type command: int
        :return: a function the corresponds to the command code
        :rtype: Callable[[Dict[str, int]], None]
        """

        return {
            0x00: self.__update_health,
            0x05: self.__update_modules,
            0x07: self.__update_topology,
            0x1F: self.__update_property,
        }.get(command, lambda _: None)

    def __update_topology(self, message: Dict[str, int]) -> None:
        """Update the topology of the connected modules

        :param message: Dictionary format message of the module
        :return: None
        """
        # Setup prerequisites
        src_id = message["s"]
        byte_data = message["b"]
        broadcast_id = 0xFFFF
        topology_by_id = {}
        topology_ids = unpack_data(byte_data, (2, 2, 2, 2))

        # UUID
        src_uuid = self.__get_uuid_by_id(src_id)
        topology_by_id['uuid'] = src_uuid
        for idx, direction in enumerate(('r', 't', 'l', 'b')):
            topology_by_id[direction] = topology_ids[idx] \
                if topology_ids[idx] != broadcast_id else None

        # Update topology data for the module
        self._topology_data[src_id] = topology_by_id

    def __get_uuid_by_id(self, id_: int) -> int:
        """Find id of a module which has corresponding uuid

        :param id_: ID of the module
        :type id_: int
        :return: UUID
        :rtype: int
        """
        for module in self._modules:
            if module.id == id_:
                return module.uuid
        return None

    def __update_health(self, message: Dict[str, str]) -> None:
        """ Update information by health message

        :param message: Dictionary format message of the module
        :type message: Dictionary
        :return: None
        """
        # Record current time and uuid, timestamp, battery information
        module_id = message["s"]
        curr_time_ms = int(time.time() * 1000)
        message_decoded = bytearray(b64decode(message["b"]))

        self.__record_module_info(module_id, curr_time_ms)
        self._module_ids[module_id]["battery"] = int(message_decoded[3])

        # Check if user code is in the module
        if not self.__user_code_checked:
            user_code_state = unpack_data(message['b'])[4]

            if user_code_state % 2 == 1:
                print("Your MODI module(s) has user code in it.")
                print("You can reset your MODI modules by calling "
                      "'update_module_firmware()'")
                self.__user_code_checked = True

        # Request uuid from network modules and other modules
        if module_id and not self._module_ids[module_id]["uuid"]:
            message_to_write = self.__request_uuid(
                module_id, is_network_module=False)
            self._send_q.put(message_to_write)
            message_to_write = self.__request_uuid(
                module_id, is_network_module=True)
            self._send_q.put(message_to_write)

        # Disconnect modules with no health message for more than 1 second
        for module_id, module_info in list(self._module_ids.items()):
            if curr_time_ms - module_info["timestamp"] > 1000:
                for module in self._modules:
                    if module.uuid == module_info["uuid"]:
                        module.set_connection_state(connection_state=False)

    def __record_module_info(self, module_id, curr_time):
        self._module_ids[module_id] = self._module_ids.get(module_id, dict())
        self._module_ids[module_id]["timestamp"] = curr_time
        self._module_ids[module_id]["uuid"] = self._module_ids[module_id].get(
            "uuid", str()
        )

    @staticmethod
    def __get_latest_version():
        version_path = (
            "https://download.luxrobo.com/modi-skeleton-mobile/version.txt"
        )
        version_info = None
        try:
            for line in ur.urlopen(version_path, timeout=1):
                version_info = line.decode('utf-8').lstrip('v')
            version_digits = [int(digit) for digit in version_info.split('.')]
            """ Version number is formed by concatenating all three version bits
                e.g. v2.2.4 -> 010 00010 00000100 -> 0100 0010 0000 0100
            """
            latest_version = (
                version_digits[0] << 13
                | version_digits[1] << 8
                | version_digits[2]
            )
        except URLError:
            latest_version = None
        return latest_version

    def __update_modules(self, message: Dict[str, str]) -> None:
        """ Update module information

        :param message: Dictionary format module info
        :type message: Dictionary
        :return: None
        """
        module_id = message['s']
        curr_time_ms = int(time.time() * 1000)
        self.__record_module_info(module_id, curr_time_ms)

        module_uuid, module_version_info = \
            unpack_data(message['b'], (6, 2))

        # Retrieve most recent skeleton version from the server
        latest_version = self.__get_latest_version()
        if not latest_version:
            latest_version = module_version_info

        module_type = get_type_from_uuid(module_uuid)
        self._module_ids[module_id]["uuid"] = module_uuid

        # Handle re-connected modules
        for module in self._modules:
            if module.uuid == module_uuid and not module.is_connected:
                module.set_connection_state(connection_state=True)
                # When reconnected, turn-off module pnp state
                self.__set_module_state(
                    0xFFF, Module.State.RUN, Module.State.PNP_OFF
                )

        # Handle newly-connected modules
        if module_uuid not in (module.uuid for module in self._modules):
            new_module = self.__add_new_module(
                module_type, module_id, module_uuid, module_version_info
            )
            if new_module and module_version_info < latest_version:
                print("Your MODI module(s) is not up-to-date.")
                print("You can update your MODI modules by calling "
                      "'update_module_firmware()'")
                new_module.is_up_to_date = False

            if self.__is_all_connected():
                self._init_event.set()

    def __add_new_module(self, module_type, module_id,
                         module_uuid, module_version_info):
        if module_type != 'Network':
            module_template = get_module_from_name(module_type)
            module_instance = module_template(
                module_id, module_uuid, self._send_q
            )
            self.__set_module_state(module_instance.id, Module.State.RUN,
                                    Module.State.PNP_OFF)
            module_instance.version = module_version_info
            self._modules.append(module_instance)
            print(f"{type(module_instance).__name__} ({module_id}) "
                  f"has been connected!")
            return module_instance

    def __is_all_connected(self) -> bool:
        """ Determine whether all modules are connected

        :return: true is all modules are connected
        :rtype: bool
        """
        return self._nb_modules == len(self._modules)

    def __update_property(self, message: Dict[str, str]) -> None:
        """ Update module property

        :param message: Dictionary format message
        :type message: Dictionary
        :return: None
        """
        # Do not update reserved property
        property_number = message["d"]
        if property_number == 0 or property_number == 1:
            return

        # Decode message of module id and module property for update property
        for module in self._modules:
            if module.id == message["s"]:
                property_type = module.PropertyType(property_number)
                module.update_property(
                    property_type,
                    decode_data(message['b']),
                )

    def __set_module_state(self, destination_id: int, module_state: IntEnum,
                           pnp_state: IntEnum) -> str:
        """ Generate message for set module state and pnp state

        :param destination_id: Id to target destination
        :type destination_id: int
        :param module_state: State value of the module
        :type module_state: int
        :param pnp_state: Pnp state value
        :type pnp_state: IntEnum
        :return: json serialized message
        :rtype: str
        """
        self._send_q.put(parse_message(0x09, 0, destination_id,
                                       (module_state, pnp_state)))

    def __init_modules(self) -> None:
        """ Initialize module on first run

        :return: None
        """

        BROADCAST_ID = 0xFFF

        # Reboot module
        self.__set_module_state(
            BROADCAST_ID, Module.State.REBOOT, Module.State.PNP_OFF
        )

        # Command module pnp off
        self.__set_module_state(
            BROADCAST_ID, Module.State.RUN, Module.State.PNP_OFF
        )

        # Command module uuid
        request_uuid_message = self.__request_uuid(BROADCAST_ID)
        self._send_q.put(request_uuid_message)

        # Request topology data
        self.request_topology()
        self.request_topology(0x2A)

    def __delay(self) -> None:
        """ Wait for delay

        :return: None
        """
        time.sleep(0.5)

    def __request_uuid(self, source_id: int,
                       is_network_module: bool = False) -> str:
        """ Generate broadcasting message for request uuid

        :param source_id: Id of the source
        :type source_id: int
        :param is_network_module: true if network module
        :type is_network_module: bool
        :return: json serialized message
        :rtype: str
        """
        return parse_message(0x28 if is_network_module else 0x08,
                             source_id, 0xFFF, (0xFF, 0x0F, 0, 0, 0, 0, 0, 0))

    def request_topology(self, cmd: int = 0x07,
                         module_id: int = 0xFFF) -> None:
        """Request module topology

        :return: json serialized topology request message
        :rtype: str
        """
        self._send_q.put(
            parse_message(cmd, 0, module_id, (0, 0, 0, 0, 0, 0, 0, 0)))
