# -*- coding: utf-8 -*-

import multiprocessing

from modi._parser_task import ParserTask


class ParserProcess(multiprocessing.Process):
    def __init__(self, serial_read_q, recv_q):
        super(ParserProcess, self).__init__()
        self.__par_task = ParserTask(serial_read_q, recv_q)
        self.__stop = multiprocessing.Event()

    def run(self):
        while not self.stopped():
            self.__par_task.start_thread()

    def stop(self):
        self.__stop.set()

    def stopped(self):
        return self.__stop.is_set()

