
import socket

from modi.task.conn_task import ConnTask


class WebTask(ConnTask):

    def __init__(self, verbose=False):
        print("Initiating web-usb connection...")
        super().__init__(verbose)
        self.__json_buffer = b''

    #
    # WebBus (TCP Client) inner class
    #
    class WebBus:

        def __init__(self):
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def open(self):
            host = socket.gethostbyname()
            port = 3571
            self.s.connect((host, port))

        def close(self):
            self.s.close()

        def read(self):
            return self.s.recv(1024)

        def write(self, pkt):
            self.s.sendall(pkt)

    #
    # Inherited Methods
    #
    def open_conn(self):
        self._bus = self.WebBus()
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
