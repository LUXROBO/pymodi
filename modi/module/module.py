# -*- coding: utf-8 -*-

"""Module module."""

from __future__ import absolute_import

import time


class Prop(object):
    def __init__(self):
        self.value = 0
        self.last_update_time = 0
        self.last_request_time = 0


class Module(object):
    def __init__(self, id, uuid, modi, serial_write_q):
        self._id = id
        self._uuid = uuid
        self._modi = modi
        self._serial_write_q = serial_write_q
        self._category = str()
        self._type = str()
        self._properties = dict()
        self._connected = True

    @property
    def id(self):
        return self._id

    @property
    def uuid(self):
        return self._uuid

    @property
    def category(self):
        return self._category

    @property
    def connected(self):
        return self._connected

    @property
    def type(self):
        return self._type

    def set_connected(self, flag):
        self._connected = flag

    def _write_property(self, prop):
        if not prop in self._properties.keys():
            self._properties[prop] = Prop()
            modi_serialtemp = self._modi._cmd.get_property(self._id, prop.value)
            self._serial_write_q.put(modi_serialtemp)
            self._properties[prop].last_request_time = time.time()

        duration = time.time() - self._properties[prop].last_update_time
        if duration > 0.5:  # 1초
            modi_serialtemp = self._modi._cmd.get_property(self._id, prop.value)
            self._serial_write_q.put(modi_serialtemp)
            self._properties[prop].last_request_time = time.time()

        return self._properties[prop].value

    def update_property(self, prop, value):
        if prop in self._properties.keys():
            self._properties[prop].value = value
            self._properties[prop].last_update_time = time.time()


class SetupModule(Module):
    def __init__(self, id, uuid, modi):
        super(SetupModule, self).__init__(id, uuid, modi)
        self._category = "setup"


class InputModule(Module):
    def __init__(self, id, uuid, modi, serial_write_q):
        super(InputModule, self).__init__(id, uuid, modi, serial_write_q)
        self._category = "input"


class OutputModule(Module):
    def __init__(self, id, uuid, modi, serial_write_q):
        super(OutputModule, self).__init__(id, uuid, modi, serial_write_q)
        self._category = "output"
        self._command = modi._cmd
