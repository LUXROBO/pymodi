from modi.module.module import Module

class InputModule(Module):
    def __init__(self, module_id, module_uuid, modi, serial_write_q):
        super(InputModule, self).__init__(module_id, module_uuid, modi, serial_write_q)
        self._category = "input"

