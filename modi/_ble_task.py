import time
import json
import queue
import base64
import pygatt

from pygatt.exceptions import NotConnectedError

from modi._communicator_task import CommunicatorTask


class BleTask:

    def __init__(self, ble_recv_q, ble_send_q):
        self._ble_recv_q = ble_recv_q
        self._ble_send_q = ble_send_q

        self.adapter = pygatt.GATTToolBackend()
        self.device = None

    def __del__(self):
        self.ble_down()

    def ble_up(self):
        self.adapter.start()

    def ble_down(self):
        self.adapter.stop()

    def ble_write(self, char_uuid):
        while True:
            time.sleep(0.01)
            try:
                message_to_write = self._ble_send_q.get_nowait().encode()
            except queue.Empty:
                pass
            else:
                self._write_data(message_to_write, char_uuid)
    
    def _write_data(self, str_msg, char_uuid):
        json_msg = json.loads(str_msg)
        ble_msg = self.__compose_ble_msg(json_msg)

        try:
            self.device.char_write(char_uuid, ble_msg)
        # TODO: Raise explicit exception
        except:
            raise ValueError("Ble message not sent!")
    
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
        self.device.subscribe(char_uuid, callback=self.recv_data)

    def recv_data(self, handle, value):
        """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """

        json_msg = dict()
        json_msg["c"] = value[1] << 8 | value[0]
        json_msg["s"] = value[3] << 8 | value[2]
        json_msg["d"] = value[5] << 8 | value[4]
        json_msg["l"] = value[7] << 8 | value[6]
        json_msg["b"] = base64.b64encode(value[8:]).decode("utf-8")

        json_res = json.dumps(json_msg, separators=(",", ":"))
        self._ble_recv_q.put(json_res)
