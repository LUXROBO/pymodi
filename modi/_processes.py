# -*- coding: utf-8 -*-

"""Processes."""

from __future__ import absolute_import

import modi._cmd as md_cmd
from modi.serial import list_ports
import serial
from modi.module import *
import modi._util as md_util

# from modi._stoppable_thread import StoppableThread

import json
import weakref
import time
import base64
import struct
import multiprocessing
import os
import threading
import queue

from multiprocessing import Process, Queue
from modi._tasks import *
import atexit


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
        print("Serial Process End")

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()


class ParsingProcess(MODIProcess):
    def __init__(self, serial_read_q, recv_q, json_box):
        super(ParsingProcess, self).__init__()
        self._ParsingTask = ParsingTask(serial_read_q, recv_q, json_box)
        self._stop = multiprocessing.Event()

    def run(self):
        while not self.stopped():
            self._ParsingTask.start_thread()
        print("Parsing Process End")

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()


class ExcuteProcess(threading.Thread):
    def __init__(self, serial_write_q, recv_q, ids, modules):
        super(ExcuteProcess, self).__init__()
        self._ExcuteTask = ExcuteTask(serial_write_q, recv_q, ids, modules)
        self._stop = threading.Event()

    def run(self):
        while not self.stopped():
            self._ExcuteTask.start_thread()
        print("Excute Process End")

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

