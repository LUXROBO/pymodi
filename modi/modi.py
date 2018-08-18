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
    """Main module.

    :param str port: MODI network module device name or ``None``.

    :raises SerialException: In case the device can not be found or can not be configured.

    The port is immediately opened on object creation, when a *port* is given. It is configured automatically when *port* is ``None`` and a successive call to :meth:`~modi.modi.MODI.open` is required.

    *port* is a device name: depending on operating system. e.g. ``/dev/ttyUSB0`` on GNU/Linux or ``COM3`` on Windows.

    Example:

    >>> import modi
    >>> bundle = modi.MODI()

    It can also be used with :meth:`modi.serial.list_ports`.

    >>> import modi
    >>> import modi.serial
    >>> ports = modi.serial.list_ports() # ['/dev/cu.usbmodem748BFFFEFFFF']
    >>> bundle = modi.MODI(ports[0])
    """
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
                raise serial.SerialException("No MODI network module connected.")

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
        """Open port.
        """
        self._serial.open()

    def close(self):
        """Close port immediately.
        """
        self._serial.close()

    def write(self, msg):
        """
        :param str msg: Data to send.
            
        Put the string to the sending data queue. This should be of type ``str``.
        """
        self._send_q.put(msg)

    def pnp_on(self, id=None):
        """Turn on PnP mode of the module.

        :param int id: The id of the module to turn on PnP mode or ``None``.

        All connected modules' PnP mode will be turned on if the `id` is ``None``.
        """
        if id == None:
            for _id in self._ids:
                self.write(md_cmd.module_state(_id, md_cmd.ModuleState.RUN))
        else:
            self.write(md_cmd.module_state(id, md_cmd.ModuleState.RUN))

    def pnp_off(self, id=None):
        """Turn off PnP mode of the module.

        :param int id: The id of the module to turn off PnP mode or ``None``.

        All connected modules' PnP mode will be turned off if the `id` is ``None``.
        """
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

