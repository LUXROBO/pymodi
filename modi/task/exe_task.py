import json
import time

from modi.module.module import Module, BROADCAST_ID
from modi.module.setup_module.battery import Battery
from modi.util.misc import get_module_from_name, get_module_type_from_uuid
from modi.util.msgutil import unpack_data, decode_data, parse_message


class ExeTask:

    def __init__(self, modules, topology_data, conn_task):
        self._modules = modules
        self._topology_data = topology_data
        self._conn = conn_task

        # Reboot all modules
        self.__set_module_state(
            BROADCAST_ID, Module.REBOOT, Module.PNP_OFF
        )

        # Request data required to initialize MODI
        self.__request_network_uuid()
        self.__request_topology()

    def run(self, delay):
        json_pkt = self._conn.recv()
        if not json_pkt:
            time.sleep(delay)
        else:
            try:
                json_msg = json.loads(json_pkt)
                self.__command_handler(json_msg['c'])(json_msg)
            except json.decoder.JSONDecodeError:
                print('current json message:', json_pkt)

    def __command_handler(self, command):
        return {
            0x00: self.__update_health,
            0x05: self.__update_modules,
            0x07: self.__update_topology,
            0x1F: self.__update_property,
        }.get(command, lambda _: None)

    def __update_topology(self, message):
        # Setup prerequisites
        src_id = message["s"]
        byte_data = message["b"]
        topology_by_id = {}
        topology_ids = unpack_data(byte_data, (2, 2, 2, 2))

        module = self.__get_module_by_id(src_id)
        if module:
            topology_by_id['type'] = get_module_type_from_uuid(module.uuid)
        else:
            topology_by_id['type'] = None

        for idx, direction in enumerate(('r', 't', 'l', 'b')):
            topology_by_id[direction] = topology_ids[idx] \
                if topology_ids[idx] != 0xFFFF else None
            # Handle battery module
            if topology_ids[idx] == 0:
                if 0 not in self._topology_data:
                    self._modules.append(Battery(0, -1, None))
                    battery_topology = {
                        'type': 'Battery',
                        'r': None, 't': None, 'l': None, 'b': src_id
                    }
                    self._topology_data[0] = battery_topology
                elif src_id not in self._topology_data[0].values():
                    self._topology_data[0]['l'] = src_id

        # Update topology data for the module
        self._topology_data[src_id] = topology_by_id

    def __get_module_by_id(self, module_id):
        for module in self._modules:
            if module.id == module_id:
                return module

    def __update_health(self, message):
        # Record battery information and user code state
        module_id = message["s"]
        _, _, _, battery_state, user_code_state \
            = unpack_data(message['b'], (1, 1, 1, 1, 1))
        curr_time = time.time()

        # Checking starts only when module is registered
        if module_id in (module.id for module in self._modules):
            module = self.__get_module_by_id(module_id)
            module.last_updated = curr_time
            module.is_connected = True
            # Reset disconnection alert status
            if module.has_printed:
                module.has_printed = False

        # Disconnect module with no health message for more than 2 second
        for module in self._modules:
            if module.module_type != 'network' and \
                    curr_time - module.last_updated > 2:
                if not module.has_printed:
                    print(
                        f"{module.module_type} ({module_id}) "
                        f"has been disconnected!!"
                    )
                    module.has_printed = True
                module.is_connected = False
                module._last_set_message = None

    def __update_modules(self, message):
        module_id = message['s']
        module_uuid, module_version_info = unpack_data(message['b'], (6, 2))

        # Handle new modules
        if module_id not in (module.id for module in self._modules):
            module_type = get_module_type_from_uuid(module_uuid)
            self.__request_topology(module_id)
            new_module = self.__add_new_module(
                module_type, module_id, module_uuid, module_version_info
            )
            new_module.module_type = module_type
        elif not self.__get_module_by_id(module_id).is_connected:
            # Handle Reconnected modules
            self.__get_module_by_id(module_id).is_connected = True
            module_type = get_module_type_from_uuid(module_uuid)
            print(f"{module_type} ({module_id}) has been reconnected!!")

    def __add_new_module(self, module_type, module_id, module_uuid, _):
        module_template = get_module_from_name(module_type)
        module_instance = module_template(
            module_id, module_uuid, self._conn
        )
        self.__set_module_state(module_instance.id, Module.RUN, Module.PNP_OFF)
        self._modules.append(module_instance)
        print(f"{str(module_instance)} has been connected!")
        return module_instance

    def __update_property(self, message):
        # Do not update reserved property
        property_number = message["d"]
        if property_number == 0 or property_number == 1:
            return
        module = self.__get_module_by_id(message['s'])
        if not module:
            return
        data = message['b']
        if module.module_type == 'network':
            module.update_property(property_number, unpack_data(data)[0])
        else:
            module.update_property(property_number, decode_data(data))

    def __set_module_state(self, destination_id, module_state, pnp_state):
        self._conn.send_nowait(
            parse_message(0x09, 0, destination_id, (module_state, pnp_state))
        )

    def __request_network_uuid(self):
        self._conn.send_nowait(
            parse_message(0x28, BROADCAST_ID, BROADCAST_ID, (0xFF, 0x0F))
        )

    def __request_topology(self, module_id=BROADCAST_ID):
        self._conn.send_nowait(
            parse_message(0x07, 0, module_id, (0, 0, 0, 0, 0, 0, 0, 0))
        )
        self._conn.send_nowait(
            parse_message(0x2A, 0, module_id, (0, 0, 0, 0, 0, 0, 0, 0))
        )
