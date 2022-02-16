import sys
import json
import time
import base64
import asyncio as aio
import nest_asyncio as nest_aio

from typing import Optional
from queue import Queue
from threading import Thread

from bleak import BleakClient, BleakError, BleakScanner

from modi.task.conn_task import ConnTask
from modi.util.connection_util import MODIConnectionError


nest_aio.apply()


class BleTask(ConnTask):
    CHAR_UUID = '00008421-0000-1000-8000-00805f9b34fb'

    def __init__(self, verbose=False, uuid=None):
        super().__init__(verbose=verbose)
        self.modi_name = f'MODI_{uuid.upper()}'
        print(f'Initiating ble_task connection with {self.modi_name}')
        self._loop = aio.get_event_loop()
        self._recv_q = Queue()
        self._send_q = Queue()
        self.__close_event = False

        if sys.platform == 'darwin':
            from bleak.backends.corebluetooth import client as mac_client
            self.__get_service = \
                mac_client.BleakClientCoreBluetooth.get_services
            mac_client.BleakClientCoreBluetooth.get_services = \
                self.mac_get_service

    @staticmethod
    async def mac_get_service(client):
        return None

    def match_device(self, device, _):
        return device.name == self.modi_name

    async def __connect(self, address):
        client = BleakClient(
            address, disconnected_callback=self.handle_disconnected, timeout=2
        )
        await client.connect(timeout=2)
        await aio.sleep(1)
        if sys.platform == 'darwin':
            await self.__get_service(client)
        return client

    def __run_loop(self):
        aio.set_event_loop(self._loop)
        tasks = aio.gather(self.__send_handler(), self.__watch_notify())
        self._loop.run_until_complete(tasks)

    async def __watch_notify(self):
        await self._bus.start_notify(self.CHAR_UUID, self.__recv_handler)
        while True:
            await aio.sleep(0.001)
            if self.__close_event:
                break

    async def __send_handler(self):
        while True:
            if self._send_q.empty():
                await aio.sleep(0.001)
            else:
                try:
                    await self._bus.write_gatt_char(
                        self.CHAR_UUID, self._send_q.get()
                    )
                except BleakError:
                    self.__close_event = True
            if self.__close_event:
                break

    def __recv_handler(self, _, data):
        self._recv_q.put(self.__parse_ble_msg(data))

    def open_conn(self):
        loop = aio.get_event_loop()
        modi_device = loop.run_until_complete(
            BleakScanner.find_device_by_filter(self.match_device)
        )
        if modi_device:
            self._bus = self._loop.run_until_complete(
                self.__connect(modi_device.address)
            )
            Thread(target=self.__run_loop, daemon=True).start()
            print(f"Connected to {modi_device.name}")
        else:
            raise MODIConnectionError(
                f"Network module of {self.modi_name} not found!"
                'Perhaps, the module is already paired with your device?'
            )

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
            self._loop.close()

    def handle_disconnected(self, _):
        print('Device is being properly disconnected...')

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
