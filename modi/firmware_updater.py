import json
import sys
import threading as th
import time
from base64 import b64encode, b64decode
from io import open
from os import path
from importlib import import_module as im

import serial

from modi.module.module import Module
from modi.util.msgutil import unpack_data, decode_message
from modi.util.conn_util import list_modi_ports, is_on_pi


class STM32FirmwareUpdater:
    """STM32 Firmware Updater: Updates a firmware of given module"""

    NO_ERROR = 0
    UPDATE_READY = 1
    WRITE_FAIL = 2
    VERIFY_FAIL = 3
    CRC_ERROR = 4
    CRC_COMPLETE = 5
    ERASE_ERROR = 6
    ERASE_COMPLETE = 7

    def __init__(self, is_os_update=True, target_ids=(0xFFF, )):
        self.__conn = self.__open_conn()
        self.__conn.open_conn()
        th.Thread(target=self.__read_conn, daemon=True).start()
        self.__target_ids = target_ids
        self.response_flag = False
        self.response_error_flag = False
        self.response_error_count = 0
        self.__running = True
        self.__is_os_update = is_os_update
        self.update_event = th.Event()
        self.update_in_progress = False
        self.modules_to_update = []
        self.modules_updated = []

    def update_module_firmware(self):
        self.reset_state()
        for target in self.__target_ids:
            self.request_to_update_firmware(target)
        self.update_event.wait()
        print("Module firmwares have been updated!")

    def close(self):
        self.__running = False
        time.sleep(0.5)
        self.__conn.close_conn()

    @staticmethod
    def __open_conn():
        if is_on_pi():
            return im('modi.task.can_task').CanTask()
        else:
            return im('modi.task.ser_task').SerTask()

    @staticmethod
    def __get_module_type_from_uuid(uuid: int) -> str:
        """Returns the name of the module based on uuid

        :param uuid: uuid of the module
        :type uuid: int
        :return: Module name
        :rtype: str
        """
        hexadecimal = hex(uuid).lstrip("0x")
        type_indicator = str(hexadecimal)[:4]
        module_type = {
            # Input modules
            '2000': 'Env',
            '2010': 'Gyro',
            '2020': 'Mic',
            '2030': 'Button',
            '2040': 'Dial',
            '2050': 'Ultrasonic',
            '2060': 'Ir',

            # Output modules
            '4000': 'Display',
            '4010': 'Motor',
            '4020': 'Led',
            '4030': 'Speaker',
        }.get(type_indicator)
        return 'network' if module_type is None else module_type

    def reset_state(self, update_in_progress: bool = False) -> None:
        """ Reset firmware updater's state

        :param update_in_progress: Whether the method is called during the
        update process or at the end of the process
        :type update_in_progress: bool
        :return: None
        """
        self.response_flag = False
        self.response_error_flag = False
        self.response_error_count = 0
        self.update_in_progress = False

        if not update_in_progress:
            print("Resetting firmware updater's state")
            self.modules_to_update = []
            self.modules_updated = []

    def request_to_update_firmware(self, module_id) -> None:
        """ Remove firmware of MODI modules (Removes EndFlash)
        """
        firmware_update_message = self.__set_module_state(
            module_id, Module.UPDATE_FIRMWARE, Module.PNP_OFF
        )
        self.__conn.send_nowait(firmware_update_message)

    def check_to_update_firmware(self, module_id: int) -> None:
        """ Check if modules with no firmware are ready to update its firmware

        :param module_id: Id of the module to check
        :type module_id: int
        :return: None
        """
        firmware_update_ready_message = self.__set_module_state(
            module_id, Module.UPDATE_FIRMWARE_READY, Module.PNP_OFF
        )
        self.__conn.send_nowait(firmware_update_ready_message)

    def add_to_waitlist(self, module_id: int, module_type: str) -> None:
        """Add the module to the waitlist to update

        :param module_id: Id of the module
        :type module_id: int
        :param module_type: type of the module in string
        :type module_type: str
        :return: None
        """
        # Check if input module already exist in the list
        for curr_module_id, curr_module_type in self.modules_to_update:
            if module_id == curr_module_id:
                return

        # Check if module is already updated
        for curr_module_id, curr_module_type in self.modules_updated:
            if module_id == curr_module_id:
                return

        print(f"\rAdding {module_type} ({module_id}) to waiting list..."
              f"{' ' * 60}")

        # Add the module to the waiting list
        module_elem = module_id, module_type
        self.modules_to_update.append(module_elem)

    def update_module(self, module_id: int, module_type: str) -> None:
        """Initiate update process starting from the given module

        :param module_id: Id of the module
        :type module_id: int
        :param module_type: Name of the module
        :type module_type: str
        :return: None
        """
        if self.update_in_progress:
            return

        self.update_in_progress = True
        updater_thread = th.Thread(
            target=self.__update_firmware, args=(module_id, module_type)
        )
        updater_thread.daemon = True
        updater_thread.start()

    def update_response(self, response: bool,
                        is_error_response: bool = False) -> None:
        """Update the response flag

        :param response: Response flag
        :type response: bool
        :param is_error_response: Error response flag
        :type is_error_response: bool
        :return: None
        """
        if not is_error_response:
            self.response_flag = response
        else:
            self.response_error_flag = response

    def __update_firmware(self, module_id: int, module_type: str) -> None:
        """ Update firmware of a given module

        :param module_id: Id of the module
        :type module_id: int
        :param module_type: Name of the module
        :type module_type: str
        :return: None
        """
        self.update_in_progress = True
        self.modules_updated.append((module_id, module_type))

        root_path = (
            path.join(path.dirname(__file__), 'firmware', 'stm32')
        )

        if self.__is_os_update:
            # Init path to binary file
            bin_path = (
                f"{module_type.lower()}.bin"
            )

            bin_path = path.join(root_path, bin_path)

            with open(bin_path, 'rb') as bin_file:
                bin_buffer = bin_file.read()

            # Init metadata of the bytes loaded
            page_size = 0x800
            flash_memory_addr = 0x08000000

            bin_size = sys.getsizeof(bin_buffer)
            bin_begin = 0x9000
            bin_end = bin_size - ((bin_size - bin_begin) % page_size)
            for page_begin in range(bin_begin, bin_end + 1, page_size):
                print(f"\rUpdating {module_type} ({module_id}) "
                      f"{self.__progress_bar(page_begin, bin_end)} "
                      f"{page_begin * 100 // bin_end}%", end='')
                page_end = page_begin + page_size
                curr_page = bin_buffer[page_begin:page_end]
                # Skip current page if empty
                if not sum(curr_page):
                    continue

                # Erase page (send erase request and receive its response)
                erase_page_success = self.send_firmware_command(
                    oper_type="erase", module_id=module_id, crc_val=0,
                    dest_addr=flash_memory_addr, page_addr=page_begin
                )
                if not erase_page_success:
                    page_begin -= page_size
                    continue
                # Copy current page data to the module's memory
                checksum = 0
                for curr_ptr in range(0, page_size, 8):
                    if page_begin + curr_ptr >= bin_size:
                        break

                    curr_data = curr_page[curr_ptr:curr_ptr + 8]
                    checksum = self.send_firmware_data(
                        module_id,
                        seq_num=curr_ptr // 8,
                        bin_data=curr_data,
                        crc_val=checksum
                    )
                    self.__delay(0.002)

                # CRC on current page (send CRC request / receive CRC response)
                crc_page_success = self.send_firmware_command(
                    oper_type="crc", module_id=module_id, crc_val=checksum,
                    dest_addr=flash_memory_addr, page_addr=page_begin
                )
                if not crc_page_success:
                    page_begin -= page_size
                time.sleep(0.01)

        print(f"\rUpdating {module_type} ({module_id}) "
              f"{self.__progress_bar(1, 1)} 100%")
        # Include MODI firmware version when writing end flash
        version_path = path.join(root_path, 'version.txt')
        with open(version_path) as version_file:
            version_info = version_file.readline().lstrip('v').rstrip('\n')
        version_digits = [int(digit) for digit in version_info.split('.')]
        """ Version number is formed by concatenating all three version bits
            e.g. 2.2.4 -> 010 00010 00000100 -> 0100 0010 0000 0100
        """
        version = (
            version_digits[0] << 13
            | version_digits[1] << 8
            | version_digits[2]
        )

        # Set end-flash data to be sent at the end of the firmware update
        end_flash_data = bytearray(8)
        end_flash_data[0] = 0xAA
        end_flash_data[1] = 1
        end_flash_data[2] = 0
        end_flash_data[6] = version & 0xFF
        end_flash_data[7] = (version >> 8) & 0xFF
        self.send_end_flash_data(module_type, module_id, end_flash_data)

        # Firmware update flag down, resetting used flags
        print(f'Firmware update is done for {module_type} ({module_id})')
        self.reset_state(update_in_progress=True)

        if self.modules_to_update:
            print("Processing the next module to update the firmware..")
            next_module_id, next_module_type = self.modules_to_update.pop(0)
            self.__update_firmware(next_module_id, next_module_type)
        else:
            # Reboot all connected modules
            reboot_message = self.__set_module_state(
                0xFFF, Module.REBOOT, Module.PNP_OFF
            )
            self.__conn.send_nowait(reboot_message)
            print("Reboot message has been sent to all connected modules")
            self.reset_state()
            self.update_event.set()

    @staticmethod
    def __delay(span):
        init_time = time.perf_counter()
        while time.perf_counter() - init_time < span:
            pass
        return

    def __set_module_state(self, destination_id: int, module_state: int,
                           pnp_state: int) -> str:
        """ Generate message for set module state and pnp state

        :param destination_id: Id of the destination module
        :type destination_id: int
        :param module_state: State of the module
        :type module_state: int
        :param pnp_state: Pnp state of the module
        :type pnp_state: int
        :return: Json serialized message
        :rtype: str
        """
        message = dict()

        message["c"] = 0x09
        message["s"] = 0
        message["d"] = destination_id

        state_bytes = bytearray(2)
        state_bytes[0] = module_state
        state_bytes[1] = pnp_state

        message["b"] = b64encode(bytes(state_bytes)).decode("utf-8")
        message["l"] = 2

        return json.dumps(message, separators=(",", ":"))

    # TODO: Use retry decorator here
    def send_end_flash_data(self, module_type: str, module_id: int,
                            end_flash_data: bytearray) -> None:
        """Send the end flash data

        :param module_type: Name of the module
        :type module_type: str
        :param module_id: Id of the module
        :type module_id: int
        :param end_flash_data: Flag indicator of the end flash data
        :type end_flash_data: bool
        :return: None
        """
        # Write end-flash data until success
        end_flash_success = False
        while not end_flash_success:

            # Erase page (send erase request and receive erase response)
            erase_page_success = self.send_firmware_command(
                oper_type="erase", module_id=module_id, crc_val=0,
                dest_addr=0x0801F800
            )
            # TODO: Remove magic number of dest_addr above, try using flash_mem
            if not erase_page_success:
                continue

            # Send data
            checksum = self.send_firmware_data(
                module_id, seq_num=0, bin_data=end_flash_data, crc_val=0
            )

            # CRC on current page (send CRC request and receive CRC response)
            crc_page_success = self.send_firmware_command(
                oper_type="crc", module_id=module_id, crc_val=checksum,
                dest_addr=0x0801F800
            )
            if not crc_page_success:
                continue

            end_flash_success = True
        # print(f"End flash is written for {module_type} ({module_id})")

    def get_firmware_command(self, module_id: int, rot_stype: int,
                             rot_scmd: int, crc32: int, page_addr: int) -> str:
        """Create a new firmware command in json format

        :param module_id: Id of the module
        :type module_id: int
        :param rot_stype: ROT_StateType
        :type rot_stype: int
        :param rot_scmd: ROT_StreamCommand
        :type rot_scmd: int
        :param crc32: Crc checksum
        :type crc32: int
        :param page_addr: Page address
        :type page_addr: int
        :return: Json serialized message
        :rtype: str
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
        message["b"] = b64encode(
            bytes(crc32_and_page_addr_data)
        ).decode("utf-8")
        message["l"] = 8

        return json.dumps(message, separators=(",", ":"))

    def get_firmware_data(self, module_id: int, seq_num: int,
                          bin_data: bytes) -> str:
        """ A data to be sent when updating firmware of a module

        :param module_id: Id of the module
        :type module_id: int
        :param seq_num: Sequence number
        :type seq_num: int
        :param bin_data: Data to be sent
        :type bin_data: bytes
        :return: Json serialized message
        :rtype: str
        """
        message = dict()
        message["c"] = 0x0B
        message["s"] = seq_num
        message["d"] = module_id

        message["b"] = b64encode(bytes(bin_data)).decode("utf-8")
        message["l"] = 8

        return json.dumps(message, separators=(",", ":"))

    def calc_crc32(self, data: bytes, crc: int) -> int:
        """Checksum calculation

        :param data: Data to be sent
        :type data: bytes
        :param crc: Checksum
        :type crc: int
        :return: Calculated crc
        :rtype: int
        """
        crc ^= int.from_bytes(data, byteorder='little', signed=False)

        for _ in range(32):
            if crc & (1 << 31) != 0:
                crc = (crc << 1) ^ 0x4C11DB7
            else:
                crc <<= 1
            crc &= 0xFFFFFFFF

        return crc

    def calc_crc64(self, data: bytes, checksum: int) -> int:
        """Calculate crc

        :param data: Data to be sent
        :type data: bytes
        :param checksum: Checksum
        :type checksum: int
        :return: Checksum
        :rtype: int
        """
        checksum = self.calc_crc32(data[:4], checksum)
        checksum = self.calc_crc32(data[4:], checksum)
        return checksum

    def send_firmware_command(self, oper_type: str, module_id: int,
                              crc_val: int, dest_addr: int,
                              page_addr: int = 0) -> bool:
        """Send the command for the firmware

        :param oper_type: Type of the operation
        :type oper_type: int
        :param module_id: Id of the module
        :type module_id: int
        :param crc_val: Checksum value
        :type crc_val: int
        :param dest_addr: Address of the destination module
        :type dest_addr: int
        :param page_addr: Page address
        :type page_addr: int
        :return: Command response
        :rtype: bool
        """

        rot_scmd = 2 if oper_type == "erase" else 1

        # Send firmware command request
        request_message = self.get_firmware_command(
            module_id, 1, rot_scmd, crc_val, page_addr=dest_addr + page_addr
        )
        self.__conn.send_nowait(request_message)

        return self.receive_command_response()

    def receive_command_response(self, response_delay: float = 0.001,
                                 response_timeout: float = 5,
                                 max_response_error_count: int = 75) -> bool:
        """ Block until receiving a response of the most recent message sent

        :param response_delay: Delay time in seconds
        :type response_delay: float
        :param response_timeout: Timeout in seconds
        :type response_timeout: float
        :param max_response_error_count: Max error count
        :type max_response_error_count: int
        :return Boolean flag of the response
        :rtype: bool
        """
        # Receive firmware command response
        response_wait_time = 0
        while not self.response_flag:
            # Calculate timeout at each iteration
            time.sleep(response_delay)
            response_wait_time += response_delay

            # If timed-out
            if response_wait_time > response_timeout:
                raise Exception("Response timed-out")

            # If error is raised
            if self.response_error_flag:
                self.response_error_count += 1
                if self.response_error_count > max_response_error_count:
                    raise Exception("Response Errored")
                self.response_error_flag = False
                return False

        self.response_flag = False
        return True

    def send_firmware_data(self, module_id: int, seq_num: int, bin_data: bytes,
                           crc_val: int) -> int:
        """Send firmware data

        :param module_id: Id of the module
        :type module_id: int
        :param seq_num: Sequence number
        :type seq_num: int
        :param bin_data: Data to be sent
        :type bin_data: int
        :param crc_val: Checksum value
        :type crc_val: int
        :return: Calculated checksum value
        :rtype: int
        """
        # Send firmware data
        data_message = self.get_firmware_data(
            module_id, seq_num=seq_num, bin_data=bin_data
        )
        self.__conn.send_nowait(data_message)

        # Calculate crc32 checksum twice
        checksum = self.calc_crc64(data=bin_data, checksum=crc_val)
        return checksum

    def __progress_bar(self, current: int, total: int) -> str:
        """Returns a string format progress bar

        :param current: Current progress
        :type current: int
        :param total: Total workload
        :type total: int
        :return: Progress bar string
        :rtype: str
        """
        curr_bar = 50 * current // total
        rest_bar = 50 - curr_bar
        return f"[{'=' * curr_bar}>{'.' * rest_bar}]"

    def __read_conn(self):
        while True:
            self.__handle_message()
            time.sleep(0.001)
            if not self.__running:
                break

    def __handle_message(self):
        msg = self.__conn.recv()
        if not msg:
            return
        try:
            ins, sid, did, data, length = decode_message(msg)
        except json.JSONDecodeError:
            return
        command = {
            0x0A: self.__update_warning,
            0x0C: self.__update_firmware_state
        }.get(ins)

        if command:
            command(sid, data)

    def __update_firmware_state(self, sid: int, data: str):
        message_decoded = unpack_data(data, (4, 1))
        stream_state = message_decoded[1]

        if stream_state == self.CRC_ERROR:
            self.update_response(response=True, is_error_response=True)
        elif stream_state == self.CRC_COMPLETE:
            self.update_response(response=True)
        elif stream_state == self.ERASE_ERROR:
            self.update_response(response=True, is_error_response=True)
        elif stream_state == self.ERASE_COMPLETE:
            self.update_response(response=True)

    def __update_warning(self, sid: int, data: str) -> None:
        """Update the warning message

        :param sid: Source id
        :type sid: int
        :param data: Data str
        :type data: str
        :return: None
        """
        module_uuid = unpack_data(data, (6, 1))[0]
        warning_type = unpack_data(data, (6, 1))[1]

        # If warning shows current module works fine, return immediately
        if not warning_type:
            return

        module_id = sid
        module_type = self.__get_module_type_from_uuid(module_uuid)

        # No need to update network module's STM firmware
        if module_type == 'network':
            return

        if warning_type == 1:
            self.check_to_update_firmware(module_id)
        elif warning_type == 2:
            # Note that more than one warning type 2 message can be received
            if self.update_in_progress:
                self.add_to_waitlist(module_id, module_type)
            else:
                self.update_module(module_id, module_type)


def retry(exception_to_catch):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_to_catch:
                return wrapper(*args, **kwargs)

        return wrapper

    return decorator


class ESP32FirmwareUpdater(serial.Serial):
    DEVICE_READY = 0x2B
    DEVICE_SYNC = 0x08
    SPI_ATTACH_REQ = 0xD
    SPI_FLASH_SET = 0xB
    ESP_FLASH_BEGIN = 0x02
    ESP_FLASH_DATA = 0x03
    ESP_FLASH_END = 0x04

    ESP_FLASH_BLOCK = 0x200
    ESP_FLASH_CHUNK = 0x4000
    ESP_CHECKSUM_MAGIC = 0xEF

    def __init__(self):
        modi_ports = list_modi_ports()
        if not modi_ports:
            raise serial.SerialException("No MODI port is connected")
        super().__init__(modi_ports[0].device, timeout=0.1, baudrate=921600)
        print(f"Connecting to MODI network module at {modi_ports[0].device}")

        self.__address = [0x1000, 0x8000, 0XD000, 0x10000, 0xD0000]
        self.file_path = [
            'bootloader.bin', 'partitions.bin', 'ota_data_initial.bin',
            'modi_ota_factory.bin', 'esp32.bin'
        ]
        self.id = None
        self.version = None
        self.__version_to_update = None

    def update_firmware(self, force=False):
        self.__boot_to_app()
        self.__version_to_update = self.__get_latest_version()
        self.id = self.__get_esp_id()
        self.version = self.__get_esp_version()
        if self.version and self.version == self.__version_to_update:
            if not force:
                response = input(
                    f"ESP version already up to date (v{self.version})."
                    f" Do you still want to proceed? [y/n]: ")
                if 'y' not in response:
                    return
        print(f"Updating v{self.version} to v{self.__version_to_update}")
        firmware_buffer = self.__compose_binary_firmware()

        self.__device_ready()
        self.__device_sync()
        self.__flash_attach()
        self.__set_flash_param()
        manager = None
        self.__write_binary_firmware(firmware_buffer, manager)
        print("Booting to application...")
        self.__wait_for_json()
        self.__boot_to_app()
        time.sleep(1)
        self.__set_esp_version(self.__version_to_update)
        print("ESP firmware update is complete!!")

    def __device_ready(self):
        print("Redirecting connection to esp device...")
        self.write(b'{"c":43,"s":0,"d":4095,"b":"AA==","l":1}')

    def __device_sync(self):
        print("Syncing the esp device...")
        sync_pkt = self.__parse_pkt([
            0x0, self.DEVICE_SYNC, 0x24, 0, 0, 0, 0, 0, 0x7, 0x7, 0x12, 0x20
        ] + 32 * [0x55])
        self.__send_pkt(sync_pkt, timeout=10, continuous=True)
        print("Sync Complete")

    def __flash_attach(self):
        print("Attaching flash to esp device..")
        attach_pkt = self.__parse_pkt([
            0x0, self.SPI_ATTACH_REQ, 0x8
        ] + 13 * [0])
        self.__send_pkt(attach_pkt, timeout=10)
        print("Flash attach Complete")

    def __set_flash_param(self):
        print("Setting esp flash parameter...")
        param_data = [0] * 32
        fl_id, total_size, block_size, sector_size, page_size, status_mask = (
            0, 2 * 1024 * 1024, 64 * 1024, 4 * 1024, 256, 0xFFFF
        )
        param_data[1] = self.SPI_FLASH_SET
        param_data[2] = 0x18
        param_data[8:12] = int.to_bytes(fl_id, length=4, byteorder='little')
        param_data[12:16] = int.to_bytes(
            total_size, length=4, byteorder='little'
        )
        param_data[16:20] = int.to_bytes(
            block_size, length=4, byteorder='little'
        )
        param_data[20:24] = int.to_bytes(
            sector_size, length=4, byteorder='little'
        )
        param_data[24:28] = int.to_bytes(
            page_size, length=4, byteorder='little'
        )
        param_data[28:32] = int.to_bytes(
            status_mask, length=4, byteorder='little'
        )
        param_pkt = self.__parse_pkt(param_data)
        self.__send_pkt(param_pkt, timeout=10)
        print("Parameter set complete")

    @staticmethod
    def __parse_pkt(data):
        pkt = bytes(data)
        pkt = pkt.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc')
        pkt = b'\xc0' + pkt + b'\xc0'
        return pkt

    @retry(Exception)
    def __send_pkt(self, pkt, wait=True, timeout=None, continuous=False):
        self.write(pkt)
        self.reset_input_buffer()
        if wait:
            cmd = bytearray(pkt)[2]
            init_time = time.time()
            while not timeout or time.time() - init_time < timeout:
                if continuous:
                    time.sleep(0.1)
                else:
                    time.sleep(0.01)
                recv_pkt = self.__read_slip()
                if not recv_pkt:
                    if continuous:
                        self.__send_pkt(pkt, wait=False)
                    continue
                recv_cmd = bytearray(recv_pkt)[2]
                if cmd == recv_cmd:
                    if bytearray(recv_pkt)[1] != 0x01:
                        raise Exception
                    return True
                elif continuous:
                    self.__send_pkt(pkt, wait=False)
            print("Sending Again...")
            raise Exception("Timeout Expired!")

    def __read_slip(self):
        slip_pkt = b''
        while slip_pkt != b'\xc0':
            slip_pkt = self.read()
            if slip_pkt == b'':
                return b''
        slip_pkt += self.read_until(b'\xc0')
        return slip_pkt

    def __read_json(self):
        json_pkt = b''
        while json_pkt != b'{':
            json_pkt = self.read()
            if json_pkt == b'':
                return ''
        json_pkt += self.read_until(b'}')
        return json_pkt

    def __wait_for_json(self):
        json_msg = self.__read_json()
        while not json_msg:
            json_msg = self.__read_json()
            time.sleep(0.01)
        return json_msg

    def __get_esp_id(self):
        json_msg = json.loads(self.__wait_for_json())
        while json_msg['c'] != 0:
            json_msg = json.loads(self.__wait_for_json())
        return json_msg['s']

    def __get_esp_version(self):
        get_version_pkt = b'{"c":160,"s":25,"d":4095,"b":"AAAAAAAAAA==","l":8}'
        self.write(get_version_pkt)
        json_msg = json.loads(self.__wait_for_json())
        init_time = time.time()
        while json_msg['c'] != 0xA1:
            self.write(get_version_pkt)
            json_msg = json.loads(self.__wait_for_json())
            if time.time() - init_time > 1:
                return None
        ver = b64decode(json_msg['b']).lstrip(b'\x00')
        return ver.decode('ascii')

    def __set_esp_version(self, version_text: str):
        print(f"Writing version info (v{version_text})")
        version_byte = version_text.encode('ascii')
        version_byte = b'\x00' * (8 - len(version_byte)) + version_byte
        version_text = b64encode(version_byte).decode('utf8')
        version_msg = '{' + f'"c":160,"s":24,"d":4095,' \
                            f'"b":"{version_text}","l":8' + '}'
        version_msg_enc = version_msg.encode('utf8')
        self.write(version_msg_enc)

        while json.loads(self.__wait_for_json())['c'] != 0xA1:
            time.sleep(0.5)
            self.__boot_to_app()
            self.write(version_msg.encode('utf8'))
        print("The version info has been set!!")

    def __compose_binary_firmware(self):
        binary_firmware = b''
        root_path = path.join(
            path.dirname(__file__), 'firmware', 'esp32'
        )
        for i, bin_path in enumerate(self.file_path):
            with open(path.join(root_path, bin_path), 'rb') as bin_file:
                bin_data = bin_file.read()
            binary_firmware += bin_data
            if i < len(self.__address) - 1:
                binary_firmware += b'\xFF' * (
                    self.__address[i + 1] - self.__address[i] - len(bin_data)
                )
        return binary_firmware

    @staticmethod
    def __get_latest_version():
        root_path = path.join(
            path.dirname(__file__), 'firmware', 'esp32'
        )
        with open(path.join(root_path, 'version.txt'), 'r') as version_file:
            version_info = version_file.readline().lstrip('v').rstrip('\n')
        return version_info

    def __erase_chunk(self, size, offset):
        num_blocks = size // self.ESP_FLASH_BLOCK + 1
        erase_data = [0] * 24
        erase_data[1] = self.ESP_FLASH_BEGIN
        erase_data[2] = 0x10
        erase_data[8:12] = int.to_bytes(size, length=4, byteorder='little')
        erase_data[12:16] = int.to_bytes(
            num_blocks, length=4, byteorder='little'
        )
        erase_data[16:20] = int.to_bytes(
            self.ESP_FLASH_BLOCK, length=4, byteorder='little'
        )
        erase_data[20:24] = int.to_bytes(
            offset, length=4, byteorder='little'
        )
        erase_pkt = self.__parse_pkt(erase_data)
        self.__send_pkt(erase_pkt, timeout=10)

    def __write_flash_block(self, data, seq_block):
        size = len(data)
        block_data = [0] * (size + 24)
        checksum = self.ESP_CHECKSUM_MAGIC

        block_data[1] = self.ESP_FLASH_DATA
        block_data[2:4] = int.to_bytes(size + 16, length=2, byteorder='little')
        block_data[8:12] = int.to_bytes(size, length=4, byteorder='little')
        block_data[12:16] = int.to_bytes(
            seq_block, length=4, byteorder='little'
        )
        for i in range(size):
            block_data[24 + i] = data[i]
            checksum ^= (0xFF & data[i])
        block_data[4:8] = int.to_bytes(checksum, length=4, byteorder='little')
        block_pkt = self.__parse_pkt(block_data)
        self.__send_pkt(block_pkt)

    def __write_binary_firmware(self, binary_firmware: bytes, manager):
        chunk_queue = []
        num_blocks = len(binary_firmware) // self.ESP_FLASH_BLOCK + 1
        while binary_firmware:
            if self.ESP_FLASH_CHUNK < len(binary_firmware):
                chunk_queue.append(binary_firmware[:self.ESP_FLASH_CHUNK])
                binary_firmware = binary_firmware[self.ESP_FLASH_CHUNK:]
            else:
                chunk_queue.append(binary_firmware[:])
                binary_firmware = b''

        blocks_downloaded = 0
        print("Start uploading firmware data...")
        for seq, chunk in enumerate(chunk_queue):
            self.__erase_chunk(
                len(chunk), self.__address[0] + seq * self.ESP_FLASH_CHUNK
            )
            blocks_downloaded += self.__write_chunk(
                chunk, blocks_downloaded, num_blocks, manager
            )
        if manager:
            manager.quit()
        print(f"\r{self.__progress_bar(1, 1)}")
        print("Firmware Upload Complete")

    def __write_chunk(self, chunk, curr_seq, total_seq, manager):
        block_queue = []
        while chunk:
            if self.ESP_FLASH_BLOCK < len(chunk):
                block_queue.append(chunk[:self.ESP_FLASH_BLOCK])
                chunk = chunk[self.ESP_FLASH_BLOCK:]
            else:
                block_queue.append(chunk[:])
                chunk = b''
        for seq, block in enumerate(block_queue):
            if manager:
                manager.status = self.__progress_bar(curr_seq + seq, total_seq)
            print(f'\r{self.__progress_bar(curr_seq + seq, total_seq)}',
                  end='')
            self.__write_flash_block(block, seq)
        return len(block_queue)

    def __boot_to_app(self):
        self.write(b'{"c":160,"s":0,"d":174,"b":"AAAAAAAAAA==","l":8}')

    @staticmethod
    def __progress_bar(current: int, total: int) -> str:
        curr_bar = 70 * current // total
        rest_bar = 70 - curr_bar
        return f"Firmware Upload: [{'=' * curr_bar}>{'.' * rest_bar}] " \
               f"{100 * current / total:3.2f}%"
