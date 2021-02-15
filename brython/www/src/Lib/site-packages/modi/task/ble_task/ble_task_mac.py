import json
import base64
import asyncio
import time
from typing import Optional
from queue import Queue
from threading import Thread

from bleak import discover, BleakClient, BleakError
from bleak.backends.corebluetooth import client as mac_client

from modi.task.conn_task import ConnTask
from modi.util.connection_util import MODIConnectionError
from modi.util.miscellaneous import ask_modi_device


class BleTask(ConnTask):

    CHAR_UUID = '00008421-0000-1000-8000-00805f9b34fb'

    def __init__(self, verbose=False, uuid=None):
        super().__init__(verbose=verbose)
        print("Initiating ble_task connection...")
        self._loop = asyncio.get_event_loop()
        self.__uuid = uuid
        self._recv_q = Queue()
        self._send_q = Queue()
        self.__close_event = False
        self.__get_service = \
            mac_client.BleakClientCoreBluetooth.get_services
        mac_client.BleakClientCoreBluetooth.get_services = self.mac_get_service

    @staticmethod
    # The 'self' parameter of this function is necessary
    async def mac_get_service(client):
        return None

    async def _list_modi_devices(self):
        devices = await discover(timeout=1)
        modi_devies = []
        for d in devices:
            if 'MODI' in d.name:
                modi_devies.append(d)
        if not self.__uuid:
            self.__uuid = ask_modi_device(
                [d.name.upper() for d in modi_devies])
        for d in modi_devies:
            if self.__uuid in d.name.upper():
                return d
        return None

    async def __connect(self, address):
        client = BleakClient(address, timeout=1)
        await client.connect(timeout=1)
        await asyncio.sleep(1)
        await self.__get_service(client)
        return client

    def __run_loop(self):
        asyncio.set_event_loop(self._loop)
        tasks = asyncio.gather(self.__send_handler(), self.__watch_notify())
        self._loop.run_until_complete(tasks)

    async def __watch_notify(self):
        await self._bus.start_notify(self.CHAR_UUID, self.__recv_handler)
        while True:
            await asyncio.sleep(0.001)
            if self.__close_event:
                break

    async def __send_handler(self):
        while True:
            if self._send_q.empty():
                await asyncio.sleep(0.001)
            else:
                await self._bus.write_gatt_char(
                    self.CHAR_UUID, self._send_q.get()
                )
            if self.__close_event:
                break

    def __recv_handler(self, _, data):
        self._recv_q.put(self.__parse_ble_msg(data))

    def open_conn(self):
        loop = asyncio.get_event_loop()
        modi_device = loop.run_until_complete(self._list_modi_devices())
        if modi_device:
            self._bus = self._loop.run_until_complete(
                self.__connect(modi_device.address)
            )
            Thread(target=self.__run_loop, daemon=True).start()
            print(f"Connected to {modi_device.name}")
        else:
            raise MODIConnectionError(f"Network module of {self.__uuid}"
                                      f" not found!")

    async def __close_client(self):
        try:
            await self._bus.stop_notify(self.CHAR_UUID)
            await self._bus.disconnect()
        except BleakError:
            pass

    def close_conn(self):
        if self._bus:
            self.__close_event = True
            while self._loop.is_running():
                time.sleep(0.1)
            self._loop.run_until_complete(self.__close_client())

    def recv(self) -> Optional[str]:
        if self._recv_q.empty():
            return None
        json_pkt = self._recv_q.get()
        if self.verbose:
            print(f'recv: {json_pkt}')
        return json_pkt

    @ConnTask.wait
    def send(self, pkt: str) -> None:
        self._send_q.put(self.__compose_ble_msg(pkt))
        while not self._send_q.empty():
            time.sleep(0.01)
        if self.verbose:
            print(f'send: {pkt}')

    def send_nowait(self, pkt: str) -> None:
        self._send_q.put(self.__compose_ble_msg(pkt))
        if self.verbose:
            print(f'send: {pkt}')

    #
    # Non-Async Methods
    #
    def __parse_ble_msg(self, ble_msg):
        json_msg = dict()
        json_msg["c"] = ble_msg[1] << 8 | ble_msg[0]
        json_msg["s"] = ble_msg[3] << 8 | ble_msg[2]
        json_msg["d"] = int.from_bytes(ble_msg[4:6], byteorder='little')
        json_msg["b"] = base64.b64encode(ble_msg[8:]).decode("utf-8")
        json_msg["l"] = ble_msg[7] << 8 | ble_msg[6]
        return json.dumps(json_msg, separators=(",", ":"))

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
