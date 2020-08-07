from typing import Optional

import serial
from serial.serialutil import SerialException

from modi.task.conn_task import ConnTask
from modi.util.conn_util import list_modi_ports


class SerTask(ConnTask):

    def __init__(self, verbose=False, port=None):
        print("Initiating serial connection...")
        super().__init__(verbose)
        self.__port = port

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
        if self._bus.in_waiting:
            json_pkt = b''
            while json_pkt != b'{':
                if not self._bus.in_waiting:
                    return None
                json_pkt = self._bus.read()

            json_pkt += self._bus.read_until(b'}')
            json_pkt = json_pkt.decode('utf8')
            if self.verbose:
                print(f'recv: {json_pkt}')
            return json_pkt
        else:
            return None

    def send(self, pkt: str) -> None:
        """ Send json pkt

        :param pkt: Json pkt to send
        :type pkt: str
        :return: None
        """
        self._bus.write(pkt.encode('utf8'))
        if self.verbose:
            print(f'send: {pkt}')
