
from modi.task.conn_task import ConnTask
from modi.util.vir_bus import VirBus


class VirTask(ConnTask):

    def __init__(self, verbose=False):
        print("Initiating virtual connection...")
        super().__init__(verbose)
        self.__json_buffer = b''

    #
    # Inherited Methods
    #
    def open_conn(self):
        # Init and open connection via virtual bus, VirBus
        self._bus = VirBus()
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
        self.__json_buffer += self._bus.read_all()
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
