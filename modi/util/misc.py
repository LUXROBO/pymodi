import time


class module_list(list):

    def __init__(self, src, module_type, lazy=True):
        self.__src = src
        self.__module_type = module_type
        self.__lazy = lazy
        super().__init__(self.sublist())

    def __getitem__(self, item):
        """ When accessing the module, the modules are sorted in an
        ascending order of
        1. the distance from network module
        2. left to right
        3. up to down

        :param item: Index of the module
        :return: Module
        """
        if self.__lazy:
            while not len(self.sublist()) > item:
                time.sleep(0.1)
        return self.sublist()[item]

    def get(self, module_id):
        for module in self.sublist():
            if module.id == module_id:
                return module
        raise Exception("Module with given id does not exits!!")

    def sublist(self):
        modules = [module for module in self.__src
                   if module.type == self.__module_type]
        modules.sort()
        return modules

    def find(self, module_id):
        for idx, module in enumerate(self.sublist()):
            if module_id == module.id:
                return idx
        return -1
