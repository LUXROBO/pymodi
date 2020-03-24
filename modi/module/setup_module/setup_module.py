from modi.module.module import Module


class SetupModule(Module):
    def __init__(self, id_, uuid, can_write_q):
        super(SetupModule, self).__init__(id_, uuid, can_write_q)
