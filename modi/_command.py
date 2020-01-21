# -*- coding: utf-8 -*-

"""Main module."""

from __future__ import absolute_import

import json
import base64
import struct

from enum import Enum


class Command(object):
    class ModuleState(Enum):
        RUN = 0
        IDLE = 1
        PAUSE = 2
        ERROR = 3
        NO_FIRMWARE = 4
        REBOOT = 6

    class ModulePnp(Enum):
        ON = 1
        OFF = 2

    class PropertyDataType(Enum):
        INT = 0
        FLOAT = 1
        STRING = 2
        RAW = 3
        DISPLAY_Var = 4

    def request_uuid(self, src_id):
        msg = dict()

        msg["c"] = 0x08
        msg["s"] = src_id
        msg["d"] = 0xFFF

        id_bytes = bytearray(8)
        id_bytes[0] = 0xFF
        id_bytes[1] = 0x0F

        msg["b"] = base64.b64encode(bytes(id_bytes)).decode("utf-8")
        msg["l"] = 8

        return json.dumps(msg, separators=(",", ":"))

    def request_network_uuid(self, src_id):
        msg = dict()

        msg["c"] = 0x28
        msg["s"] = src_id
        msg["d"] = 0xFFF

        id_bytes = bytearray(8)
        id_bytes[0] = 0xFF
        id_bytes[1] = 0x0F

        msg["b"] = base64.b64encode(bytes(id_bytes)).decode("utf-8")
        msg["l"] = 8

        return json.dumps(msg, separators=(",", ":"))

    def module_state(self, dst_id, state, pnp):
        if type(state) is self.ModuleState:
            msg = dict()

            msg["c"] = 0x09
            msg["s"] = 0
            msg["d"] = dst_id

            state_bytes = bytearray(2)
            state_bytes[0] = state.value  # set state instruction 에서 Module State 지정 바이트
            state_bytes[
                1
            ] = pnp.value  # set state instruction 에서 Module Plug & Play 지정 바이트

            msg["b"] = base64.b64encode(bytes(state_bytes)).decode("utf-8")
            msg["l"] = 2

            return json.dumps(msg, separators=(",", ":"))
        else:
            raise RuntimeError("The type of state is not ModuleState")

    def set_property(self, dst_id, property_type, values, datatype=None):
        msg = dict()

        msg["c"] = 0x04
        msg["s"] = property_type
        msg["d"] = dst_id

        values_bytes = bytearray(8)
        # motor channel control
        # channel(2) mode(2) value_high(2) value_low(2)
        if datatype is None or datatype == self.PropertyDataType.INT:
            for index, value in enumerate(values):
                value = int(value)
                # leaves the last 8 bits only
                values_bytes[index * 2] = value & 0xFF
                values_bytes[index * 2 + 1] = (value & 0xFF00) >> 8
        elif datatype == self.PropertyDataType.FLOAT:
            for index, value in enumerate(values):
                values_bytes[index * 4 : index * 4 + 4] = struct.pack("f", float(value))
        elif datatype == self.PropertyDataType.STRING:
            cmds = list()
            value = str(values)[:27]
            num_of_chunks = int(len(value) / 8) + 1

            for i in range(num_of_chunks):
                values_bytes[:] = [ord(i) for i in value[i * 8 : i * 8 + 8]]
                msg["b"] = base64.b64encode(bytes(values_bytes)).decode("utf-8")
                msg["l"] = len(values_bytes)
                cmds.append(json.dumps(msg, separators=(",", ":")))
            return cmds
        elif datatype == self.PropertyDataType.RAW:
            msg["b"] = base64.b64encode(bytearray(values)).decode("utf-8")
            msg["l"] = len(values)
        elif datatype == self.PropertyDataType.DISPLAY_Var:
            values_bytes[:4] = struct.pack("f", float(values[0]))
            values_bytes[4] = values[1]
            values_bytes[5] = 0x00
            values_bytes[6] = values[2]
            values_bytes[7] = 0x00
        else:
            raise RuntimeError("Not supported property data type.")

        msg["b"] = base64.b64encode(bytes(values_bytes)).decode("utf-8")
        msg["l"] = 8

        return json.dumps(msg, separators=(",", ":"))

    def get_property(self, dst_id, property_type):
        msg = dict()

        msg["c"] = 0x03
        msg["s"] = 0
        msg["d"] = dst_id

        property_bytes = bytearray(4)

        property_bytes[0] = property_type
        property_bytes[2] = 95

        msg["b"] = base64.b64encode(bytes(property_bytes)).decode("utf-8")
        msg["l"] = 4

        return json.dumps(msg, separators=(",", ":"))
