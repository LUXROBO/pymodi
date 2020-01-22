# -*- coding: utf-8 -*-

"""Serial Parsing Task module."""

from __future__ import absolute_import

import json
import time
import queue


class ParserTask(object):
    def __init__(self, serial_read_q, recv_q):
        super(ParserTask, self).__init__()
        self._serial_read_q = serial_read_q
        self._recv_q = recv_q

        self.__buffer = str()
        self.__json = str()

    def start_thread(self):
        self.read_json()
        time.sleep(0.008)

    def read_json(self):
        try:
            data = self._serial_read_q.get_nowait()
        except queue.Empty:
            pass
        else:
            self.__buffer += data

        while self.has_json():
            json_temp = self.__json
            self._recv_q.put(json_temp)

    def has_json(self):
        end = self.__buffer.find("}")
        if end >= 0:
            start = self.__buffer.rfind("{", 0, end)
            if start >= 0:
                self.__json = self.__buffer[start : end + 1]
                self.__buffer = self.__buffer[end + 1 :]
                return True
            else:
                self.__buffer = self.__buffer[end + 1 :]
                return False
        else:
            start = self.__buffer.rfind("{")
            if start >= 0:
                self.__buffer = self.__buffer[start:]
            else:
                self.__buffer = str()
            return False
