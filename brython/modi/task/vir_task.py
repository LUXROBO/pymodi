
import socket

from modi.task.conn_task import ConnTask


class VirTask(ConnTask):

    def __init__(self, verbose=False, port=12345):
        print("Initiating virtual connection...")
        super().__init__(verbose)
        self._bus = self.VirBus(serv_info=('127.0.0.1', port))
        self.__json_buffer = b''

    class VirBus:
        """
        This wraps a virtual bundle object, where both are the interface for
        PyMODI and VirtualMODI respectively.
        """

        RECV_BUFF_SIZE = 1024

        def __init__(self, serv_info=('127.0.0.1', 12345)):
            # VirtualBundle asynchronously generates MODI messages
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.serv_host, self.serv_port = serv_info

        def open(self):
            # Open client, PyMODI Side
            self._s.connect((self.serv_host, self.serv_port))

        def close(self):
            # Close client, PyMODI Side
            self._s.close()

        def write(self, msg):
            # Pass the outgoing message to virtual bundle
            self._s.sendall(msg)

        def read(self):
            # Flush all stacked messages from the virtual bundle
            return self._s.recv(self.RECV_BUFF_SIZE)

        def __read_all(self):
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
