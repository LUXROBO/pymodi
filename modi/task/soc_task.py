

from websocket import create_connection

from modi.task.conn_task import ConnTask


class SocTask(ConnTask):
    """
    SocTask implements a websocket client.
    Thus, PyMODI works as a websocket client, listening to a MODI Client.
    However, it's possible for PyMODI client to connect to a MODI relay server.
    A connection between a server and a client must be one-to-one.
    """

    def __init__(self, verbose=False, port=None):
        super().__init__(verbose=verbose)
        print('Initiating soc_task connection...')
        DEFAULT_SOC_PORT = 8765
        self.port = port if port else DEFAULT_SOC_PORT

    def open_conn(self):
        self._bus = create_connection(f'ws://localhost:{self.port}')

    def close_conn(self):
        self._bus.close()

    def recv(self):
        json_pkt = self._bus.recv()
        if self.verbose:
            print(f'recv: {json_pkt}')
        return json_pkt

    @ConnTask.wait
    def send(self, pkt):
        self._bus.send(pkt.encode())
        if self.verbose:
            print(f'send: {pkt}')

    def send_nowait(self, pkt):
        self._bus.send(pkt.encode())
        if self.verbose:
            print(f'send: {pkt}')
