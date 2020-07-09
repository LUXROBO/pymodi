from abc import ABC
from abc import abstractmethod


class ConnTask(ABC):

    def __init__(self, recv_q, send_q):
        self._recv_q = recv_q
        self._send_q = send_q

    #
    # Abstract Methods
    #
    @abstractmethod
    def _close_conn(self):
        pass

    @abstractmethod
    def _recv_data(self):
        pass

    @abstractmethod
    def _send_data(self):
        pass

    @abstractmethod
    def open_conn(self):
        pass

    @abstractmethod
    def run_recv_data(self, delay: float):
        pass

    @abstractmethod
    def run_send_data(self, delay: float):
        pass
