
# TODO: virtual modules have been detached as `virtual-modi` package
from modi.virtual_module.virtual_network import VirtualNetwork


class VirBus:

    def __init__(self):
        self._virtual_network = None

    def open(self):
        self._virtual_network = VirtualNetwork()
        self._virtual_network.open()

    def close(self):
        self._virtual_network.close()
        self._virtual_network = None

    def write(self, msg):
        # Pass the message to virtual network module, a virtual bundle
        self._virtual_network.recv(msg)

    def read_all(self):
        # TODO: read all stacked messages from network module
        json_buffer = None
        return json_buffer
