import json
import queue
import base64
import asyncio

from bleak import discover
from bleak import BleakClient

from modi.task.conn_task import ConnTask
from modi.util.conn_util import MODIConnectionError


class BleTask(ConnTask):

    def __init__(self, verbose=False, uuid=None):
        super().__init__(verbose=verbose)
        self._loop = asyncio.get_event_loop()
        self.__uuid = uuid

    async def _list_modi_devices(self):
        devices = await discover(timeout=2)
        modi_devies = []
        for d in devices:
            if 'MODI' in d.name:
                print(f'Found MODI device of uuid {d.name.lstrip("MODI_")}')
                modi_devies.append(d)
        if not self.__uuid:
            return modi_devies[0]
        else:
            for d in modi_devies:
                if self.__uuid in d.name:
                    return d
            return None

    def open_conn(self):
        print("Searching for MODI network module...")
        modi_device = self._loop.run_until_complete(self._list_modi_devices())
        if modi_device:
            print(f"Connected to {modi_device.name}")
            self._bus = modi_device
        else:
            raise MODIConnectionError(f"Network module of {self.__uuid}"
                                      f" not found!")

    #
    # Non-Async Methods
    #
    def __parse_ble_msg(self, ble_msg):
        json_msg = dict()
        json_msg["c"] = ble_msg[1] << 8 | ble_msg[0]
        json_msg["s"] = ble_msg[3] << 8 | ble_msg[2]
        json_msg["d"] = ble_msg[5] << 8 | ble_msg[4]
        json_msg["b"] = base64.b64encode(ble_msg[8:]).decode("utf-8")
        json_msg["l"] = ble_msg[7] << 8 | ble_msg[6]
        return json.dumps(json_msg, separators=(",", ":"))

    def __compose_ble_msg(self, json_msg):
        ble_msg = bytearray(16)

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

        ble_msg[8:8+dlc] = bytearray(base64.b64decode(data))

        return ble_msg
