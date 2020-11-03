
import socket

import threading as th

from modi.task.conn_task import ConnTask

from virtual_modi import VirtualBundle


class VirTask(ConnTask):

    def __init__(self, verbose=False, virtual_modules=None, modi_version=1):
        print("Initiating virtual connection...")
        super().__init__(verbose)
        self._bus = self.VirBus(
            virtual_modules=virtual_modules, modi_version=modi_version
        )
        self.__json_buffer = b''

    class VirBus:
        """
        This wraps a virtual bundle object, where both are the interface for
        PyMODI and VirtualMODI respectively.
        """

        HOST = '127.0.0.1'
        PORT = 12345
        RECV_BUFF_SIZE = 1024

        def __init__(self, virtual_modules=None, modi_version=1):
            # VirtualBundle asynchronously generates MODI messages
            self._virtual_bundle = VirtualBundle(
                conn_type='tcp',
                modi_version=modi_version,
                modules=virtual_modules
            )
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def open(self):
            # Open server, VirtualMODI
            th.Thread(target=self._virtual_bundle.open, daemon=True).start()

            # Open client, PyMODI Side
            self._s.connect((self.HOST, self.PORT))

        def close(self):
            # Close server, VirtualMODI
            self._virtual_bundle.close()

            # Close client, PyMODI Side
            self._s.close()

        def write(self, msg):
            # Pass the outgoing message to virtual bundle
            self._s.sendall(msg)

        def read(self):
            # Flush all stacked messages from the virtual bundle
            return self._s.recv(self.RECV_BUFF_SIZE)

        def __recvall(self):
            data = bytearray()
            while True:
                packet = self._s.recv(self.RECV_BUFF_SIZE)
                if not packet:
                    break
                data.extend(packet)
            return data

    #
    # Inherited Methods
    #
    def open_conn(self):
        self._bus.open()

    def close_conn(self):
        self._bus.close()

    @ConnTask.wait
    def send(self, pkt):
        self._bus.write(pkt.encode('utf8'))
        if self.verbose:
            print(f'send: {pkt}')

    def send_nowait(self, pkt):
        self._bus.write(pkt.encode('utf8'))
        if self.verbose:
            print(f'send: {pkt}')

    def recv(self):
        self.__json_buffer += self._bus.read()
        idx = self.__json_buffer.find(b'{')
        if idx < 0:
            self.__json_buffer = b''
            return None
        self.__json_buffer = self.__json_buffer[idx:]
        idx = self.__json_buffer.find(b'}')
        if idx < 0:
            return None
        json_pkt = self.__json_buffer[:idx + 1].decode('utf8')
        self.__json_buffer = self.__json_buffer[idx + 1:]
        if self.verbose:
            print(f'recv: {json_pkt}')
        return json_pkt
