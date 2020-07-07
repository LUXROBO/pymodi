import io
import sys
import time
import json
import base64
import zipfile
import requests

import threading as th
import urllib.request as ur

from urllib.error import URLError
from enum import IntEnum

from modi.module.module import Module


class FirmwareUpdater:
    """Module Firmware Updater: Updates a firmware of given module"""

    class State(IntEnum):
        NO_ERROR = 0
        UPDATE_READY = 1
        WRITE_FAIL = 2
        VERIFY_FAIL = 3
        CRC_ERROR = 4
        CRC_COMPLETE = 5
        ERASE_ERROR = 6
        ERASE_COMPLETE = 7

    def __init__(self, send_q):
        self._send_q = send_q

        self.response_flag = False
        self.response_error_flag = False
        self.response_error_count = 0

        self.update_event = th.Event()
        self.update_in_progress = False
        self.modules_to_update = []
        self.modules_updated = []

    def __get_module_type_from_uuid(self, uuid: int) -> str:
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
            '2060': 'Infrared',

            # Output modules
            '4000': 'Display',
            '4010': 'Motor',
            '4020': 'Led',
            '4030': 'Speaker',
        }.get(type_indicator)
        return 'Network' if module_type is None else module_type

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

    def request_to_update_firmware(self) -> None:
        """ Remove firmware of MODI modules (Removes EndFlash)
        """

        firmware_update_message = self.__set_module_state(
            0xFFF, Module.State.UPDATE_FIRMWARE, Module.State.PNP_OFF
        )
        self._send_q.put(firmware_update_message)

    def check_to_update_firmware(self, module_id: int) -> None:
        """ Check if modules with no firmware are ready to update its firmware

        :param module_id: Id of the module to check
        :type module_id: int
        :return: None
        """

        firmware_update_ready_message = self.__set_module_state(
            module_id, Module.State.UPDATE_FIRMWARE_READY, Module.State.PNP_OFF
        )
        self._send_q.put(firmware_update_ready_message)

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

        for curr_module_id, curr_module_type in self.modules_updated:
            if module_id == curr_module_id:
                return

        print(f"Adding {module_type} ({module_id}) to waiting list..")

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

        print(
            "Start updating the binary firmware "
            f"for {module_type} ({module_id})"
        )
        self.update_in_progress = True
        self.modules_updated.append((module_id, module_type))

        # Init path to binary file
        root_path = (
            'https://download.luxrobo.com/modi-skeleton-mobile/skeleton.zip'
        )
        bin_path = (
            f"skeleton/{module_type}.bin"
            if module_type != 'env' else
            "skeleton/environment.bin"
        )

        try:
            # Init bytes data from the given binary file of the current module
            download_response = requests.get(root_path)
        except URLError:
            raise URLError("Failed to download firmware. Check your internet")
        zip_content = zipfile.ZipFile(
            io.BytesIO(download_response.content), 'r'
        )
        bin_buffer = zip_content.read(bin_path)

        # Init metadata of the bytes loaded
        page_size = 0x800
        flash_memory_addr = 0x08000000

        bin_size = sys.getsizeof(bin_buffer)
        bin_begin = 0x9000
        bin_end = bin_size - ((bin_size - bin_begin) % page_size)
        for page_begin in range(bin_begin, bin_end + 1, page_size):
            print(f"{self.__progress_bar(page_begin, bin_end)} "
                  f"{page_begin * 100 // bin_end}% \r", end='')
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
                time.sleep(0.0025)

            # CRC on current page (send CRC request and receive CRC response)
            crc_page_success = self.send_firmware_command(
                oper_type="crc", module_id=module_id, crc_val=checksum,
                dest_addr=flash_memory_addr, page_addr=page_begin
            )
            if not crc_page_success:
                page_begin -= page_size

        # Include MODI firmware version when writing end flash
        version_path = (
            "https://download.luxrobo.com/modi-skeleton-mobile/version.txt"
        )
        version_info = None
        for line in ur.urlopen(version_path):
            version_info = line.decode('utf-8').lstrip('v')
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
        end_flash_data[1] = 0
        end_flash_data[2] = 0
        end_flash_data[6] = version & 0xFF
        end_flash_data[7] = (version >> 8) & 0xFF
        self.send_end_flash_data(module_type, module_id, end_flash_data)

        # Firmware update flag down, resetting used flags
        print(f'\nFirmware update is done for {module_type} ({module_id})')
        self.reset_state(update_in_progress=True)

        if self.modules_to_update:
            print("Processing the next module to update the firmware..")
            next_module_id, next_module_type = self.modules_to_update.pop(0)
            self.__update_firmware(next_module_id, next_module_type)
        else:
            # Reboot all connected modules
            reboot_message = self.__set_module_state(
                0xFFF, Module.State.REBOOT, Module.State.PNP_OFF
            )
            self._send_q.put(reboot_message)
            print("Reboot message has been sent to all connected modules")
            self.reset_state()
            self.update_event.set()

    def __set_module_state(self, destination_id: int, module_state: IntEnum,
                           pnp_state: IntEnum) -> str:
        """ Generate message for set module state and pnp state

        :param destination_id: Id of the destination module
        :type destination_id: int
        :param module_state: State of the module
        :type module_state: IntEnum
        :param pnp_state: Pnp state of the module
        :type pnp_state: IntEnum
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

        message["b"] = base64.b64encode(bytes(state_bytes)).decode("utf-8")
        message["l"] = 2

        return json.dumps(message, separators=(",", ":"))

    # TODO: Use retry decorator here
    def send_end_flash_data(self, module_type: str, module_id: int,
                            end_flash_data: bool) -> None:
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
        message["b"] = base64.b64encode(
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

        message["b"] = base64.b64encode(bytes(bin_data)).decode("utf-8")
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
        self._send_q.put(request_message)

        return self.receive_command_response()

    def receive_command_response(self, response_delay: float = 0.1,
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
        self._send_q.put(data_message)

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
        return f"Updating: [{'=' * curr_bar}>{'.' * rest_bar}]"
