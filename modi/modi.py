# -*- coding: utf-8 -*-

"""Main module."""

from __future__ import absolute_import

import serial
import time
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
    """
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
    >>> ports = modi.serial.list_ports() # [<serial.tools.list_ports_common.ListPortInfo object at 0x1026e95c0>]
    >>> bundle = modi.MODI(ports[0].device)
    """
    def __init__(self, port=None):
        self._recv_q = Queue()
        self._send_q = Queue()

        self._ids = dict()
        self._modules = list()

        if port == None:
            ports = list_ports()

            if len(ports) > 0:
                self._serial = serial.Serial(ports[0].device)
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
        
        time.sleep(1)
        
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
        """Tuple of connected modules except network module.

        Example:

        >>> bundle = modi.MODI()
        >>> modules = bundle.modules # (<modi.module.button.Button object at 0x1009455c0>, <modi.module.led.Led object at 0x100945630>)
        """
        return tuple(self._modules)

    @property
    def buttons(self):
        """Tuple of connected :class:`~modi.module.button.Button` modules.
        """
        return tuple([x for x in self.modules if x.type == "button"])

    @property
    def dials(self):
        """Tuple of connected :class:`~modi.module.dial.Dial` modules.
        """
        return tuple([x for x in self.modules if x.type == "dial"])

    @property
    def displays(self):
        """Tuple of connected :class:`~modi.module.display.Display` modules.
        """
        return tuple([x for x in self.modules if x.type == "display"])

    @property
    def envs(self):
        """Tuple of connected :class:`~modi.module.env.Env` modules.
        """
        return tuple([x for x in self.modules if x.type == "env"])

    @property
    def gyros(self):
        """Tuple of connected :class:`~modi.module.gyro.Gyro` modules.
        """
        return tuple([x for x in self.modules if x.type == "gyro"])

    @property
    def irs(self):
        """Tuple of connected :class:`~modi.module.ir.Ir` modules.
        """
        return tuple([x for x in self.modules if x.type == "ir"])

    @property
    def leds(self):
        """Tuple of connected :class:`~modi.module.led.Led` modules.
        """
        return tuple([x for x in self.modules if x.type == "led"])

    @property
    def mics(self):
        """Tuple of connected :class:`~modi.module.mic.Mic` modules.
        """
        return tuple([x for x in self.modules if x.type == "mic"])

    @property
    def motors(self):
        """Tuple of connected :class:`~modi.module.motor.Motor` modules.
        """
        return tuple([x for x in self.modules if x.type == "motor"])

    @property
    def speakers(self):
        """Tuple of connected :class:`~modi.module.speaker.Speaker` modules.
        """
        return tuple([x for x in self.modules if x.type == "speaker"])

    @property
    def ultrasonics(self):
        """Tuple of connected :class:`~modi.module.ultrasonic.Ultrasonic` modules.
        """
        return tuple([x for x in self.modules if x.type == "ultrasonic"])

