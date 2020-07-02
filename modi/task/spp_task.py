import time
import queue
import serial
import serial.tools.list_ports as stl

from typing import List
from serial import SerialException
from serial.tools.list_ports_common import ListPortInfo

from modi.task.conn_task import ConnTask


class SppTask(ConnTask):

    def __init__(self, spp_recv_q, spp_send_q, module_uuid, verbose, port=None):
        print("Run Spp Task.")
        super().__init__(spp_recv_q, spp_send_q)
        self._spp_recv_q = spp_recv_q
        self._spp_send_q = spp_send_q
        self._module_uuid = module_uuid

        self.__verbose = verbose
        if self.__verbose:
            print('PyMODI log...\n==================================')

        self.__ser = None
        self.__json_buffer = ""

    @property
    def get_serial(self) -> serial.Serial:
        """Getter method for the serial

        :return: __ser
        """
        return self.__ser

    def set_serial(self, ser: serial.Serial) -> None:
        """Manually sets the __ser

        :param ser: Serial to set the __ser
        :return: None
        """
        self.__ser = ser

    def _list_modi_ports(self) -> List[ListPortInfo]:
        """Returns a list of all the connected MODI ports

        :return: List[ListPortInfo]
        """
        modi_ports = list()
        ports = stl.comports()
        for port in ports:
            if self._module_uuid in port.device \
                or ("Bluetooth" in port.description
                    and port.hwid.split('&')[1][:4] == '0002'):
                modi_ports.append(port)

        if not modi_ports:
            devices = [port.device for port in ports]
            print("Currently connected devices are:", devices)
            raise Exception(
                "No MODI network module is connected. "
                "Have you connected your network module using bluetooth?"
            )

        # TODO: Support multiple network module
        if len(modi_ports) > 1:
            print("Current MODI ports are:", modi_ports)
            raise Exception("More than one MODI network module exist.")
        return modi_ports

    #
    # Inherited Methods
    #
    def open_conn(self) -> None:
        """ Open serial port

        :return: None
        """

        modi_ports = self._list_modi_ports()

        # TODO: Refactor code to support multiple MODI network modules here
        modi_port = modi_ports.pop()
        self.__ser = serial.Serial()
        self.__ser.baudrate = 921600
        self.__ser.port = modi_port.device

        # Check if the modi port(i.e. MODI network module) is in use
        if self.__ser.is_open:
            raise SerialException(
                "The MODI port {} is already in use".format(self.__ser.port)
            )
        self.__ser.open()
        time.sleep(1)

    def _close_conn(self) -> None:
        """ Close serial port

        :return: None
        """

        self.__ser.close()

    def _recv_data(self) -> None:
        """ Read serial message and put message to serial read queue

        :return: None
        """

        serial_buffer = self.__ser.in_waiting
        if serial_buffer:
            # Flush the serial buffer and concatenate it to json buffer
            self.__json_buffer += self.__ser.read(
                serial_buffer
            ).decode("utf-8")

            # Once json buffer is obtained, we parse and send json message
            self.__parse_serial()

    def _send_data(self) -> None:
        """ Write serial message in serial write queue

        :return: None
        """

        try:
            message_to_send = self._spp_send_q.get_nowait().encode()
        except queue.Empty:
            pass
        else:
            self.__ser.write(message_to_send)
            if self.__verbose:
                print(f'send: {message_to_send.decode("utf8")}')

    def run_recv_data(self, delay: float) -> None:
        """Read data through spp

        :param delay: time value to wait in seconds
        :type delay: float
        :return: None
        """
        while True:
            self._recv_data()
            time.sleep(delay)

    def run_send_data(self, delay: float) -> None:
        """Write data through spp

        :param delay: time value to wait in seconds
        :type delay: float
        :return: None
        """
        while True:
            self._send_data()
            time.sleep(delay)

    #
    # Helper method
    #
    def __parse_serial(self) -> None:
        """Update the json buffer

        :return: None
        """
        # While there is a valid json in the json buffer
        while "{" in self.__json_buffer and "}" in self.__json_buffer:
            split_index = self.__json_buffer.find("}") + 1

            # Parse json message and send it
            json_msg = self.__json_buffer[:split_index]
            self._spp_recv_q.put(json_msg)
            if self.__verbose:
                print(f'recv: {json_msg}')

            # Update json buffer, remove the json message sent
            self.__json_buffer = self.__json_buffer[split_index:]
