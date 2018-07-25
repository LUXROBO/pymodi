# -*- coding: utf-8 -*-

"""Main module."""

from __future__ import absolute_import

import json
import base64
import struct

from enum import Enum

class ModuleState(Enum):
    RUN = 0
    IDLE = 1
    PAUSE = 2
    ERROR = 3
    NO_FIRMWARE = 4
    REBOOT = 5

class PropertyDataType(Enum):
    INT = 0
    FLOAT = 1
    STRING = 2
    RAW = 3

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
    
def set_property(id, property_type, values, datatype=None):
    msg = dict()

    msg['c'] = 0x04
    msg['s'] = property_type
    msg['d'] = id

    values_bytes = bytearray(8)

    if datatype == None or datatype == PropertyDataType.INT:
        for index, value in enumerate(values):
            value = int(value)
            values_bytes[index * 2] = value & 0xFF
            values_bytes[index * 2 + 1] = (value & 0xFF00) >> 8
    elif datatype == PropertyDataType.FLOAT:
        for index, value in enumerate(values):
            values_bytes[index * 4:index * 4 + 4] = struct.pack('f', float(value))
    elif datatype == PropertyDataType.STRING:
        cmds = list()
        value = str(values)[:27]
        num_of_chunks = int(len(value) / 8) + 1

        for i in range(num_of_chunks):
            values_bytes[:] = [ord(i) for i in value[i * 8:i * 8 + 8]]
            msg['b'] = base64.b64encode(bytes(values_bytes)).decode('utf-8')
            msg['l'] = len(values_bytes)

            cmds.append(json.dumps(msg, separators=(',', ':')))

        return tuple(cmds)
    elif datatype == PropertyDataType.RAW:
        msg['b'] = base64.b64encode(bytearray(values)).decode('utf-8')
        msg['l'] = len(values)

    else:
        raise RuntimeError("Not supported property data type.")

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