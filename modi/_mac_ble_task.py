import time
import json
import base64
import asyncio

from bleak import discover
from bleak import BleakScanner
from bleak import BleakClient


class MacBleTask:
    char_uuid = "00008421-0000-1000-8000-00805F9B34FB"

    def __init__(self, ble_recv_q, ble_send_q):
        self._ble_recv_q = ble_recv_q
        self._ble_send_q = ble_send_q

        loop = asyncio.get_event_loop()
        addr = loop.run_until_complete(
            self.get_target_device_addr("MODI_1022889")
        )
        print('target addr:', addr)

        loop.run_until_complete(self.communicate(addr, loop))

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
   
    async def communicate(self, device_addr, loop):
        """ Start communicate with MODI HW via BLE Conneciton
        """

        async with BleakClient(device_addr, loop=loop) as client:
            await client.start_notify(self.char_uuid, self.notification_handler)

            while True:
                #await client.write_gatt_char(self.char_uuid, None)
                await asyncio.sleep(0.01)

    #
    # Non-Async Methods
    #
    def notification_handler(self, _, data):
        json_msg = self.__parse_ble_msg(bytearray(data))
        self._ble_recv_q.put(json_msg)

    def __parse_ble_msg(self, ble_msg):
        json_msg = dict()
        json_msg["c"] = ble_msg[1] << 8 | ble_msg[0]
        json_msg["s"] = ble_msg[3] << 8 | ble_msg[2]
        json_msg["d"] = ble_msg[5] << 8 | ble_msg[4]
        json_msg["b"] = base64.b64encode(ble_msg[8:]).decode("utf-8")
        json_msg["l"] = ble_msg[7] << 8 | ble_msg[6]
        return json.dumps(json_msg, separators=(",", ":"))
