import os
import can
import time
import json

from queue import Empty
from base64 import b64decode, b64encode
from typing import Dict, Tuple
from modi.task.conn_task import ConnTask


class CanTask(ConnTask):

    _instances = set()

    def __init__(self, can_recv_q, can_send_q, verbose, port=None):
        print("Run Can Task.")
        if CanTask._instances:
            raise Exception("can0 device already in use")
        self._can_recv_q = can_recv_q
        self._can_send_q = can_send_q
        self._instances.add(self)
        self.__can0 = None
        self.__verbose = verbose
        if self.__verbose:
            print('PyMODI log...\n==================================')

    def __del__(self):
        self._close_conn()

    @property
    def can0(self):
        return self.__can0

    @can0.setter
    def can0(self, can_port):
        self.__can0 = can_port

    def __can_recv(self) -> None:
        """Reads data through CAN and put it on recv_q

        :return: None
        """
        can_msg = self._recv_data()
        if not can_msg:
            time.sleep(0.01)
        else:
            json_msg = self.__parse_can_msg(can_msg)
            self._can_recv_q.put(json_msg)
            if self.__verbose:
                print(f'recv: {json_msg}')

    def __can_send(self) -> None:
        """Write data through CAN

        :return: None
        """
        try:
            message_to_send = self._can_send_q.get_nowait().encode()
        except Empty:
            time.sleep(0.01)
        else:
            self._send_data(message_to_send)
            if self.__verbose:
                print(f'send: {message_to_send.decode("utf8")}')

    #
    # Can Methods
    #
    def open_conn(self) -> None:
        """Open connection through CAN

        :return: None
        """
        os.system("sudo ip link set can0 type can bitrate 1000000")
        os.system("sudo ifconfig can0 up")

        self.__can0 = can.interface.Bus(
            channel="can0", bustype="socketcan_ctypes"
        )

    def _close_conn(self) -> None:
        """Close connection through CAN

        :return: None
        """
        os.system("sudo ifconfig can0 down")

    def _recv_data(self, timeout: float = 0.01) -> can.Message:
        """Read data from CAN and returns CAN message

        :param timeout: timeout value
        :type timeout: float, optional
        :raises: ValueError: CAN is not initialized or message is not received
        :return: CAN message received
        :rtype: can.Message
        """
        if self.__can0 is None:
            raise ValueError("Can is not initialized")

        can_msg = self.__can0.recv(timeout=timeout)
        return can_msg

    def _send_data(self, str_msg: str) -> None:
        """ Given parsed binary string message in json format,
            convert and send the message as CAN format

        :param str_msg: json serialized string message
        :type str_msg: str
        :return: None
        """

        json_msg = json.loads(str_msg)
        can_msg = self.__compose_can_msg(json_msg)
        try:
            self.__can0.send(can_msg)
        except can.CanError:
            print("Can connection is lost, please check your modules")

    def run_recv_data(self, delay: float) -> None:
        """Read the data and wait a given time

        :param delay: time value to wait in seconds
        :type delay: float
        :return: None
        """
        while True:
            self.__can_recv()

    def run_send_data(self, delay: float) -> None:
        """Write the data and wait a given time

        :param delay: time value to wait in seconds
        :type delay: float
        :return: None
        """
        while True:
            self.__can_send()

    #
    # Can helper methods
    #
    @staticmethod
    def __parse_can_msg(can_msg: can.Message) -> str:
        """Parse a can message to json format

        :param can_msg: CAN message received
        :type can_msg: can.Message
        :return: json serialized string message
        :rtype: str
        """
        can_id = can_msg.arbitration_id
        can_dlc = can_msg.dlc
        can_data = can_msg.data

        can_id_in_bin_str = format(can_id, "029b")
        c, s, d = CanTask.__parse_can_id(can_id_in_bin_str)

        json_msg = dict()
        json_msg["c"], json_msg["s"], json_msg["d"] = c, s, d
        json_msg["b"] = b64encode(can_data).decode("utf-8")
        json_msg["l"] = can_dlc
        return json.dumps(json_msg, separators=(",", ":"))

    @staticmethod
    def __parse_can_id(can_id: str) -> Tuple[int, int, int]:
        """ Parse a 29 bits length Can ID into INS, SID and DID

        :param can_id: 29 bits string CAN ID
        :type can_id: str
        :return: INS, SID, DID
        :rtype: Tuple[int, int, int]
        """
        BIN = 2
        SID_BEGIN_IDX = 5
        DID_BEGIN_IDX = 17

        ins = int(can_id[:SID_BEGIN_IDX], BIN)
        sid = int(can_id[SID_BEGIN_IDX:DID_BEGIN_IDX], BIN)
        did = int(can_id[DID_BEGIN_IDX:], BIN)
        return ins, sid, did

    @staticmethod
    def __compose_can_msg(json_msg: Dict[str, str]) -> can.Message:
        """Returns CAN message from a dictionary format message

        :param json_msg: Dictionary format json message
        :type json_msg: Dictionary
        :return: Composed Can message
        :rtype: can.Message
        """
        ins = format(json_msg["c"], '05b')
        sid = format(json_msg["s"], '012b')
        did = format(json_msg["d"], '012b')
        can_id = int(ins + sid + did, 2)

        data = json_msg["b"]
        data_decoded = b64decode(data)
        data_decoded_in_bytes = bytearray(data_decoded)

        can_msg = can.Message(
            arbitration_id=can_id,
            data=data_decoded_in_bytes,
            dlc=json_msg["l"],
            extended_id=True,
        )
        return can_msg
