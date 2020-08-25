import json
import base64
from os import path
from typing import Optional

import clr
from modi.task.conn_task import ConnTask
from modi.util.conn_util import MODIConnectionError


class BleTaskWindows(ConnTask):

    def __init__(self, verbose=False, uuid=None):
        clr.AddReference(f'{path.dirname(__file__)}/backend/BleTaskWin')
        super().__init__(verbose=verbose)
        from BleTaskWin import BleTask
        self.__ble_task = BleTask(verbose=verbose, uuis=uuid)

    def open_conn(self):
        print("Connecting...", end='')
        for i in range(5):
            try:
                self.__ble_task.open_conn()
                print()
                return
            except Exception:
                print("...", end='')
        raise MODIConnectionError("BLE Connection Failed!")

    def close_conn(self):
        self.__ble_task.close_conn()

    def recv(self) -> Optional[str]:
        return self.__ble_task.recv()

    @ConnTask.wait
    def send(self, pkt: str) -> None:
        return self.__ble_task.send(self.__compose_ble_msg(pkt))

    def send_nowait(self, pkt: str) -> None:
        return self.__ble_task.send(self.__compose_ble_msg(pkt))

    def __compose_ble_msg(self, json_msg):
        ble_msg = bytearray(16)
        json_msg = json.loads(json_msg)
        ins = json_msg["c"]
        sid = json_msg["s"]
        did = json_msg["d"]
        dlc = json_msg["l"]
        data = json_msg["b"]

        ble_msg[0] = ins & 0xFF
        ble_msg[1] = ins >> 8 & 0xFF
        ble_msg[2] = sid & 0xFF
        ble_msg[3] = sid >> 8 & 0xFF
        ble_msg[4] = did & 0xFF
        ble_msg[5] = did >> 8 & 0xFF
        ble_msg[6] = dlc & 0xFF
        ble_msg[7] = dlc >> 8 & 0xFF

        ble_msg[8:8 + dlc] = bytearray(base64.b64decode(data))

        return ble_msg
