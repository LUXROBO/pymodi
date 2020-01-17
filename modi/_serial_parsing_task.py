# -*- coding: utf-8 -*-

"""Serial Parsing Task module."""

from __future__ import absolute_import

import json
import time


class ParsingTask(object):
    def __init__(self, serial_read_q, recv_q, json_box):
        super(ParsingTask, self).__init__()
        self._serial_read_q = serial_read_q
        self._recv_q = recv_q
        self._json_box = json_box
        # if os.name != 'nt':
        #    self.start_thread()

    def start_thread(self):
        # print('ParsingTask : ', os.getpid())
        # while True:
        self.adding_json()
        time.sleep(0.005)

    def adding_json(self):
        try:
            self._json_box.add(self._serial_read_q.get(False))
        except:
            pass

        while self._json_box.has_json():
            json_temp = self._json_box.json
            self._recv_q.put(json_temp)
            # print('jsonread : ', json_temp)
