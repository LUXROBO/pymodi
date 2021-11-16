
import time

from queue import Queue
from threading import Thread

from websocket_server import WebsocketServer

from modi.task.conn_task import ConnTask



class SocTask(ConnTask):

    def __init__(self, verbose=False, port=None):
        super().__init__(verbose=verbose)
        print('Initiating soc_task connection...')
        self._bus = WebsocketServer(host='localhost', port=8765)
        self._recv_q = Queue()
        self._send_q = Queue()
        self.__close_event = False

    def open_conn(self):
        Thread(target=self.__open, daemon=True).start()
        Thread(target=self.__send_handler, daemon=True).start()
    
    def close_conn(self):
        self.__close_event = True
        self._bus.shutdown_gracefully()

    def recv(self):
        if self._recv_q.empty():
            return None
        json_pkt = self._recv_q.get()
        if self.verbose:
            print(f'recv: {json_pkt}')
        return json_pkt

    @ConnTask.wait
    def send(self, pkt):
        self._send_q.put(pkt.encode())
        while not self._send_q.empty():
            time.sleep(0.01)
        if self.verbose:
            print(f'send: {pkt}')

    def send_nowait(self, pkt: str) -> None:
        self._send_q.put(pkt.encode())
        if self.verbose:
            print(f'send: {pkt}')

    #
    # Async Methods
    #
    def __open(self):
        def new_client(client, server):
            server.send_message_to_all(
                f'Hey all, a new client:{client} has joined us'
            )
        def client_left(client, server):
            server.send_message_to_all(
                f'Hey all, a client:{client} has left us'
            )

        # Set callback functions
        self._bus.set_fn_new_client(new_client)
        self._bus.set_fn_message_received(self.__recv_handler)
        self._bus.set_fn_client_left(client_left)

        # Run the server forever
        self._bus.run_forever()

    def __recv_handler(self, client, server, message):
        self._recv_q.put(message)

    def __send_handler(self):
        while not self.__close_event:
            if self._send_q.empty():
                time.sleep(0.001)
                continue
            try:
                message = self._send_q.get()
                self._bus.send_message_to_all(message)
            except Exception:
                self.__close_event = True