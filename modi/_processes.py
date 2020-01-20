# -*- coding: utf-8 -*-

"""Processes."""

from __future__ import absolute_import

import multiprocessing
from multiprocessing import Process, Queue
import threading

import json
import time
import base64
import struct
import queue

from modi._serial_task import SerialTask
from modi._serial_parsing_task import ParsingTask
from modi._json_excute_task import ExcuteTask


class MODIProcess(multiprocessing.Process):
    def __init__(self):
        super(MODIProcess, self).__init__()


class SerialProcess(MODIProcess):
    def __init__(self, serial_read_q, serial_write_q, port):
        super(SerialProcess, self).__init__()
        self._SerialTask = SerialTask(serial_read_q, serial_write_q, port)
        self._stop = multiprocessing.Event()

    def run(self):
        self._SerialTask.connect_serial()
        while not self.stopped():
            self._SerialTask.start_thread()
        self._SerialTask.disconnect_serial()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()


class ParsingProcess(MODIProcess):
    def __init__(self, serial_read_q, recv_q):
        super(ParsingProcess, self).__init__()
        self._ParsingTask = ParsingTask(serial_read_q, recv_q)
        self._stop = multiprocessing.Event()

    def run(self):
        while not self.stopped():
            self._ParsingTask.start_thread()
        print("Parsing Process End")

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()


class ExeThread(threading.Thread):
    def __init__(self, serial_write_q, recv_q, ids, modules, cmd):
        super(ExeThread, self).__init__()
        self._ExcuteTask = ExcuteTask(serial_write_q, recv_q, ids, modules, cmd)
        self._stop = threading.Event()

    def run(self):
        while not self.stopped():
            self._ExcuteTask.start_thread()
        print("Excute Process End")

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
