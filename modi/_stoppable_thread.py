# -*- coding: utf-8 -*-

"""Stoppable Thread module."""

from __future__ import absolute_import

from abc import *
import threading

class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__(target=self.run)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()
    
    @abstractmethod
    def run(self):
        pass