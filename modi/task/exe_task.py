import time
import json
import queue
import base64
import struct

import urllib.request as ur

from urllib.error import URLError

from enum import IntEnum
from typing import Callable, Dict

from modi.module.input_module.button import Button
from modi.module.input_module.dial import Dial
from modi.module.input_module.env import Env
from modi.module.input_module.gyro import Gyro
from modi.module.input_module.ir import Ir
from modi.module.input_module.mic import Mic
from modi.module.input_module.ultrasonic import Ultrasonic

from modi.module.output_module.display import Display
from modi.module.output_module.led import Led
from modi.module.output_module.motor import Motor
from modi.module.output_module.speaker import Speaker

from modi.module.module import Module
from modi.util.msgutil import unpack_data as up


class ExeTask:
    """
    :param queue send_q: Inter-process queue for writing serial
    message.
    :param queue recv_q: Inter-process queue for parsing json message.
    :param dict() module_ids: dict() of module_id : ['timestamp', 'uuid'].
    :param list() modules: list() of module instance.
    """

    # variables shared across all class instances
    __module_categories = ["network", "input", "output"]
    __module_types = {
        "network": ["usb", "usb/wifi/ble"],
        "input": ["env", "gyro", "mic", "button", "dial", "ultrasonic", "ir"],
        "output": ["display", "motor", "led", "speaker"],
    }

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

        self.__init_modules()
        print('Start initializing connected MODI modules')

    def run(self, delay: float):
        """ Run in ExecutorThread

        :param delay: time value to wait in seconds
        :type delay: float
        """
        time.sleep(delay)

        try:
            raw_message = self._recv_q.get_nowait()
            message = json.loads(raw_message)
        except queue.Empty:
            pass
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
        # print('topology_msg:', message)

        # Setup prerequisites
        src_id = message["s"]
        byte_data = message["b"]
        broadcast_id = 2 ** 16 - 1
        topology_by_id = {}

        message_decoded = bytearray(base64.b64decode(byte_data))
        # print('topology_msg_dec:', message_decoded)

        # UUID
        src_uuid = self.__get_uuid_by_id(src_id)
        topology_by_id['uuid'] = src_uuid

        # RIGHT ID
        right_id = message_decoded[1] << 8 | message_decoded[0]
        topology_by_id['r'] = right_id if right_id != broadcast_id else None

        # TOP ID
        top_id = message_decoded[3] << 8 | message_decoded[2]
        topology_by_id['t'] = top_id if top_id != broadcast_id else None

        # LEFT ID
        left_id = message_decoded[5] << 8 | message_decoded[4]
        topology_by_id['l'] = left_id if left_id != broadcast_id else None

        # BOTTOM ID
        bottom_id = message_decoded[7] << 8 | message_decoded[6]
        topology_by_id['b'] = bottom_id if bottom_id != broadcast_id else None
        # Save topology data for current module
        if not self._topology_data.get(src_id):
            self._topology_data[src_id] = topology_by_id
        else:
            # If the topology data already exists, update it
            for key in self._topology_data[src_id]:
                if not self._topology_data[src_id][key]:
                    self._topology_data[src_id][key] = topology_by_id[key]

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

    def __update_health(self, message: Dict[str, int]) -> None:
        """ Update information by health message

        :param message: Dictionary format message of the module
        :type message: Dictionary
        :return: None
        """
        # Record current time and uuid, timestamp, battery information
        module_id = message["s"]
        curr_time_ms = int(time.time() * 1000)
        message_decoded = bytearray(base64.b64decode(message["b"]))

        self._module_ids[module_id] = self._module_ids.get(module_id, dict())
        self._module_ids[module_id]["timestamp"] = curr_time_ms
        self._module_ids[module_id]["uuid"] = self._module_ids[module_id].get(
            "uuid", str()
        )
        self._module_ids[module_id]["battery"] = int(message_decoded[3])

        # Request uuid from network modules and other modules
        if not self._module_ids[module_id]["uuid"]:
            message_to_write = self.__request_uuid(
                module_id, is_network_module=False)
            self._send_q.put(message_to_write)
            message_to_write = self.__request_uuid(
                module_id, is_network_module=True)
            self._send_q.put(message_to_write)

        # Disconnect modules with no health message for more than 2 seconds
        for module_id, module_info in list(self._module_ids.items()):
            if curr_time_ms - module_info["timestamp"] > 1000:
                for module in self._modules:
                    if module.uuid == module_info["uuid"]:
                        module.set_connection_state(connection_state=False)

    def __update_modules(self, message: Dict[str, str]) -> None:
        """ Update module information

        :param message: Dictionary format module info
        :type message: Dictionary
        :return: None
        """

        # Set time variable for timestamp
        curr_time_ms = int(time.time() * 1000)

        # Record information by module id
        module_id = message["s"]
        self._module_ids[module_id] = self._module_ids.get(module_id, dict())
        self._module_ids[module_id]["timestamp"] = curr_time_ms
        self._module_ids[module_id]["uuid"] = self._module_ids[module_id].get(
            "uuid", str()
        )

        # Extract uuid from message "b"
        message_decoded = bytearray(base64.b64decode(message["b"]))
        module_uuid_bytes = message_decoded[:4]
        module_info_bytes = message_decoded[-4:]

        module_info = (module_info_bytes[1] << 8) + module_info_bytes[0]
        module_version_info = module_info_bytes[3] << 8 | module_info_bytes[2]

        # Retrieve most recent skeleton version from the server
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
            latest_version = module_version_info

        module_category_idx = module_info >> 13
        module_type_idx = (module_info >> 4) & 0x1FF

        module_category = self.__module_categories[module_category_idx]
        module_type = self.__module_types[module_category][module_type_idx]
        module_uuid = self.__fit_module_uuid(
            module_info,
            (
                (module_uuid_bytes[3] << 24)
                + (module_uuid_bytes[2] << 16)
                + (module_uuid_bytes[1] << 8)
                + module_uuid_bytes[0]
            ),
        )

        module_uuid = up(message['b'], (6, 2))[0]

        if module_category != 'network' and \
                not self.firmware_update_message_flag and \
                module_version_info < latest_version:

            print("Your MODI module(s) is not up-to-date.")
            print("You can update your MODI modules by calling "
                  "'update_module_firmware()'")
            self.firmware_update_message_flag = True

        self._module_ids[module_id]["uuid"] = module_uuid

        # Handle re-connected modules
        for module in self._modules:
            if module.uuid == module_uuid and not module.is_connected:
                module.set_connection_state(connection_state=True)
                # When reconnected, turn-off module pnp state
                pnp_off_message = self.__set_module_state(
                    0xFFF, Module.State.RUN, Module.State.PNP_OFF
                )
                self._send_q.put(pnp_off_message)

        # Handle newly-connected modules
        if not next(
            (module for module in self._modules if module.uuid == module_uuid),
            None
        ):
            if module_category != "network":
                module_template = self.__init_module(module_type)
                module_instance = module_template(
                    module_id, module_uuid, self._send_q
                )
                self.__set_pnp(
                    module_id=module_instance.id,
                    module_pnp_state=Module.State.PNP_OFF
                )

                self._modules.append(module_instance)
                print(f"{type(module_instance).__name__} ({module_id}) "
                      f"has been connected!")

                if self.__is_all_connected():
                    self._init_event.set()

    def __is_all_connected(self) -> bool:
        """ Determine whether all modules are connected

        :return: true is all modules are connected
        :rtype: bool
        """

        return self._nb_modules == len(self._modules)

    def __init_module(self, module_type: str) -> Module:
        """ Find module type for module initialize

        :param module_type: Type of the module in string
        :type module_type: str
        :return: Module corresponding to the type
        :rtype: Module
        """

        module = {
            "button": Button,
            "dial": Dial,
            "display": Display,
            "env": Env,
            "gyro": Gyro,
            "ir": Ir,
            "led": Led,
            "mic": Mic,
            "motor": Motor,
            "speaker": Speaker,
            "ultrasonic": Ultrasonic,
        }.get(module_type)
        return module

    def __update_property(self, message: Dict[str, int]) -> None:
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
                message_decoded = bytearray(base64.b64decode(message["b"]))
                property_type = module.PropertyType(property_number)
                module.update_property(
                    property_type,
                    round(struct.unpack("f", bytes(
                        message_decoded[:4]))[0], 2),
                )

    def __set_pnp(self, module_id: int, module_pnp_state: IntEnum) -> None:
        """ Generate module pnp on/off command

        :param module_id: ID of the target module
        :type module_id: int
        :param module_pnp_state: Pnp state value
        :type module_pnp_state: IntEnum
        :return: None
        """

        # If no module_id is specified, it will broadcast incoming pnp state
        if module_id is None:
            for curr_module_id in self._module_ids:
                pnp_message = self.__set_module_state(
                    curr_module_id, Module.State.RUN, module_pnp_state
                )
                self._send_q.put(pnp_message)

        # Otherwise, it sets pnp state of the given module
        else:
            pnp_message = self.__set_module_state(
                module_id, Module.State.RUN, module_pnp_state
            )
            self._send_q.put(pnp_message)

    def __fit_module_uuid(self, module_info: int, module_uuid: int) -> int:
        """ Generate uuid using bitwise operation

        :param module_info: Module info
        :type module_info: int
        :param module_uuid: Module uuid
        :type module_uuid: int
        :return: Fitted uuid
        :rtype: int
        """

        sizeof_module_uuid = 0
        while (module_uuid >> sizeof_module_uuid) > 0:
            sizeof_module_uuid += 1
        sizeof_module_uuid += sizeof_module_uuid % 4
        return (module_info << sizeof_module_uuid) | module_uuid

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

        message = dict()

        message["c"] = 0x09
        message["s"] = 0
        message["d"] = destination_id

        state_bytes = bytearray(2)
        state_bytes[0] = module_state
        state_bytes[1] = pnp_state

        message["b"] = base64.b64encode(bytes(state_bytes)).decode("utf-8")
        message["l"] = 2

        return json.dumps(message, separators=(",", ":"))

    def __init_modules(self) -> None:
        """ Initialize module on first run

        :return: None
        """

        BROADCAST_ID = 0xFFF

        # Reboot module
        reboot_message = self.__set_module_state(
            BROADCAST_ID, Module.State.REBOOT, Module.State.PNP_OFF
        )
        self._send_q.put(reboot_message)
        # self.__delay()

        # Command module pnp off
        pnp_off_message = self.__set_module_state(
            BROADCAST_ID, Module.State.RUN, Module.State.PNP_OFF
        )
        self._send_q.put(pnp_off_message)
        # self.__delay()

        # Command module uuid
        request_uuid_message = self.__request_uuid(BROADCAST_ID)
        self._send_q.put(request_uuid_message)
        # self.__delay()

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

        BROADCAST_ID = 0xFFF

        message = dict()
        message["c"] = 0x28 if is_network_module else 0x08
        message["s"] = source_id
        message["d"] = BROADCAST_ID

        id_bytes = bytearray(8)
        id_bytes[0] = 0xFF
        id_bytes[1] = 0x0F

        message["b"] = base64.b64encode(bytes(id_bytes)).decode("utf-8")
        message["l"] = 8

        return json.dumps(message, separators=(",", ":"))

    def request_topology(self, cmd: int = 0x07,
                         module_id: int = 0xFFF) -> None:
        """Request module topology

        :return: json serialized topology request message
        :rtype: str
        """
        message = dict()
        message["c"] = cmd
        message["s"] = 0
        message["d"] = module_id

        direction_data = bytearray(8)
        message["b"] = base64.b64encode(bytes(direction_data)).decode("utf-8")
        message["l"] = 8

        self._send_q.put(json.dumps(message, separators=(",", ":")))

    def update_firmware(self) -> None:
        """ Remove firmware of MODI modules

        :return: None
        """

        BROADCAST_ID = 0xFFF
        firmware_update_message = self.__set_module_state(
            BROADCAST_ID, Module.State.UPDATE_FIRMWARE, Module.State.PNP_OFF
        )
        self._send_q.put(firmware_update_message)
        self.__delay()

    def update_firmware_ready(self, module_id: int) -> None:
        """ Check if modules with no firmware are ready to update its firmware

        :param module_id: Id of the target module
        :type module_id: int
        :return: None
        """

        firmware_update_ready_message = self.__set_module_state(
            module_id, Module.State.UPDATE_FIRMWARE_READY, Module.State.PNP_OFF
        )
        self._send_q.put(firmware_update_ready_message)
        self.__delay()

    def __get_type_from_uuid(self, uuid):
        if uuid is None:
            return 'Network'

        hexadecimal = hex(uuid).lstrip("0x")
        type_indicator = str(hexadecimal)[:4]
        module_type = {
            # Input modules
            '2000': 'env',
            '2010': 'gyro',
            '2020': 'mic',
            '2030': 'button',
            '2040': 'dial',
            '2050': 'ultrasonic',
            '2060': 'ir',

            # Output modules
            '4000': 'display',
            '4010': 'motor',
            '4020': 'led',
            '4030': 'speaker',
        }.get(type_indicator)
        return 'Network' if module_type is None else module_type
