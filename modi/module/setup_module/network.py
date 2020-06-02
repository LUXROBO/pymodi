"""Network module."""

from enum import IntEnum

from modi.module.setup_module.setup_module import SetupModule


class Network(SetupModule):
    class PropertyType(IntEnum):
        RESERVED = 0

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)
