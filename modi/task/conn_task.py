import time
from abc import ABC
from abc import abstractmethod
from typing import Optional


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
    def recv(self) -> Optional[str]:
        pass

    @abstractmethod
    def send(self, pkt: str) -> None:
        pass

    @staticmethod
    def wait(func):
        """Wait decorator
        Make sure this is attached to inherited send method
        """
        def decorator(self, pkt: str) -> None:
            init_time = time.perf_counter()
            func(self, pkt)
            while time.perf_counter() - init_time < 0.04:
                pass
        return decorator
