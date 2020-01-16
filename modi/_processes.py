# -*- coding: utf-8 -*-

"""Processes."""

from __future__ import absolute_import

import modi._cmd as md_cmd 
from modi.serial import list_ports
import serial
from modi.module import *
import modi._util as md_util

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

class MODIProcess(multiprocessing.Process):
    def __init__(self):
        super(MODIProcess, self).__init__()

# SerialProcess
# Run SerialTask

class SerialProcess(MODIProcess):
    
    def __init__(self, serial_read_q, serial_write_q, port):
        super(SerialProcess, self).__init__()
        self._SerialTask = SerialTask(serial_read_q, serial_write_q, port)
        
        # self.dostuff = DoStuff(self)
    def run(self):
        if os.name == 'nt':
            self._SerialTask.start_thread()

# ParsingProcess
# Run ParseTask

class ParsingProcess(MODIProcess):

    def __init__(self, serial_read_q, recv_q, json_box):
        super(ParsingProcess,self).__init__()
        self._ParsingTask = ParsingTask(serial_read_q, recv_q, json_box)
    
    def run(self):
        if os.name == 'nt':
            self._ParsingTask.start_thread()

class ExcuteProcess(MODIProcess):

    def __init__(self, serial_write_q, recv_q, ids, modules):
        super(ExcuteProcess,self).__init__()
        self._ExcuteTask = ExcuteTask(serial_write_q, recv_q, ids, modules)

    def run(self):
        if os.name == 'nt':
            self._ExcuteTask.start_thread()