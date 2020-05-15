import os
import can
import time
import json
import queue
import base64

from modi._communicator_task import CommunicatorTask


class CanTask(CommunicatorTask):

    def __init__(self, can_recv_q, can_send_q):
        print("Run Can Task.")
        self._can_recv_q = can_recv_q
        self._can_send_q = can_send_q

        self.__can0 = None

    def __del__(self):
        self._close_conn()

    def __can_read(self):
        can_msg = self._read_data()
        json_msg = self.__parse_can_msg(can_msg)
        self._can_recv_q.put(json_msg)

    def __can_write(self):
        try:
            message_to_write = self._can_send_q.get_nowait().encode()
        except queue.Empty:
            pass
        else:
            self._write_data(message_to_write)

    #
    # Can Methods
    #
    def open_conn(self):
        os.system("sudo ip link set can0 type can bitrate 1000000")
        os.system("sudo ifconfig can0 up")

        self.__can0 = can.interface.Bus(
            channel="can0", bustype="socketcan_ctypes"
        )

    def _close_conn(self):
        os.system("sudo ifconfig can0 down")

    def _read_data(self, timeout=None):
        if self.__can0 is None:
            raise ValueError("Can is not initialized")

        can_msg = self.__can0.recv(timeout=timeout)
        if can_msg is None:
            raise ValueError("Can message not received!")
        return can_msg

    def _write_data(self, str_msg):
        """ Given parsed binary string message in json format,
            convert and send the message as CAN format
        """

        json_msg = json.loads(str_msg)
        can_msg = self.__compose_can_msg(json_msg)
        try:
            self.__can0.send(can_msg)
        except can.CanError:
            raise ValueError("Can message not sent!")

    def run_read_data(self, delay):
        while True:
            self.__can_read()
            time.sleep(delay)

    def run_write_data(self, delay):
        while True:
            self.__can_write()
            time.sleep(delay)

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
