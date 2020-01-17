# -*- coding: utf-8 -*-

"""Stoppable Thread module."""

from __future__ import absolute_import

from abc import *
import threading
import multiprocessing

class StoppableProc(multiprocessing.Process):
    def __init__(self):
        super(StoppableProc, self).__init__(target=self.run)
        self._stop = multiprocessing.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()
    
    @abstractmethod
    def run(self):
        pass