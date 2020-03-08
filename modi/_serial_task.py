import time
import queue
import serial
import serial.tools.list_ports as stl


class SerialTask:
    """
    :param queue serial_read_q: Multiprocessing Queue for serial reading data
    :param queue serial_write_q: Multiprocessing Queue for serial writing data
    """

    def __init__(self, serial_read_q, serial_write_q):
        super(SerialTask, self).__init__()
        self.__serial = None

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

    def open_serial(self):
        """ Open serial port
        """

        ports = self.__list_modi_ports()
        if len(ports) > 0:
            self.__serial = serial.Serial(ports[0].device, 921600)
        else:
            raise serial.SerialException("No MODI network module connected.")

    def close_serial(self):
        """ Close serial port
        """

        self.__serial.close()

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

        if self.__serial.in_waiting != 0:
            message_to_read = self.__serial.read(
                self.__serial.in_waiting).decode()
            self._serial_read_q.put(message_to_read)

    def __write_serial(self):
        """ Write serial message in serial write queue
        """

        try:
            message_to_write = self._serial_write_q.get_nowait().encode()
        except queue.Empty:
            pass
        else:
            self.__serial.write(message_to_write)

