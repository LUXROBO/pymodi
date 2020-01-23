# -*- coding: utf-8 -*-

import multiprocessing

from modi._parser_task import ParserTask


class ParserProcess(multiprocessing.Process):
    """ This process run parser task
    """

    def __init__(self, serial_read_q, json_recv_q):
        super(ParserProcess, self).__init__()
        self.__par_task = ParserTask(serial_read_q, json_recv_q)
        self.__stop = multiprocessing.Event()

    def run(self):
        while not self.stopped():
            self.__par_task.start_thread()

    def stop(self):
        self.__stop.set()

    def stopped(self):
        return self.__stop.is_set()

