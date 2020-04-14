import time

import pygatt

from binascii import hexlify
from pygatt.exceptions import NotConnectedError


class BleTask:
    def __init__(self):
        self.adapter = pygatt.GATTToolBackend()
        self.device = None

    def __del__(self):
        self.ble_down()

    def ble_up(self):
        self.adapter.start()

    def ble_down(self):
        self.adapter.stop()

    def connect(self, target_name, max_retries=3):
        target_addr = self.find_addr(target_name)

        while max_retries <= 3:
            print('Try connecting to target address:', target_addr)

            try:
                device = self.adapter.connect(address=target_addr, timeout=10)
            except NotConnectedError:
                max_retries -= 1
                continue
            break

        print('Successfully connected to the target device')
        self.device = device

    def find_addr(self, target_name, max_retries=5):
        """ Given target device name, find corresponding device address
        """

        target_addr = None
        while target_addr is None:
            if max_retries < 0:
                raise ValueError("Cannot connect to the target_device")

            scanned_devices = self.adapter.scan(run_as_root=True)

            for scanned_device in scanned_devices:
                device_name = scanned_device['name']
                device_addr = scanned_device['address']

                if device_name is None:
                    continue

                if device_name == target_name:
                    target_addr = device_addr
                    break

            max_retries -= 1

        return target_addr

    def subscribe(self, char_uuid):
        self.device.subscribe(char_uuid, callback=self.handle_data)

    def handle_data(self, handle, value):
        """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
        print("Received data: %s" % hexlify(value))


if __name__ == '__main__':
    bt = BleTask()
    bt.ble_up()

    target_name = 'MODI_1022889'
    bt.connect(target_name)

    # characteristic UUID
    CHAR_UUID = '00008421-0000-1000-8000-00805F9B34FB'
    bt.subscribe(CHAR_UUID)

    while True:
        time.sleep(1)
