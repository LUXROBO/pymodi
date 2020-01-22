# -*- coding: utf-8 -*-

"""Processes."""

from __future__ import absolute_import

import json
import time
import queue
import base64
import struct
import threading

from multiprocessing import Process, Queue, Event

from modi._serial_task import SerialTask
from modi._serial_parsing_task import ParserTask
from modi._json_excute_task import ExcutableTask


class MODIProcess(Process):
    def __init__(self):
        super(MODIProcess, self).__init__()


class SerialProcess(MODIProcess):
    def __init__(self, serial_read_q, serial_write_q, port):
        super(SerialProcess, self).__init__()
        self.__SerialTask = SerialTask(serial_read_q, serial_write_q, port)
        self.__stop = Event()

    def run(self):
        self.__SerialTask.open_serial()
        while not self.stopped():
            self.__SerialTask.start_thread()
        self.__SerialTask.close_serial()
        # print("SerProc terminates")

    def stop(self):
        self.__stop.set()

    def stopped(self):
        return self.__stop.is_set()


class ParserProcess(MODIProcess):
    def __init__(self, serial_read_q, recv_q):
        super(ParserProcess, self).__init__()
        self.__ParsingTask = ParserTask(serial_read_q, recv_q)
        self.__stop = Event()

    def run(self):
        while not self.stopped():
            self.__ParsingTask.start_thread()
        # print("ParProc terminates")

    def stop(self):
        self.__stop.set()

    def stopped(self):
        return self.__stop.is_set()


class ExecutableThread(threading.Thread):
    def __init__(self, serial_write_q, recv_q, ids, modules, cmd):
        super(ExecutableThread, self).__init__()
        self.__ExcutableTask = ExcutableTask(serial_write_q, recv_q, ids, modules, cmd)
        self.__stop = threading.Event()

    def run(self):
        while not self.stopped():
            self.__ExcutableTask.start_thread()
        # print("ExeThrd terminates")

    def stop(self):
        self.__stop.set()

    def stopped(self):
        return self.__stop.is_set()
