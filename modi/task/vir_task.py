
from modi.task.conn_task import ConnTask

from virtual_modi import VirtualBundle


class VirTask(ConnTask):

    def __init__(self, verbose=False):
        print("Initiating virtual connection...")
        super().__init__(verbose)
        self.__json_buffer = b''

    class VirBus:

        def __init__(self):
            self._virtual_bundle = None

        def open(self):
            # VirtualBundle asynchronously generates MODI json messages
            self._virtual_bundle = VirtualBundle()
            self._virtual_bundle.open()

        def close(self):
            self._virtual_bundle.close()
            self._virtual_bundle = None

        def write(self, msg):
            # Pass the message to virtual interface, a virtual bundle
            self._virtual_bundle.recv(msg)

        def read(self):
            # Flush all stacked messages from the virtual bundle interface
            return self._virtual_bundle.send()

    #
    # Inherited Methods
    #
    def open_conn(self):
        # Init and open connection via virtual bus, VirBus
        self._bus = self.VirBus()
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
