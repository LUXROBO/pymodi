from abc import ABC
from abc import abstractmethod


class ConnTask(ABC):

    def __init__(self):
        self.__bus = None

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
    def recv_data(self):
        pass

    @abstractmethod
    def send_data(self):
        pass
