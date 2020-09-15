import json
import base64
from os import path
from typing import Optional

import clr

from modi.task.conn_task import ConnTask
from modi.util.conn_util import MODIConnectionError
from modi.util.misc import ask_modi_device


class BleTask(ConnTask):

    def __init__(self, verbose=False, uuid=None):
        print("Initiating ble connection...")
        clr.AddReference(f'{path.dirname(__file__)}/BleTaskWin')
        super().__init__(verbose=verbose)
        from BleTaskWin import BleTask
        self.__ble_task = BleTask(verbose=verbose, uuid=uuid)

    def open_conn(self):
        if not self.__ble_task.uuid:
            devices = self.__ble_task.list_modi_devices()
            self.__ble_task.uuid = ask_modi_device(devices)

        print("Connecting...")
        for _ in range(5):
            try:
                self.__ble_task.open_conn()
                return
            except Exception:
                print("...")
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
