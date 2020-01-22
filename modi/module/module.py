# -*- coding: utf-8 -*-

"""Module module."""

from __future__ import absolute_import

import time

from enum import Enum


class Module(object):
    class ConnectionState(Enum):
        CONNECTED = True
        DISCONNECTED = False

    class Property(object):
        def __init__(self):
            self.value = 0
            self.last_update_time = 0
            self.last_request_time = 0

    def __init__(self, module_id, module_uuid, modi, serial_write_q):
        self._module_id = module_id
        self._module_uuid = module_uuid
        self._modi = modi
        self._serial_write_q = serial_write_q
        self._category = str()
        self._type = str()
        self._properties = dict()
        self._connected = self.ConnectionState.CONNECTED

    @property
    def id(self):
        return self._module_id

    @property
    def uuid(self):
        return self._module_uuid

    @property
    def category(self):
        return self._category

    @property
    def connected(self):
        return self._connected

    @property
    def module_type(self):
        return self._type

    def set_connection_state(self, state):
        self._connected = state

    def _get_property(self, property_):
        if not property_ in self._properties.keys():
            self._properties[property_] = self.Property()
            modi_serialtemp = self._modi._command.request_property(
                self._module_id, property_.value
            )
            self._serial_write_q.put(modi_serialtemp)
            self._properties[property_].last_request_time = time.time()

        duration = time.time() - self._properties[property_].last_update_time
        if duration > 0.5:
            modi_serialtemp = self._modi._command.request_property(
                self._module_id, property_.value
            )
            self._serial_write_q.put(modi_serialtemp)
            self._properties[property_].last_request_time = time.time()

        return self._properties[property_].value

    def update_property(self, prop, value):
        if prop in self._properties.keys():
            self._properties[prop].value = value
            self._properties[prop].last_update_time = time.time()


class SetupModule(Module):
    def __init__(self, module_id, module_uuid, modi):
        super(SetupModule, self).__init__(module_id, module_uuid, modi)
        self._category = "setup"


class InputModule(Module):
    def __init__(self, module_id, module_uuid, modi, serial_write_q):
        super(InputModule, self).__init__(module_id, module_uuid, modi, serial_write_q)
        self._category = "input"


class OutputModule(Module):
    def __init__(self, module_id, module_uuid, modi, serial_write_q):
        super(OutputModule, self).__init__(module_id, module_uuid, modi, serial_write_q)
        self._category = "output"
        self._command = modi._command
