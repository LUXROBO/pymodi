import time
import os
import json
import queue
import base64
import pexpect

from typing import Optional
from threading import Thread

from modi.task.conn_task import ConnTask
from modi.util.miscellaneous import ask_modi_device


class BleTask(ConnTask):

    def __init__(self, verbose=False, uuid=None):
        print("Initiating ble_task connection...")
        script = os.path.join(os.path.dirname(__file__), 'change_interval.sh')
        os.system(f'chmod 777 {script}')
        os.system(f'sudo {script}')
        super().__init__(verbose=verbose)
        self._bus = None
        self.__uuid = uuid
        self._recv_q = queue.Queue()
        self.__close_event = False

    @property
    def bus(self):
        return self._bus

    def __find_modi_device(self):
        scanner = pexpect.spawn('sudo hcitool lescan')
        init_time = time.time()
        devices = []
        while time.time() - init_time < 1:
            info = scanner.readline()
            info = info.decode().split()
            if 'MODI' in info[1] and info[1] not in (d[1] for d in devices):
                devices.append(info)
        scanner.terminate()
        if not self.__uuid:
            self.__uuid = ask_modi_device([d[1].upper() for d in devices])
        for info in devices:
            if self.__uuid.upper() in info[1].upper():
                return info
        raise ValueError('MODI network module does not exist!')

    def __reset(self):
        os.system('sudo hciconfig hci0 down')
        os.system('sudo hciconfig hci0 up')

    def open_conn(self):
        self.__reset()
        modi_device = self.__find_modi_device()
        print(f'Connecting to {modi_device[1]}...')
        self.__reset()
        self._bus = pexpect.spawn('gatttool -I')
        self._bus.expect('LE')
        for _ in range(5):
            try:
                self._bus.sendline(f'connect {modi_device[0]}')
                self._bus.expect('Connection successful', timeout=1)
                Thread(daemon=True, target=self.__ble_read).start()
                break
            except Exception:
                print('...')

    def close_conn(self):
        # Reboot modules to stop receiving channel messages
        self.__close_event = True
        self.send('{"c":9,"s":0,"d":4095,"b":"Bgg=","l":2}')
        time.sleep(0.5)
        self._bus.sendline('disconnect')
        self._bus.terminate()
        os.system("sudo hciconfig hci0 down")

    def __ble_read(self):
        """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
        while True:
            try:
                self._bus.expect('value: .*?\r', timeout=0.5)
            except Exception:
                continue
            msg = self._bus.after.decode().lstrip('value: ').split()
            json_msg = self.__parse_ble_msg(
                bytearray([int(b, 16) for b in msg]))
            if self.verbose:
                print(f"recv: {json_msg}")
            self._recv_q.put(json_msg)
            if self.__close_event:
                break
            time.sleep(0.002)

    @ConnTask.wait
    def send(self, pkt: str) -> None:
        self.send_nowait(pkt)

    def send_nowait(self, pkt: str) -> None:
        json_msg = json.loads(pkt)
        ble_msg = self.__compose_ble_msg(json_msg)
        if self.verbose:
            print(f"send: {json_msg}")
        self._bus.sendline(f'char-write-cmd 0x002a {ble_msg}')

    def recv(self) -> Optional[str]:
        if self._recv_q.empty():
            return None
        return self._recv_q.get()

    #
    # Ble Helper Methods
    #
    @staticmethod
    def __compose_ble_msg(json_msg):
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

        ble_msg[8:8 + dlc] = bytearray(base64.b64decode(data))
        data = ""
        for b in ble_msg:
            data += f'{b:02X}'
        return data

    @staticmethod
    def __parse_ble_msg(ble_msg):
        json_msg = dict()
        json_msg["c"] = ble_msg[1] << 8 | ble_msg[0]
        json_msg["s"] = ble_msg[3] << 8 | ble_msg[2]
        json_msg["d"] = ble_msg[5] << 8 | ble_msg[4]
        json_msg["l"] = ble_msg[7] << 8 | ble_msg[6]
        json_msg["b"] = base64.b64encode(ble_msg[8:]).decode("utf-8")
        return json.dumps(json_msg, separators=(",", ":"))
