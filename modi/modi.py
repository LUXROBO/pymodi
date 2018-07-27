# -*- coding: utf-8 -*-

"""Main module."""

from __future__ import absolute_import

import serial
from modi.serial import list_ports
import modi._cmd as md_cmd
from modi._tasks import *

import sys
IS_PY2 = sys.version_info < (3, 0)

if IS_PY2:
    from Queue import Queue
else:
    from queue import Queue

class MODI:
    def __init__(self, port=None):
        self._recv_q = Queue()
        self._send_q = Queue()

        self._ids = dict()
        self._modules = list()

        if port == None:
            ports = list_ports()

            if len(ports) > 0:
                self._serial = serial.Serial(ports[0])
            else:
                raise RuntimeError("There is no MODI module.")

        else:
            self._serial = serial.Serial(port)

        self._threads = list()
        tasks = [ReadDataTask, ProcDataTask, WriteDataTask]

        for task in tasks:
            thread = task(self) 
            thread.daemon = True
            thread.start()
            self._threads.append(thread)
        
    def open(self):
        self._serial.open()

    def close(self):
        self._serial.close()

    def write(self, msg):
        self._send_q.put(msg)

    def pnp_on(self):
        for id in self._ids:
            self.write(md_cmd.module_state(id, md_cmd.ModuleState.RUN))

    def pnp_off(self, id=None):
        if id == None:
            for _id in self._ids:
                self.write(md_cmd.module_state(_id, md_cmd.ModuleState.PAUSE))
        else:
            self.write(md_cmd.module_state(id, md_cmd.ModuleState.PAUSE))

    @property
    def modules(self):
        return tuple(self._modules)

    @property
    def buttons(self):
        return tuple([x for x in self.modules if x.type == "button"])

    @property
    def dials(self):
        return tuple([x for x in self.modules if x.type == "dial"])

    @property
    def displays(self):
        return tuple([x for x in self.modules if x.type == "display"])

    @property
    def envs(self):
        return tuple([x for x in self.modules if x.type == "env"])

    @property
    def gyros(self):
        return tuple([x for x in self.modules if x.type == "gyro"])

    @property
    def irs(self):
        return tuple([x for x in self.modules if x.type == "ir"])

    @property
    def leds(self):
        return tuple([x for x in self.modules if x.type == "led"])

    @property
    def mics(self):
        return tuple([x for x in self.modules if x.type == "mic"])

    @property
    def motors(self):
        return tuple([x for x in self.modules if x.type == "motor"])

    @property
    def speakers(self):
        return tuple([x for x in self.modules if x.type == "speaker"])

    @property
    def ultrasonics(self):
        return tuple([x for x in self.modules if x.type == "ultrasonic"])

