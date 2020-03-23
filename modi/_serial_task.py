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

        self.__json_buffer = ""

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

        serial_buffer = self.__ser.in_waiting
        if serial_buffer:
            # Flush the serial buffer and concatenate it to json buffer
            self.__json_buffer += self.__ser.read(
                serial_buffer
            ).decode("utf-8")

            # Once json buffer is obtained, we parse and send json message
            self.__send_serial()

    def __send_serial(self):
        # While there is a valid json in the json buffer
        while "{" in self.__json_buffer and "}" in self.__json_buffer:
            split_index = self.__json_buffer.find("}") + 1

            # Parse json message and send it
            json_msg = self.__json_buffer[:split_index]
            self._serial_read_q.put(json_msg)

            # Update json buffer, remove the json message sent
            self.__json_buffer = self.__json_buffer[split_index:]

    def __write_serial(self):
        """ Write serial message in serial write queue
        """

        try:
            message_to_write = self._serial_write_q.get_nowait().encode()
        except queue.Empty:
            pass
        else:
            self.__ser.write(message_to_write)
