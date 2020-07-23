
import os
import time
import queue
import serial
import traceback
import sys

from serial.serialutil import SerialException

from modi.task.conn_task import ConnTask


class SerTask(ConnTask):

    def __init__(self, ser_recv_q, ser_send_q, verbose, port=None):
        print("Run Ser Task.")
        super().__init__(ser_recv_q, ser_send_q)
        self._ser_recv_q = ser_recv_q
        self._ser_send_q = ser_send_q
        self.__verbose = verbose
        self.__ser = None
        self.__json_buffer = ""
        self.__port = port
        if self.__verbose:
            print('PyMODI log...\n==================================')
            sys.stdout.flush()

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

    #
    # Inherited Methods
    #
    def open_conn(self) -> None:
        """ Open serial port

        :return: None
        """

        modi_ports = ConnTask.list_modi_ports()
        if not modi_ports:
            raise SerialException("No MODI network module is connected.")

        if self.__port:
            if self.__port not in map(lambda info: info.device, modi_ports):
                raise SerialException(f"{self.__port} is not connected "
                                      f"to a MODI network module.")
            else:
                try:
                    self.__init_serial(self.__port)
                    self.__ser.open()
                    return
                except SerialException:
                    raise SerialException(f"{self.__port} is not available.")

        for modi_port in modi_ports:
            self.__init_serial(modi_port.device)
            try:
                self.__ser.open()
                return
            except SerialException:
                continue
        raise SerialException("No MODI port is available now")

    def __init_serial(self, port):
        self.__ser = serial.Serial(exclusive=True)
        self.__ser.baudrate = 921600
        self.__ser.port = port
        self.__ser.timeout = 1

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
            ).decode("utf8")

            # Once json buffer is obtained, we parse and send json message
            self.__parse_serial()
        else:
            time.sleep(0.01)

    def _send_data(self) -> None:
        """ Write serial message in serial write queue

        :return: None
        """
        try:
            message_to_send = self._ser_send_q.get_nowait().encode()
        except queue.Empty:
            time.sleep(0.01)
        else:
            self.__ser.write(message_to_send)
            if self.__verbose:
                sys.stdout.write(f'send: {message_to_send.decode("utf8")}\n')
                sys.stdout.flush()

    def run_recv_data(self, delay: float) -> None:
        """Read data through serial port

        :param delay: time value to wait in seconds
        :type delay: float
        :return: None
        """
        while True:
            try:
                self._recv_data()
            except SerialException:
                print("\nMODI connection is lost!!!")
                traceback.print_exc()
                os._exit(1)

    def run_send_data(self, delay: float) -> None:
        """Write data through serial port

        :param delay: time value to wait in seconds
        :type delay: float
        :return: None
        """
        while True:
            try:
                self._send_data()
            except SerialException:
                print("\nMODI connection is lost!!!")
                traceback.print_exc()
                os._exit(1)

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
            self._ser_recv_q.put(json_msg)
            if self.__verbose:
                sys.stdout.write(f'recv: {json_msg}\n')
                sys.stdout.flush()
            # Update json buffer, remove the json message sent
            self.__json_buffer = self.__json_buffer[split_index:]
