"""Main MODI module."""

import time

import multiprocessing as mp

from pprint import pprint

from modi._serial_process import SerialProcess
from modi._parser_process import ParserProcess
from modi._executor_thread import ExecutorThread

from modi.module.input_module.button import Button
from modi.module.input_module.dial import Dial
from modi.module.input_module.env import Env
from modi.module.input_module.gyro import Gyro
from modi.module.input_module.ir import Ir
from modi.module.input_module.mic import Mic
from modi.module.input_module.ultrasonic import Ultrasonic

from modi.module.output_module.display import Display
from modi.module.output_module.led import Led
from modi.module.output_module.motor import Motor
from modi.module.output_module.speaker import Speaker


class MODI:
    """
    Example:
    >>> import modi
    >>> bundle = modi.MODI()
    """

    def __init__(self, test=False):
        self._modules = list()
        self._module_ids = dict()
        self._topology_data = dict()

        self._serial_read_q = mp.Queue()
        self._serial_write_q = mp.Queue()
        self._json_recv_q = mp.Queue()

        self._ser_proc = None
        self._par_proc = None
        self._exe_thrd = None

        if not test:
            self._ser_proc = SerialProcess(
                self._serial_read_q, self._serial_write_q,)
            self._ser_proc.daemon = True
            self._ser_proc.start()
            time.sleep(1)

            self._par_proc = ParserProcess(
                self._serial_read_q, self._json_recv_q,)
            self._par_proc.daemon = True
            self._par_proc.start()
            time.sleep(1)

            self._exe_thrd = ExecutorThread(
                self._modules,
                self._module_ids,
                self._topology_data,
                self._serial_write_q,
                self._json_recv_q,
            )
            self._exe_thrd.daemon = True
            self._exe_thrd.start()
            time.sleep(1)

            # TODO: receive flag from executor thread
            time.sleep(5)

    def exit(self):
        """ Stop modi instance
        """

        self._ser_proc.stop()
        self._par_proc.stop()
        self._exe_thrd.stop()
        time.sleep(1)

    def print_ids(self):
        """ Print each module type and its id
        """
        for module in self.modules:
            pprint('module: {}, module_id: {}'.format(module, module.id))

    @property
    def modules(self):
        """Tuple of connected modules except network module.
        Example:
        >>> bundle = modi.MODI()
        >>> modules = bundle.modules
        """

        return tuple(self._modules)

    @property
    def buttons(self):
        """Tuple of connected :class:`~modi.module.button.Button` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Button)])

    @property
    def dials(self):
        """Tuple of connected :class:`~modi.module.dial.Dial` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Dial)])

    @property
    def displays(self):
        """Tuple of connected :class:`~modi.module.display.Display` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Display)])

    @property
    def envs(self):
        """Tuple of connected :class:`~modi.module.env.Env` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Env)])

    @property
    def gyros(self):
        """Tuple of connected :class:`~modi.module.gyro.Gyro` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Gyro)])

    @property
    def irs(self):
        """Tuple of connected :class:`~modi.module.ir.Ir` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Ir)])

    @property
    def leds(self):
        """Tuple of connected :class:`~modi.module.led.Led` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Led)])

    @property
    def mics(self):
        """Tuple of connected :class:`~modi.module.mic.Mic` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Mic)])

    @property
    def motors(self):
        """Tuple of connected :class:`~modi.module.motor.Motor` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Motor)])

    @property
    def speakers(self):
        """Tuple of connected :class:`~modi.module.speaker.Speaker` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Speaker)])

    @property
    def ultrasonics(self):
        """Tuple of connected :class:`~modi.module.ultrasonic.Ultrasonic` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Ultrasonic)])
