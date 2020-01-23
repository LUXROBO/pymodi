# -*- coding: utf-8 -*-

"""Main MODI module."""

import os
import time
import json
import base64

from modi._serial_process import SerialProcess
from modi._parser_process import ParserProcess
from modi._executor_thread import ExecutorThread

from modi.module.module import Module
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

import multiprocessing


class MODI:
    """
    Example:

    >>> import modi
    >>> bundle = modi.MODI()
    """

    def __init__(self):
        self._serial_read_q = multiprocessing.Queue(100)
        self._serial_write_q = multiprocessing.Queue(100)
        self._json_recv_q = multiprocessing.Queue(100)

        self._modules = list()
        self._module_ids = dict()

        self._ser_proc = SerialProcess(self._serial_read_q, self._serial_write_q)
        self._ser_proc.daemon = True
        self._ser_proc.start()

        self._par_proc = ParserProcess(self._serial_read_q, self._json_recv_q)
        self._par_proc.daemon = True
        self._par_proc.start()

        self._exe_thrd = ExecutorThread(
            self._serial_write_q, self._json_recv_q, self._module_ids, self._modules
        )
        self._exe_thrd.daemon = True
        self._exe_thrd.start()

        # TODO: receive flag from executor thread
        time.sleep(5)

    def exit(self):
        """ Stop modi instance
        """

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
