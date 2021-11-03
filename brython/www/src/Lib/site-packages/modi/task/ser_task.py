from typing import Optional

import serial
from serial.serialutil import SerialException
from modi.task.conn_task import ConnTask
from modi.util.connection_util import list_modi_ports


class SerTask(ConnTask):

    def __init__(self, verbose=False, port=None):
        print("Initiating serial connection...")
        super().__init__(verbose)
        self.__port = port
        self.__json_buffer = b''

    #
    # Inherited Methods
    #
    def open_conn(self) -> None:
        """ Open serial port

        :return: None
        """
        modi_ports = list_modi_ports()
        if not modi_ports:
            raise SerialException("No MODI network module is available")

        if self.__port:
            if self.__port not in map(lambda info: info.device, modi_ports):
                raise SerialException(f"{self.__port} is not connected "
                                      f"to a MODI network module.")
            else:
                try:
                    self._bus = self.__init_serial(self.__port)
                    self._bus.open()
                    return
                except SerialException:
                    raise SerialException(f"{self.__port} is not available.")

        for modi_port in modi_ports:
            self._bus = self.__init_serial(modi_port.device)
            try:
                self._bus.open()
                print(f'Serial is open at "{modi_port}"')
                return
            except SerialException:
                continue
        raise SerialException("No MODI port is available now")

    @staticmethod
    def __init_serial(port):
        ser = serial.Serial(exclusive=True)
        ser.baudrate = 921600
        ser.port = port
        ser.write_timeout = 0
        return ser

    def close_conn(self) -> None:
        """ Close serial port

        :return: None
        """
        self._bus.close()

    def recv(self) -> Optional[str]:
        """ Read serial message and put message to serial read queue

        :return: str
        """
        buf_temp = self._bus.read_all()
        self.__json_buffer += buf_temp
        idx = self.__json_buffer.find(b'{')
        if idx < 0:
            self.__json_buffer = b''
            return None
        self.__json_buffer = self.__json_buffer[idx:]
        idx = self.__json_buffer.find(b'}')
        if idx < 0:
            return None
        json_pkt = self.__json_buffer[:idx + 1].decode('utf8')
        self.__json_buffer = self.__json_buffer[idx + 1:]
        if self.verbose:
            print(f'recv: {json_pkt}')
        return json_pkt

    @ConnTask.wait
    def send(self, pkt: str, verbose=False) -> None:
        """ Send json pkt

        :param pkt: Json pkt to send
        :type pkt: str
        :param verbose: Verbosity parameter
        :type verbose: bool
        :return: None
        """
        self._bus.write(pkt.encode('utf8'))
        if self.verbose or verbose:
            print(f'send: {pkt}')

    def send_nowait(self, pkt: str, verbose=False) -> None:
        """ Send json pkt

        :param pkt: Json pkt to send
        :type pkt: str
        :param verbose: Verbosity parameter
        :type verbose: bool
        :return: None
        """
        self._bus.write(pkt.encode('utf8'))
        if self.verbose or verbose:
            print(f'send: {pkt}')
