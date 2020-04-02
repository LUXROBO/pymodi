import os
import time
import json
import queue
import base64
import struct
import threading

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


class ExecutorTask:
    """
    :param queue serial_write_q: Inter-process queue for writing serial
    message.
    :param queue json_recv_q: Inter-process queue for parsing json message.
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

        self.firmware_update_flag = False
        self.erase_error_flag = False
        self.erase_flag = False
        self.erase_count = 0
        self.crc_error_flag = False
        self.crc_flag = False
        self.crc_count = 0
        self.end_flash_success = False

        self.__init_modules()
        print('Start initializing connected MODI modules')

    def run(self, delay):
        """ Run in ExecutorThread
        """

        try:
            message = json.loads(self._recv_q.get_nowait())
        except queue.Empty:
            pass
        else:
            self.__command_handler(message["c"])(message)

        time.sleep(delay)

    def __command_handler(self, command):
        """ Excute task based on command message
        """

        return {
            0x00: self.__update_health,
            0x0A: self.__update_warning,
            0x0C: self.__update_firmware_state,
            0x05: self.__update_modules,
            0x07: self.__update_topology,
            0x1F: self.__update_property,
        }.get(command, lambda _: None)

    def __update_topology(self, message):
        # print('topology_msg:', message)

        # Setup prerequisites
        src_id = message["s"]
        byte_data = message["b"]
        broadcast_id = 2**16-1
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
        self._topology_data[src_id] = topology_by_id

    def __get_uuid_by_id(self, id_):

        # find id of a module which has corresponding uuid
        for module in self._modules:
            if module.id == id_:
                return module.uuid
        return None

    def __update_health(self, message):
        """ Update information by health message
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

    def __update_warning(self, message):
        #print('Warning message:', message)

        sid = message["s"]

        WARNING_TYPE_INDEX = 6
        warning_type = bytearray(base64.b64decode(message["b"]))[
            WARNING_TYPE_INDEX
        ]
        if not warning_type:
            None

        if warning_type == 1:
            self.update_firmware_ready(module_id=sid)
        elif warning_type == 2:
            if not self.firmware_update_flag:
                self.t = threading.Thread(
                    target=self.update_firmware_for_real, args=(sid,)
                )
                self.t.start()
                self.firmware_update_flag = True
        else:
            print("Unsupported warning type:", warning_type)

    def __update_modules(self, message):
        """ Update module information
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

                if self.__is_all_connected():
                    self._init_event.set()

    def __is_all_connected(self):
        """ determine whether all modules are connected
        """

        return self._nb_modules == len(self._modules)

    def __init_module(self, module_type):
        """ Find module type for module initialize
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

    def __update_property(self, message):
        """ Update module property
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

    def __set_pnp(self, module_id, module_pnp_state):
        """ Generate module pnp on/off command
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

    def __fit_module_uuid(self, module_info, module_uuid):
        """ Generate uuid using bitwise operation
        """

        sizeof_module_uuid = 0
        while (module_uuid >> sizeof_module_uuid) > 0:
            sizeof_module_uuid += 1
        sizeof_module_uuid += sizeof_module_uuid % 4
        return (module_info << sizeof_module_uuid) | module_uuid

    def __set_module_state(self, destination_id, module_state, pnp_state):
        """ Generate message for set module state and pnp state
        """

        if type(module_state) is Module.State:
            message = dict()

            message["c"] = 0x09
            message["s"] = 0
            message["d"] = destination_id

            state_bytes = bytearray(2)
            state_bytes[0] = module_state.value
            state_bytes[1] = pnp_state.value

            message["b"] = base64.b64encode(bytes(state_bytes)).decode("utf-8")
            message["l"] = 2

            return json.dumps(message, separators=(",", ":"))
        else:
            raise RuntimeError("The type of state is not ModuleState")

    def __init_modules(self):
        """ Initialize module on first run
        """

        BROADCAST_ID = 0xFFF

        # Reboot module
        reboot_message = self.__set_module_state(
            BROADCAST_ID, Module.State.REBOOT, Module.State.PNP_OFF
        )
        self._send_q.put(reboot_message)
        self.__delay()

        # Command module pnp off
        pnp_off_message = self.__set_module_state(
            BROADCAST_ID, Module.State.RUN, Module.State.PNP_OFF
        )
        self._send_q.put(pnp_off_message)
        self.__delay()

        # Command module uuid
        request_uuid_message = self.__request_uuid(BROADCAST_ID)
        self._send_q.put(request_uuid_message)
        self.__delay()

        # Request topology data
        request_topology_message = self.__request_topology()
        self._send_q.put(request_topology_message)
        self.__delay()

    def __delay(self):
        """ Wait for delay
        """

        time.sleep(1)

    def __request_uuid(self, source_id, is_network_module=False):
        """ Generate broadcasting message for request uuid
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

    def __request_topology(self):

        message = dict()
        message["c"] = 0x07
        message["s"] = 0
        message["d"] = 0xFFF

        direction_data = bytearray(8)
        message["b"] = base64.b64encode(bytes(direction_data)).decode("utf-8")
        message["l"] = 8

        return json.dumps(message, separators=(",", ":"))

    def update_firmware(self):
        """ Remove firmware of MODI modules (Removes EndFlash)
        """

        BROADCAST_ID = 0xFFF
        firmware_update_message = self.__set_module_state(
            BROADCAST_ID, Module.State.UPDATE_FIRMWARE, Module.State.PNP_OFF
        )
        self._send_q.put(firmware_update_message)
        self.__delay()

    def update_firmware_ready(self, module_id):
        """ Check if modules with no firmware are ready to update its firmware
        """

        firmware_update_ready_message = self.__set_module_state(
            module_id, Module.State.UPDATE_FIRMWARE_READY, Module.State.PNP_OFF
        )
        self._send_q.put(firmware_update_ready_message)
        self.__delay()

    def update_firmware_for_real(self, module_id):
        module_type = "ir"

        # Init path to binary file
        root_path = "/Users/jha/Downloads"
        bin_path = os.path.join(root_path,
                                "skeleton", module_type, "Base_module.bin")

        # Read bytes data from the given binary file of the current module
        bin_buffer = None
        with open(bin_path, "rb") as bf:
            bin_buffer = bf.read()

        # Init metadata of the bytes loaded
        page_size = 0x800
        flash_memory_addr = 0x08000000

        bin_size = os.stat(bin_path).st_size
        bin_begin = 0x9000
        bin_end = bin_size - ((bin_size - bin_begin) % page_size)

        response_delay = 0.1
        response_timeout = 10
        for page_begin in range(bin_begin, bin_end+1, page_size):
            page_end = page_begin + page_size
            curr_page = bin_buffer[page_begin:page_end]

            # Skip current page if empty
            if not sum(curr_page):
                continue

            # Erase page (send erase request and receive erase response)
            erase_response_wait_time = 0
            erase_message = self.get_firmware_command(
                module_id, 1, 2, 0, flash_memory_addr+page_begin
            )
            self._send_q.put(erase_message)
            while not self.erase_flag:
                if self.erase_error_flag:
                    self.erase_count += 1
                    if self.erase_count > 5:
                        raise Exception("Erase Errored")
                    break
                if erase_response_wait_time > response_timeout:
                    raise Exception("Erase timed-out")
                time.sleep(response_delay)
                erase_response_wait_time += response_delay
            else:
                self.erase_flag = False
            if self.erase_error_flag:
                page_begin -= page_size
                self.erase_error_flag = False
                continue

            # Copy current page data to the module
            checksum = 0
            for curr_ptr in range(0, page_size, 8):
                if page_begin + curr_ptr >= bin_size:
                    break

                curr_data = curr_page[curr_ptr:curr_ptr+8]
                data_message = self.get_firmware_data(
                    module_id, seq_num=curr_ptr//8, bin_data=curr_data
                )
                self._send_q.put(data_message)

                # Calculate CRC64 using CRC32 twice
                checksum = self.crc32(curr_data[:4], checksum)
                checksum = self.crc32(curr_data[4:], checksum)

            # CRC on current page (send CRC request and receive CRC response)
            crc_response_wait_time = 0
            crc_message = self.get_firmware_command(
                module_id, 1, 1, checksum, flash_memory_addr + page_begin
            )
            self._send_q.put(crc_message)
            while not self.crc_flag:
                if self.crc_error_flag:
                    self.crc_count += 1
                    if self.crc_count > 5:
                        raise Exception("CRC Errored")
                    break
                if crc_response_wait_time > response_timeout:
                    raise Exception("CRC timed-out")
                time.sleep(response_delay)
                crc_response_wait_time += response_delay
            else:
                self.crc_flag = False
            if self.crc_error_flag:
                page_begin -= page_size
                self.crc_error_flag = False
                continue
        
        # Write end-flash data until success
        while not self.end_flash_success:
            end_flash_data = bytearray(8)
            end_flash_data[0] = 0xAA

            # Erase page (send erase request and receive erase response)
            erase_response_wait_time = 0
            erase_message = self.get_firmware_command(
                module_id, 1, 2, 0, 0x0801F800
            )
            self._send_q.put(erase_message)
            while not self.erase_flag:
                if self.erase_error_flag:
                    self.erase_count += 1
                    if self.erase_count > 5:
                        raise Exception("Erase Errored")
                    break
                if erase_response_wait_time > response_timeout:
                    raise Exception("Erase timed-out")
                time.sleep(response_delay)
                erase_response_wait_time += response_delay
            else:
                self.erase_flag = False
            if self.erase_error_flag:
                page_begin -= page_size
                self.erase_error_flag = False
                continue

            data_message = self.get_firmware_data(
                module_id, seq_num=0, bin_data=end_flash_data
            )

            checksum = 0
            checksum = self.crc32(curr_data[:4], checksum)
            checksum = self.crc32(curr_data[4:], checksum)

            # CRC on current page (send CRC request and receive CRC response)
            crc_response_wait_time = 0
            crc_message = self.get_firmware_command(
                module_id, 1, 1, checksum, 0x0801F800
            )
            self._send_q.put(crc_message)
            while not self.crc_flag:
                if self.crc_error_flag:
                    self.crc_count += 1
                    if self.crc_count > 5:
                        raise Exception("CRC Errored")
                    break
                if crc_response_wait_time > response_timeout:
                    raise Exception("CRC timed-out")
                time.sleep(response_delay)
                crc_response_wait_time += response_delay
            else:
                self.crc_flag = False
            if self.crc_error_flag:
                page_begin -= page_size
                self.crc_error_flag = False
                continue

            self.end_flash_success = True

        # Reboot
        reboot_message = self.__set_module_state(
            module_id, Module.State.REBOOT, Module.State.PNP_OFF
        )
        self._send_q.put(reboot_message)
        self.__delay()

        # Firmware update flag down
        print('Firmware update is done for current module', module_id)
        self.firmware_update_flag = False

    def get_firmware_command(self, module_id, rot_stype, rot_scmd,
                             crc32, page_addr):
        """ Create a new firmware command in json format
            ROT_StateType, ROT_StreamCommand
        """

        message = dict()
        message["c"] = 0x0D

        """ SID is 12-bits length in MODI CAN.
            To fully utilize its capacity, we split 12-bits into 4 and 8 bits.
            First 4 bits include rot_scmd information.
            And the remaining bits represent rot_stype.
        """
        message["s"] = (rot_scmd << 8) | rot_stype
        message["d"] = module_id

        """ The firmware command data to be sent is 8-bytes length.
            Where the first 4 bytes consist of CRC-32 information.
            Last 4 bytes represent page address information.
        """
        crc32_and_page_addr_data = bytearray(8)
        for i in range(4):
            crc32_and_page_addr_data[i] = crc32 & 0xFF
            crc32 >>= 8
            crc32_and_page_addr_data[4 + i] = page_addr & 0xFF
            page_addr >>= 8
        message["b"] = base64.b64encode(
            bytes(crc32_and_page_addr_data)
        ).decode("utf-8")
        message["l"] = 8

        return json.dumps(message, separators=(",", ":"))

    def get_firmware_data(self, module_id, seq_num, bin_data):
        """ A data to be sent when updating firmware of a module
        """

        message = dict()
        message["c"] = 0x0B
        message["s"] = seq_num
        message["d"] = module_id

        message["b"] = base64.b64encode(bytes(bin_data)).decode("utf-8")
        message["l"] = 8

        return json.dumps(message, separators=(",", ":"))

    def __update_firmware_state(self, message):
        module_id = message["s"]
        byte_data = message["b"]
        message_decoded = bytearray(base64.b64decode(byte_data))

        stream_state = message_decoded[4]
        firmware_state = self.get_firmware_state(stream_state)
        if firmware_state == "CRC Error":
            self.crc_error_flag = True
        elif firmware_state == "CRC Complete":
            self.crc_flag = True
        elif firmware_state == "Erase Error":
            self.erase_error_flag = True
        elif firmware_state == "Erase Complete":
            self.erase_flag = True
    
    def get_firmware_state(self, stream_state):
        return {
            0 : "No Error",
            1 : "Update Ready",
            2 : "Write Fail",
            3 : "Verify Fail",
            4 : "CRC Error",
            5 : "CRC Complete",
            6 : "Erase Error",
            7 : "Erase Complete",
        }.get(stream_state)

    def crc32(self, data, crc):
        crc ^= int.from_bytes(data, byteorder='little', signed=False)

        for _ in range(32):
            if ((crc & (1 << 31)) != 0):
                crc = (crc << 1) ^ 0x4C11DB7
            else:
                crc <<= 1
            crc &= 0xFFFFFFFF

        return crc
