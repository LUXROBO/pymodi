import time


class module_list(list):

    def __init__(self, src, module_type, lazy=True):
        self.__src = src
        self.__module_type = module_type
        self.__lazy = lazy
        super().__init__(self.sublist())

    def __getitem__(self, item):
        if self.__lazy:
            while not len(self.sublist()) > item:
                time.sleep(0.1)
            return self.sublist()[item]
        else:
            return super().__getitem__(item)

    def get(self, module_id):
        for module in self.sublist():
            if module.id == module_id:
                return module
        raise Exception("Module with given id does not exits!!")

    def sublist(self):
        return [module for module in self.__src
                if module.type == self.__module_type]
