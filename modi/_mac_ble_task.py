import time
import asyncio

from bleak import discover
from bleak import BleakScanner
from bleak import BleakClient


class MacBleTask:
    char_uuid = "00008421-0000-1000-8000-00805F9B34FB"

    def __init__(self, ble_recv_q, ble_send_q):
        self._ble_recv_q = ble_recv_q
        self._ble_send_q = ble_send_q

        self.loop = asyncio.get_event_loop()
        addr = self.loop.run_until_complete(
            self.get_target_device_addr("MODI_1022889")
        )

        self.client = self.loop.run_until_complete(
            self.connect_to_client(addr, self.loop)
        )

        asyncio.gather(
            self.recv_ble_data(addr, self.loop),
            self.send_ble_data(addr, self.loop),
        )

    def __del__(self):
        self.loop.run_until_complete(self.client.disconnect())
        self.loop.close()
    
    async def connect_to_client(self, addr, loop):
        client = await BleakClient(addr, loop=loop)
        await client.connect()
        return client

    #
    # Async Methods
    #
    async def get_target_device_addr(self, target_device_name):
        # TODO: Use BleakScanner.discover() later
        devices = await discover()
        for d in devices:
            if 'uuids' in d.metadata:
                device_info = d.__str__()
                device_addr, device_name = device_info.split()
                if target_device_name == device_name:
                    return device_addr[:-1]
    
    async def recv_ble_data(self, device_addr, loop):
        await self.client.start_notify(self.char_uuid, self.notification_handler)

        while True:
            await asyncio.sleep(0.5, loop=loop)
        #await client.stop_notify(self.char_uuid)

    async def send_ble_data(self, device_addr, loop):

        while True:
            await self.client.write_gatt_char(self.char_uuid, None)
            await asyncio.sleep(0.01)

    #
    # Non-Async Methods
    #
    def notification_handler(self, _, data):
        print(data)
