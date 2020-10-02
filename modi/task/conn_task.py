import time

from abc import ABC
from abc import abstractmethod


class ConnTask(ABC):

    def __init__(self, verbose=False):
        self._bus = None
        self.verbose = verbose

    @property
    def bus(self):
        return self._bus

    @bus.setter
    def bus(self, new_bus):
        if not isinstance(new_bus, type(self._bus)):
            raise ValueError()
        else:
            self._bus = new_bus

    #
    # Abstract Methods
    #
    @abstractmethod
    def close_conn(self):
        pass

    @abstractmethod
    def open_conn(self):
        pass

    @abstractmethod
    def recv(self):
        pass

    @abstractmethod
    def send(self, pkt):
        pass

    @staticmethod
    def wait(func):
        def decorator(self, pkt):
            init_time = time.perf_counter()
            func(self, pkt)
            while time.perf_counter() - init_time < 0.04:
                pass
        return decorator
