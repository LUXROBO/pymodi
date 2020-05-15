import time
import queue
import serial

from serial import SerialException

from modi._communicator_task import CommunicatorTask


class SerTask(CommunicatorTask):

    def __init__(self, ser_recv_q, ser_send_q):
        print("Run Ser Task.")
        super().__init__(ser_recv_q, ser_send_q)
        self._ser_recv_q = ser_recv_q
        self._ser_send_q = ser_send_q

        self.__ser = None
        self.__json_buffer = ""

    #
    # Inherited Methods
    #
    def open_conn(self):
        """ Open serial port
        """

        modi_ports = self._list_modi_ports()
        if not modi_ports:
            raise SerialException("No MODI network module is connected.")

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

    def _close_conn(self):
        """ Close serial port
        """

        self.__ser.close()

    def _read_data(self):
        """ Read serial message and put message to serial read queue
        """

        serial_buffer = self.__ser.in_waiting
        if serial_buffer:
            # Flush the serial buffer and concatenate it to json buffer
            self.__json_buffer += self.__ser.read(
                serial_buffer
            ).decode("utf-8")

            # Once json buffer is obtained, we parse and send json message
            self.__parse_serial()

    def _write_data(self):
        """ Write serial message in serial write queue
        """

        try:
            message_to_write = self._ser_send_q.get_nowait().encode()
        except queue.Empty:
            pass
        else:
            self.__ser.write(message_to_write)

    def run_read_data(self, delay):
        while True:
            self._read_data()
            time.sleep(delay)

    def run_write_data(self, delay):
        while True:
            self._write_data()
            time.sleep(delay)

    #
    # Helper method
    #
    def __parse_serial(self):
        # While there is a valid json in the json buffer
        while "{" in self.__json_buffer and "}" in self.__json_buffer:
            split_index = self.__json_buffer.find("}") + 1

            # Parse json message and send it
            json_msg = self.__json_buffer[:split_index]
            self._ser_recv_q.put(json_msg)

            # Update json buffer, remove the json message sent
            self.__json_buffer = self.__json_buffer[split_index:]
