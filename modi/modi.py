# -*- coding: utf-8 -*-

"""Main module."""

from __future__ import absolute_import

import os
import time
import serial

from modi._processes import SerialProcess, ParserProcess, ExecutableThread
from modi._command import Command
from modi.module import (
    button,
    dial,
    display,
    env,
    gyro,
    ir,
    led,
    mic,
    motor,
    network,
    speaker,
    ultrasonic,
)

from multiprocessing import Process, Queue


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
        self._serial_read_q = Queue(100)
        self._serial_write_q = Queue(100)
        self._recv_q = Queue(100)
        self._send_q = Queue(100)

        self._src_ids = dict()
        self._modules = list()
        self._command = Command()

        self._ser_proc = SerialProcess(self._serial_read_q, self._serial_write_q, port)
        self._ser_proc.daemon = True
        self._ser_proc.start()

        self._par_proc = ParserProcess(self._serial_read_q, self._recv_q)
        self._par_proc.daemon = True
        self._par_proc.start()

        self._exe_thrd = ExecutableThread(
            self._serial_write_q,
            self._recv_q,
            self._src_ids,
            self._modules,
            self._command,
        )
        self._exe_thrd.daemon = True
        self._exe_thrd.start()

        self.__init_modules()

    def __init_modules(self):
        BROADCAST_ID = 0xFFF

        msg_to_send = self._command.set_module_state(
            BROADCAST_ID, self._command.ModuleState.REBOOT, self._command.ModulePnp.OFF
        )
        self._serial_write_q.put(msg_to_send)
        self.__delay()

        msg_to_send = self._command.set_module_state(
            BROADCAST_ID, self._command.ModuleState.RUN, self._command.ModulePnp.OFF
        )
        self._serial_write_q.put(msg_to_send)
        self.__delay()

        msg_to_send = self._command.request_uuid(BROADCAST_ID)
        self._serial_write_q.put(msg_to_send)
        self.__delay()

    def __delay(self):
        time.sleep(1)

    def exit(self):
        self._ser_proc.stop()
        self._par_proc.stop()
        self._exe_thrd.stop()

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
        return tuple(
            [module for module in self.modules if module.module_type == "button"]
        )

    @property
    def dials(self):
        """Tuple of connected :class:`~modi.module.dial.Dial` modules.
        """
        return tuple(
            [module for module in self.modules if module.module_type == "dial"]
        )

    @property
    def displays(self):
        """Tuple of connected :class:`~modi.module.display.Display` modules.
        """
        return tuple(
            [module for module in self.modules if module.module_type == "display"]
        )

    @property
    def envs(self):
        """Tuple of connected :class:`~modi.module.env.Env` modules.
        """
        return tuple([module for module in self.modules if module.module_type == "env"])

    @property
    def gyros(self):
        """Tuple of connected :class:`~modi.module.gyro.Gyro` modules.
        """
        return tuple(
            [module for module in self.modules if module.module_type == "gyro"]
        )

    @property
    def irs(self):
        """Tuple of connected :class:`~modi.module.ir.Ir` modules.
        """
        return tuple([module for module in self.modules if module.module_type == "ir"])

    @property
    def leds(self):
        """Tuple of connected :class:`~modi.module.led.Led` modules.
        """
        return tuple([module for module in self.modules if module.module_type == "led"])

    @property
    def mics(self):
        """Tuple of connected :class:`~modi.module.mic.Mic` modules.
        """
        return tuple([module for module in self.modules if module.module_type == "mic"])

    @property
    def motors(self):
        """Tuple of connected :class:`~modi.module.motor.Motor` modules.
        """
        return tuple(
            [module for module in self.modules if module.module_type == "motor"]
        )

    @property
    def speakers(self):
        """Tuple of connected :class:`~modi.module.speaker.Speaker` modules.
        """
        return tuple(
            [module for module in self.modules if module.module_type == "speaker"]
        )

    @property
    def ultrasonics(self):
        """Tuple of connected :class:`~modi.module.ultrasonic.Ultrasonic` modules.
        """
        return tuple(
            [module for module in self.modules if module.module_type == "ultrasonic"]
        )
