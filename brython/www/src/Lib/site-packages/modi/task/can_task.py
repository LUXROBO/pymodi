import json
import os
from base64 import b64decode, b64encode
from typing import Dict, Tuple, Optional

import can

from modi.task.conn_task import ConnTask
from modi.util.connection_util import MODIConnectionError


class CanTask(ConnTask):

    _instances = set()

    def __init__(self, verbose=False):
        super().__init__(verbose)
        print("Initiating can connection...")
        if CanTask._instances:
            raise Exception("can0 device already in use")
        self._instances.add(self)

    #
    # Inherited Methods
    #
    def open_conn(self) -> None:
        """Open connection through CAN

        :return: None
        """
        os.system("sudo ip link set can0 type can bitrate 1000000")
        os.system("sudo ifconfig can0 up")

        self._bus = can.interface.Bus(
            channel="can0", bustype="socketcan_ctypes"
        )

    def close_conn(self) -> None:
        """Close connection through CAN

        :return: None
        """
        os.system("sudo ifconfig can0 down")
        CanTask._instances.clear()

    def recv(self) -> Optional[str]:
        """Read json msg from CAN

        :return: json pkt
        :rtype: str
        """
        if self._bus is None:
            raise MODIConnectionError("Can is not initialized")

        can_msg = self._bus.recv(timeout=0.01)
        if not can_msg:
            return None
        else:
            json_msg = self.__parse_can_msg(can_msg)
            if self.verbose:
                print(f'recv: {json_msg}')
            return json_msg

    @ConnTask.wait
    def send(self, pkt: str) -> None:
        """Send json pkt through can

        :param pkt: Json pkt
        :type pkt: str
        :return: None
        """
        json_msg = json.loads(pkt)
        can_msg = self.compose_can_msg(json_msg)
        try:
            self._bus.send(can_msg)
        except can.CanError:
            print("Can connection is lost, please check your modules")
        if self.verbose:
            print(f'send: {pkt}')

    def send_nowait(self, pkt: str) -> None:
        """Send json pkt through can

        :param pkt: Json pkt
        :type pkt: str
        :return: None
        """
        json_msg = json.loads(pkt)
        can_msg = self.compose_can_msg(json_msg)
        try:
            self._bus.send(can_msg)
        except can.CanError:
            print("Can connection is lost, please check your modules")
        if self.verbose:
            print(f'send: {pkt}')

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
    def compose_can_msg(json_msg: Dict[str, str]) -> can.Message:
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
