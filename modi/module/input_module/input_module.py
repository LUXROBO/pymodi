from modi.module.module import Module


class InputModule(Module):
    def __init__(self, id_, uuid, msg_send_q, property_types):
        super().__init__(id_, uuid, msg_send_q, property_types)
