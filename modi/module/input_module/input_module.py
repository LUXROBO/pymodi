from modi.module.module import Module


class InputModule(Module):
    def __init__(self, id_, uuid, msg_send_q):
        super(InputModule, self).__init__(id_, uuid, msg_send_q)
