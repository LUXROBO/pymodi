import os
import json
import queue
import base64
from typing import Optional

import pygatt

from modi.task.conn_task import ConnTask


class BleTask(ConnTask):
    char_uuid = "00008421-0000-1000-8000-00805F9B34FB"

    def __init__(self, verbose=False, uuid=""):
        super().__init__(verbose=verbose)
        self.uuid = uuid
        self.adapter = pygatt.GATTToolBackend()
        self.device = None
        self._recv_q = queue.Queue()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_conn()

    def _list_modi_devices(self):
        self.adapter.reset()
        devices = self.adapter.scan(run_as_root=True, timeout=2)
        return [module for module in devices
                if module['name'] and 'MODI' in module['name']]

    def open_conn(self):
        os.system("sudo hciconfig hci0 up")
        self.adapter.start()
        print('Searching for MODI device')
        devices = self._list_modi_devices()
        if not devices:
            raise ValueError('No MODI device found!')
        modi_device = None
        if not self.uuid:
            modi_device = devices[0]
        else:
            for d in devices:
                if self.uuid in d['name']:
                    modi_device = d
                    break
            if not modi_device:
                raise ValueError('MODI with given uuid does not exist!')
        print(f'Found {modi_device["name"]}')
        self.device = self.adapter.connect(modi_device['address'])
        self.device.subscribe(self.char_uuid, callback=self.__ble_read)
        print('Connection Complete')

    def close_conn(self):
        # Reboot modules to stop receiving channel messages
        self.send('{"c":9,"s":0,"d":4095,"b":"Bgg=","l":2}')
        self.adapter.stop()
        os.system("sudo hciconfig hci0 down")

    def __ble_read(self, _, value):
        """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
        json_msg = self.__parse_ble_msg(value)
        if self.verbose:
            print(f"recv: {json_msg}")
        self._recv_q.put(json_msg)

    def send(self, pkt: str) -> None:
        json_msg = json.loads(pkt)
        ble_msg = self.__compose_ble_msg(json_msg)
        self.device.char_write(self.char_uuid, ble_msg)

    def recv(self) -> Optional[str]:
        if self._recv_q.empty():
            return None
        return self._recv_q.get()

    #
    # Ble Helper Methods
    #
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

    def __parse_ble_msg(self, ble_msg):
        json_msg = dict()
        json_msg["c"] = ble_msg[1] << 8 | ble_msg[0]
        json_msg["s"] = ble_msg[3] << 8 | ble_msg[2]
        json_msg["d"] = ble_msg[5] << 8 | ble_msg[4]
        json_msg["l"] = ble_msg[7] << 8 | ble_msg[6]
        json_msg["b"] = base64.b64encode(ble_msg[8:]).decode("utf-8")
        return json.dumps(json_msg, separators=(",", ":"))
