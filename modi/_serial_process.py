# -*- coding: utf-8 -*-

import multiprocessing

from modi._serial_task import SerialTask


class SerialProcess(multiprocessing.Process):
    def __init__(self, serial_read_q, serial_write_q):
        super(SerialProcess, self).__init__()
        self.__ser_task = SerialTask(serial_read_q, serial_write_q)
        self.__stop = multiprocessing.Event()

    def run(self):
        self.__ser_task.open_serial()
        while not self.stopped():
            self.__ser_task.start_thread()
        self.__ser_task.close_serial()

    def stop(self):
        self.__stop.set()

    def stopped(self):
        return self.__stop.is_set()
