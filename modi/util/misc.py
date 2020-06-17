import time


class module_list(list):

    def __init__(self, src, module_type):
        super().__init__(src)
        self.__src = src
        self.__module_type = module_type

    def __getitem__(self, item):
        sublist = [module for module in self.__src
                   if module.type == self.__module_type]
        while not len(sublist) > item:
            sublist = [module for module in self.__src
                       if module.type == self.__module_type]
            time.sleep(0.1)
        return sublist[item]
