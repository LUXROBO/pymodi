from modi.module.module import Module


class SetupModule(Module):
    def __init__(self, module_id, module_uuid, modi):
        super(SetupModule, self).__init__(module_id, module_uuid, modi)
        self._category = "setup"
