import os
import can
import time
import json
import queue
import base64

import serial.tools.list_ports as stl


class CanTask:

    def __init__(self, can_read_q, can_write_q):
        self.__can_mode = (
            self.__is_on_pi() and not self.__is_network_module_connected()
        )
        if self.__can_mode:
            self.__can_up()
            self.__can0 = can.interface.Bus(
                channel="can0", bustype="socketcan_ctypes"
            )
        else:
            raise Exception("Invalid Platform")

        self._can_read_q = can_read_q
        self._can_write_q = can_write_q

    def run(self):

        self.__can_read()
        self.__can_write()

        time.sleep(0.004)

    def run_read(self,stopped):
        """ Run serial task
        """

        while not stopped:
            self.__can_read()
            time.sleep(0.001)

        print('finish run_read')
        # TODO: Replace time.sleep below

    def run_write(self,stopped):
        """ Run write task
        """
        while not stopped:
            self.__can_write()
            time.sleep(0.001)

        print('finish run_write')

    def __del__(self):
        self.__can_down()

    def __can_read(self):
        can_msg = self.__can_recv()
        json_msg = self.__parse_can_msg(can_msg)
        self._can_read_q.put(json_msg)

    def __can_write(self):
        try:
            message_to_write = self._can_write_q.get_nowait().encode()
        except queue.Empty:
            pass
        else:
            self.__can_send(message_to_write)

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

    @staticmethod
    def __is_network_module_connected():
        return bool(CanTask.__list_modi_ports())

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

    #
    # Can helper methods
    #
    @staticmethod
    def __parse_can_msg(can_msg):
        """ Parse a can message to json format
        """
        can_id = can_msg.arbitration_id
        can_dlc = can_msg.dlc
        can_data = can_msg.data

        can_id_in_bin_str = format(can_id, "029b")
        c, s, d = CanTask.__parse_can_id(can_id_in_bin_str)

        json_msg = dict()
        json_msg["c"], json_msg["s"], json_msg["d"] = c, s, d
        json_msg["b"] = base64.b64encode(can_data).decode("utf-8")
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
