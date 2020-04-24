import time
import json
import queue
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
        self.addr = loop.run_until_complete(
            self.get_target_device_addr("MODI_1022889")
        )
        print('target addr:', self.addr)

        self.loop = loop

    def run(self):
        self.loop.run_until_complete(self.communicate(self.addr, self.loop))
        time.sleep(5)

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
                await asyncio.sleep(0.01)

                try:
                    msg_to_send = self._ble_send_q.get_nowait().encode()
                except queue.Empty:
                    pass
                else:
                    ble_msg = self.__compose_ble_msg(msg_to_send)
                    await client.write_gatt_char(self.char_uuid, ble_msg)

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
