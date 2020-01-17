# -*- coding: utf-8 -*-

"""Main module."""

from __future__ import absolute_import

import serial
import time
from modi.serial import list_ports
from modi._json_box import JsonBox
import modi._cmd as md_cmd

# from modi._tasks import *
from modi._serial_task import *
from modi._serial_parsing_task import *
from modi._json_excute_task import *

from modi._processes import *
from modi.module import *

import sys
import os

IS_PY2 = sys.version_info < (3, 0)
# if IS_PY2:
#    from Queue import Queue
# else:
#    from queue import Queue

import multiprocessing
from multiprocessing import Process, Queue, Pipe, Manager, Lock
from multiprocessing.managers import BaseManager

import queue


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
        print("os.getpid():", os.getpid())
        # self._manager = multiprocessing.Manager()

        self._serial_read_q = multiprocessing.Queue(200)
        self._serial_write_q = multiprocessing.Queue(200)
        self._recv_q = multiprocessing.Queue(100)
        self._send_q = multiprocessing.Queue(100)
        self._display_send_q = multiprocessing.Queue(200)
        # sharable?
        self._json_box = JsonBox()
        self._ids = dict()  # _ids -> _module_ids
        self._modules = list()

        print("Serial Process Start")
        self._serialp = SerialProcess(self._serial_read_q, self._serial_write_q, port)
        self._serialp.daemon = True
        self._serialp.start()
        # _serialp -> _serial_proc

        print("Parsing Process Start")
        self._parsingp = ParsingProcess(
            self._serial_read_q, self._recv_q, self._json_box
        )
        self._parsingp.daemon = True
        self._parsingp.start()
        # _parsingp -> _paresing_proc

        print("Excute Process Start")
        self._excutep = ExcuteProcess(
            self._serial_write_q, self._recv_q, self._ids, self._modules
        )
        self._excutep.daemon = True
        self._excutep.start()
        # _ExcuteProcess -> _ExcuteTask
        # _excutep -> _excute_task

        modi_serialtemp = md_cmd.module_state(
            0xFFF, md_cmd.ModuleState.REBOOT, md_cmd.ModulePnp.OFF
        )
        self._serial_write_q.put(modi_serialtemp)
        time.sleep(1)
        modi_serialtemp = md_cmd.module_state(
            0xFFF, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.OFF
        )
        self._serial_write_q.put(modi_serialtemp)
        time.sleep(1)
        modi_serialtemp = md_cmd.request_uuid(0xFFF)
        self._serial_write_q.put(modi_serialtemp)
        time.sleep(1)
        # 함수로 변경, -> _init_modules

    def write(self, msg, is_display=False):
        """
        :param str msg: Data to send.
            
        Put the string to the sending data queue. This should be of type ``str``.
        """
        if is_display:
            self._display_send_q.put(msg)
        else:
            self._send_q.put(msg)

    def end(self):
        # end -> exit
        print("You are now leaving the Python sector.")
        self._serialp.stop()
        self._parsingp.stop()
        self._excutep.stop()

        os._exit(0)

    # methods below are getters
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

    def __delattr__(self, name):
        return super().__delattr__(name)

