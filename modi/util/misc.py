import time

from modi.module.input_module.button import Button
from modi.module.input_module.dial import Dial
from modi.module.input_module.env import Env
from modi.module.input_module.gyro import Gyro
from modi.module.input_module.ir import Ir
from modi.module.input_module.mic import Mic
from modi.module.input_module.ultrasonic import Ultrasonic

from modi.module.output_module.display import Display
from modi.module.output_module.led import Led
from modi.module.output_module.motor import Motor
from modi.module.output_module.speaker import Speaker

from modi.module.setup_module.network import Network


def get_type_from_uuid(uuid):
    if uuid is None:
        return 'Network'

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
    return 'Network' if module_type is None else module_type


def get_module_from_name(module_type: str):
    """ Find module type for module initialize

    :param module_type: Type of the module in string
    :type module_type: str
    :return: Module corresponding to the type
    :rtype: Module
    """
    module = {
        "button": Button,
        "dial": Dial,
        "display": Display,
        "env": Env,
        "gyro": Gyro,
        "ir": Ir,
        "led": Led,
        "mic": Mic,
        "motor": Motor,
        "speaker": Speaker,
        "ultrasonic": Ultrasonic,
        "Network": Network,
    }.get(module_type)
    return module


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
