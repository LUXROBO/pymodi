"""Network module."""

from enum import Enum

from modi.module.setup_module.setup_module import SetupModule


class Network(SetupModule):
    class PropertyType(Enum):
        RESERVED = 0

    def __init__(self, module_id, uuid, modi):
        super(Network, self).__init__(module_id, uuid, modi)
        self._type = "network"
