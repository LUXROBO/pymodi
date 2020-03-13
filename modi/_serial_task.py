import time
import queue
import serial
import serial.tools.list_ports as stl

from serial import SerialException


class SerialTask:
    """
    :param queue serial_read_q: Multiprocessing Queue for serial reading data
    :param queue serial_write_q: Multiprocessing Queue for serial writing data
    """

    def __init__(self, serial_read_q, serial_write_q):
        super(SerialTask, self).__init__()
        self.__ser = self.__open_serial()

        self._serial_read_q = serial_read_q
        self._serial_write_q = serial_write_q

    @staticmethod
    def __list_modi_ports():
        def __is_modi_port(port):
            return (
                port.manufacturer == "LUXROBO" or
                port.product == "MODI Network Module" or
                port.description == "MODI Network Module" or
                (port.vid == 12254 and port.pid == 2)
            )

        return [port for port in stl.comports() if __is_modi_port(port)]

    def __open_serial(self):
        """ Open serial port
        """

        modi_ports = self.__list_modi_ports()
        if not modi_ports:
            raise SerialException("No MODI network module is connected.")

        # TODO: Refactor code to support multiple MODI network modules here
        modi_port = modi_ports.pop()
        ser = serial.Serial()
        ser.baudrate = 921600
        ser.port = modi_port.device

        # Check if the modi port(i.e. MODI network module) is in use
        if ser.is_open:
            raise SerialException(
                "The MODI port {} is already in use".format(ser.port)
            )
        ser.open()
        return ser

    def close_serial(self):
        """ Close serial port
        """

        self.__ser.close()

    def run(self):
        """ Run serial task
        """

        self.__read_serial()
        self.__write_serial()

        # TODO: Replace time.sleep below
        time.sleep(0.008)

    def __read_serial(self):
        """ Read serial message and put message to serial read queue
        """

        buffer = self.__ser.in_waiting
        if buffer:
            message_to_read = self.__ser.read(buffer).decode()
            self._serial_read_q.put(message_to_read)

    def __write_serial(self):
        """ Write serial message in serial write queue
        """

        try:
            message_to_write = self._serial_write_q.get_nowait().encode()
        except queue.Empty:
            pass
        else:
            self.__ser.write(message_to_write)
