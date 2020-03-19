import os
import can
import json
import base64

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
        self.__can_mode = (
            self.__is_on_pi() and self.__is_network_module_connected()
        )
        if self.__can_mode:
            self.__can_up()
            self.__can0 = can.interface.Bus(
                channel="can0", bustype="socketcan_ctypes"
            )
        else:
            self.__ser = self.__open_serial()

        self._serial_read_q = serial_read_q
        self._serial_write_q = serial_write_q

    def run(self):
        """ Run serial task
        """

        self.__read_serial()
        self.__write_serial()

        # TODO: Replace time.sleep below
        time.sleep(0.004)

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

    @staticmethod
    def __is_on_pi():
        return os.uname()[4][:3] == "arm"

    def __is_network_module_connected(self):
        return bool(self.__list_modi_ports())

    #
    # Can Methods
    #
    def __can_up(self):
        os.system("sudo ip link set can0 type can bitrate 1000000")
        os.system("sudo ifconfig can0 up")

    def __can_down(self):
        os.system("sudo ifconfig can0 down")

    def __can_recv(self, timeout=None):
        can_msg = self.__can0.recv(timeout=timeout)
        if can_msg is None:
            raise ValueError("Can message not received!")
        return can_msg

    @staticmethod
    def __parse_can_msg(can_msg):
        """ Parse a can message to json format
        """
        can_id = can_msg.arbitration_id
        can_dlc = can_msg.can_dlc
        can_data = can_msg.data

        can_id_in_bin_str = format(can_id, "029b")
        c, s, d = SerialTask.__parse_can_id(can_id_in_bin_str)

        json_msg = dict()
        json_msg["c"], json_msg["s"], json_msg["d"] = c, s, d
        json_msg["b"] = base64.b64decode(can_data).decode("utf-8")
        json_msg["l"] = can_dlc
        return json.dumps(json_msg, separators=(",", ":"))

    @staticmethod
    def __parse_can_id(can_id):
        """ Parse a 29 bits length Can ID into INS, SID and DID
        """
        BIN = 2
        SID_BEGIN_IDX = 5
        DID_BEGIN_IDX = 17

        ins = int(can_id[:SID_BEGIN_IDX], BIN)
        sid = int(can_id[SID_BEGIN_IDX:DID_BEGIN_IDX], BIN)
        did = int(can_id[DID_BEGIN_IDX:], BIN)
        return ins, sid, did

    def __can_send(self, str_msg):
        """ Given parsed binary string message in json format, 
            convert and send the message as CAN format
        """

        json_msg = json.loads(str_msg)
        can_msg = self.__compose_can_msg(json_msg)
        try:
            self.__can0.send(can_msg)
        except can.CanError:
            raise ValueError("Can message not sent!")

    @staticmethod
    def __compose_can_msg(json_msg):
        ins = format(json_msg["c"], '05b')
        sid = format(json_msg["s"], '012b')
        did = format(json_msg["d"], '012b')
        can_id = int(ins + sid + did, 2)

        data = json_msg["b"]
        data_decoded = base64.b64decode(data)
        data_decoded_in_bytes = bytearray(data_decoded)

        can_msg = can.Message(
            arbitration_id=can_id,
            data=data_decoded_in_bytes,
            dlc=json_msg["l"],
            extended_id=True,
        )
        return can_msg

    #
    # Serial Methods
    #
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

        if self.__can_mode:
            self.__can_down()
        else:
            self.__ser.close()

    def __read_serial(self):
        """ Read serial message and put message to serial read queue
        """

        if self.__can_mode:
            # TODO: Recv all from the buffer and concat them in a string
            message_to_read = self.__can_recv()
            self._serial_read_q(message_to_read)
        else:
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
            if self.__can_mode:
                self.__can_send(message_to_write)
            else:
                self.__ser.write(message_to_write)
