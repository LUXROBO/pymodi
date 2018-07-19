# -*- coding: utf-8 -*-

"""Main module."""

from __future__ import absolute_import

import json
import base64

from enum import Enum

class ModuleState(Enum):
    RUN = 0
    IDLE = 1
    PAUSE = 2
    ERROR = 3
    NO_FIRMWARE = 4
    REBOOT = 5

def request_uuid(id):
    msg = dict()

    msg['c'] = 0x08
    msg['s'] = 0
    msg['d'] = 0xFFF

    id_bytes = bytearray(8)
    id_bytes[0] = id & 0xFF
    id_bytes[1] = (id & 0xFF00) >> 8

    msg['b'] = base64.b64encode(bytes(id_bytes)).decode('utf-8')
    msg['l'] = 8

    return json.dumps(msg, separators=(',', ':'))

def module_state(id, state):
    if type(state) is ModuleState:
        msg = dict()

        msg['c'] = 0x09
        msg['s'] = 0
        msg['d'] = id

        state_bytes = bytearray(2)
        state_bytes[1] = state.value

        msg['b'] = base64.b64encode(bytes(state_bytes)).decode('utf-8')
        msg['l'] = 2

        return json.dumps(msg, separators=(',', ':'))
    else:
        raise RuntimeError("The type of state is not ModuleState")
    
def set_property(id, property_type, values):
    msg = dict()

    msg['c'] = 0x04
    msg['s'] = property_type
    msg['d'] = id

    values_bytes = bytearray(8)

    for index, value in enumerate(values):
        value = int(value)
        values_bytes[index * 2] = value & 0xFF
        values_bytes[index * 2 + 1] = (value & 0xFF00) >> 8

    msg['b'] = base64.b64encode(bytes(values_bytes)).decode('utf-8')
    msg['l'] = 8

    return json.dumps(msg, separators=(',', ':'))

def get_property(id, property_type):
    msg = dict()

    msg['c'] = 0x03
    msg['s'] = 0
    msg['d'] = id

    property_bytes = bytearray(4)

    property_bytes[0] = property_type
    property_bytes[2] = 97 

    msg['b'] = base64.b64encode(bytes(property_bytes)).decode('utf-8')
    msg['l'] = 4

    return json.dumps(msg, separators=(',', ':'))