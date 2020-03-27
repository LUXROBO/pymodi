
import os

import serial.tools.list_ports as stl

from abc import ABC
from abc import abstractmethod


class CommunicatorTask(ABC):

    def __init__(self, read_q, write_q):
        self._read_q = read_q
        self._write_q = write_q

    #
    # Abstract Methods
    #
    @abstractmethod
    def _open_conn(self):
        pass

    @abstractmethod
    def _close_conn(self):
        pass

    @abstractmethod
    def _read_data(self):
        pass

    @abstractmethod
    def _write_data(self):
        pass

    @abstractmethod
    def run_read_data(self, delay):
        pass

    @abstractmethod
    def run_write_data(self, delay):
        pass
