
from modi.task.conn_task import ConnTask

from virtual_modi import VirtualBundle


class VirTask(ConnTask):

    def __init__(self, verbose=False, virtual_modules=None):
        print("Initiating virtual connection...")
        super().__init__(verbose)
        self.__virtual_modules = virtual_modules
        self.__json_buffer = b''

    class VirBus:
        """
        This wraps a virtual bundle object, where both are the interface for
        PyMODI and VirtualMODI respectively.
        """

        def __init__(self, virtual_modules=None):
            self._virtual_bundle = None
            self._virtual_modules = virtual_modules

        def open(self):
            # VirtualBundle asynchronously generates MODI json messages
            self._virtual_bundle = VirtualBundle(modules=self._virtual_modules)
            self._virtual_bundle.open()

        def close(self):
            # All running threads (mostly for read and write) are terminated
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
        self._bus = self.VirBus(virtual_modules=self.__virtual_modules)
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
