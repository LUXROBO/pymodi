import os
import json
import queue
import base64
from typing import Optional

import pygatt

from modi.task.conn_task import ConnTask


class BleTaskPi(ConnTask):
    CHAR_UUID = "00008421-0000-1000-8000-00805f9b34fb"

    def __init__(self, verbose=False, uuid=None):
        super().__init__(verbose=verbose)
        self.__adapter = pygatt.GATTToolBackend()
        self._bus = None
        self._recv_q = queue.Queue()
        self.__uuid = uuid

    @property
    def bus(self):
        return self._bus

    def __find_modi_device(self):
        self.__adapter.reset()
        devices = self.__adapter.scan(run_as_root=True, timeout=1)
        modi_devices = []
        for d in devices:
            if d['name'] and 'MODI' in d['name']:
                modi_devices.append(d)
        if self.__uuid:
            for d in modi_devices:
                if self.__uuid in d['name']:
                    return d
            return None
        else:
            return modi_devices[0]

    def open_conn(self):
        os.system("sudo hciconfig hci0 down")
        os.system("sudo hciconfig hci0 up")
        self.__adapter.start()
        modi_device = self.__find_modi_device()
        self._bus = self.__adapter.connect(modi_device['address'])
        self._bus.subscribe(self.CHAR_UUID, callback=self.__ble_read)

    def close_conn(self):
        # Reboot modules to stop receiving channel messages
        self.send('{"c":9,"s":0,"d":4095,"b":"Bgg=","l":2}')
        self.__adapter.stop()
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

    @ConnTask.wait
    def send(self, pkt: str) -> None:
        json_msg = json.loads(pkt)
        ble_msg = self.__compose_ble_msg(json_msg)
        if self.verbose:
            print(f"send: {json_msg}")
        self._bus.char_write(self.CHAR_UUID, ble_msg, wait_for_response=False)

    def send_nowait(self, pkt: str) -> None:
        json_msg = json.loads(pkt)
        ble_msg = self.__compose_ble_msg(json_msg)
        if self.verbose:
            print(f"send: {json_msg}")
        self._bus.char_write(self.CHAR_UUID, ble_msg, wait_for_response=False)

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
