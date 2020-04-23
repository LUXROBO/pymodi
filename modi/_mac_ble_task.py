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

    def __del__(self):
        self.loop.close()

    #
    # Async methods
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
    
    async def read_ble_data(self, device_addr, loop):
        async with BleakClient(device_addr, loop=loop) as client:
            conn_stat = await client.is_connected()
            if not conn_stat:
                raise Exception("Cannot connect to:", device_addr)
            print("Successfully established the BLE connection")

            await client.start_notify(self.char_uuid, self.notification_handler)

            # TODO: Change while-condition
            while await client.is_connected():
                await asyncio.sleep(0.5, loop=loop)
            await client.stop_notify(self.char_uuid)

    #
    # Non-async methods
    #
    def notification_handler(self, _, data):
        print(data)

