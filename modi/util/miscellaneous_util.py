from importlib.util import find_spec


def get_module_type_from_uuid(uuid):
    hexadecimal = hex(uuid).lstrip("0x")
    type_indicator = str(hexadecimal)[:4]
    module_type = {
        # Input modules
        '2000': 'env',
        '2010': 'gyro',
        '2020': 'mic',
        '2030': 'button',
        '2040': 'dial',
        '2050': 'ultrasonic',
        '2060': 'ir',

        # Output modules
        '4000': 'display',
        '4010': 'motor',
        '4020': 'led',
        '4030': 'speaker',
    }.get(type_indicator)
    return 'network' if module_type is None else module_type


def get_module_from_name(module_type: str):
    """ Find module type for module initialize

    :param module_type: Type of the module in string
    :type module_type: str
    :return: Module corresponding to the type
    :rtype: Module
    """
    module_type = module_type[0].lower() + module_type[1:]
    module_name = module_type[0].upper() + module_type[1:]
    module_module = find_spec(f'modi.module.input_module.{module_type}')
    if not module_module:
        module_module = find_spec(f'modi.module.output_module.{module_type}')
    if not module_module:
        module_module = find_spec(f'modi.module.setup_module.{module_type}')
    module_module = module_module.loader.load_module(module_module.name)
    return getattr(module_module, module_name)


def ask_modi_device(devices):
    for idx, dev in enumerate(devices):
        print(f"<{idx}>: {dev}")
    i = input("Choose your device index (ex: 0) : ")
    return devices[int(i)].lstrip('MODI_')


class ModuleList(list):

    def __init__(self, src, module_type=None):
        self.__src = src
        self.__module_type = module_type
        super().__init__(self.sublist())

    def __len__(self):
        return len(self.sublist())

    def __eq__(self, other):
        return super().__eq__(other)

    def get(self, module_id):
        for module in self.sublist():
            if module.id == module_id:
                return module
        raise Exception("Module with given id does not exits!!")

    def sublist(self):
        """ When accessing the module, the modules are sorted in an
        ascending order of
        1. the distance from network module
        2. left to right
        3. up to down

        :return: Module
        """
        if self.__module_type:
            modules = list(
                filter(
                    lambda module: module.module_type == self.__module_type,
                    self.__src
                )
            )
        else:
            modules = self.__src
        modules.sort()
        return modules

    def find(self, module_id):
        for idx, module in enumerate(self.sublist()):
            if module_id == module.id:
                return idx
        return -1


class MockConn:
    def __init__(self):
        self.send_list = []

    def send(self, pkt):
        self.send_list.append(pkt)

    def recv(self):
        return 'Test'
