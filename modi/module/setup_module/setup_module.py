from modi.module.module import Module


class SetupModule(Module):
    def __init__(self, id_, uuid, serial_write_q):
        super(SetupModule, self).__init__(id_, uuid, serial_write_q)
        self._category = "setup"
