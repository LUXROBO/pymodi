
import time
import asyncio
from queue import Queue
from websockets import serve

from modi.task.conn_task import ConnTask


class SocTask(ConnTask):

    def __init__(self, verbose=False):
        super().__init__(verbose=verbose)
        print('Initiating soc_task connection...')
        self._recv_q = Queue()
        self._send_q = Queue()
        self.__close_event = False

    def open_conn(self):
        asyncio.run(self.__main())

    def close_conn(self):
        while self._loop.is_running():
            time.sleep(0.1)
        self._loop.run_until_complete(self.__close())

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
    async def __main(self):
        await asyncio.gather(
            self.__open(), self.__send_handler()
        )

    async def __open(self):
        async with serve(self.__recv_handler, 'localhost', 8765):
            await asyncio.Future()

    async def __close(self):
        try:
            await self._bus.disconnect()
        except Exception:
            self.__close_event = True

    async def __recv_handler(self, websocket):
        self._bus = websocket
        while not self.__close_event:
            try:
                message = await self._bus.recv()
                self._recv_q.put(message)
            except Exception:
                self.__close_event = True

    async def __send_handler(self):
        while not self.__close_event:
            if self._send_q.empty():
                await asyncio.sleep(0.001)
                continue
            try:
                await self._bus.send(self._send_q.get())
            except Exception:
                self.__close_event = True
