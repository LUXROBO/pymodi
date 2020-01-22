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

    def request_uuid(self, src_id, is_network_module=False):
        BROADCAST_ID = 0xFFF

        msg = dict()
        msg["c"] = 0x28 if is_network_module else 0x08
        msg["s"] = src_id
        msg["d"] = BROADCAST_ID

        id_bytes = bytearray(8)
        id_bytes[0] = 0xFF
        id_bytes[1] = 0x0F

        msg["b"] = base64.b64encode(bytes(id_bytes)).decode("utf-8")
        msg["l"] = 8

        return json.dumps(msg, separators=(",", ":"))

    def set_module_state(self, dst_id, module_state, pnp_state):
        if type(module_state) is self.ModuleState:
            msg = dict()

            msg["c"] = 0x09
            msg["s"] = 0
            msg["d"] = dst_id

            state_bytes = bytearray(2)
            state_bytes[0] = module_state.value
            state_bytes[1] = pnp_state.value

            msg["b"] = base64.b64encode(bytes(state_bytes)).decode("utf-8")
            msg["l"] = 2

            return json.dumps(msg, separators=(",", ":"))
        else:
            raise RuntimeError("The type of state is not ModuleState")

    def set_property(self, dst_id, property_type, property_values, data_type=None):
        msg = dict()

        msg["c"] = 0x04
        msg["s"] = property_type
        msg["d"] = dst_id

        property_values_bytes = bytearray(8)
        if data_type is None or data_type == self.PropertyDataType.INT:
            for index, property_value in enumerate(property_values):
                property_value = int(property_value)
                property_values_bytes[index * 2] = property_value & 0xFF
                property_values_bytes[index * 2 + 1] = (property_value & 0xFF00) >> 8

        elif data_type == self.PropertyDataType.FLOAT:
            for index, property_value in enumerate(property_values):
                property_values_bytes[index * 4 : index * 4 + 4] = struct.pack(
                    "f", float(property_value)
                )

        elif data_type == self.PropertyDataType.STRING:
            msgs = list()
            property_value = str(property_values)[:27]
            num_of_chunks = int(len(property_value) / 8) + 1

            for i in range(num_of_chunks):
                property_values_bytes[:] = [
                    ord(i) for i in property_value[i * 8 : i * 8 + 8]
                ]
                msg["b"] = base64.b64encode(bytes(property_values_bytes)).decode(
                    "utf-8"
                )
                msg["l"] = len(property_values_bytes)
                msgs.append(json.dumps(msg, separators=(",", ":")))
            return msgs

        elif data_type == self.PropertyDataType.RAW:
            msg["b"] = base64.b64encode(bytearray(property_values)).decode("utf-8")
            msg["l"] = len(property_values)

        elif data_type == self.PropertyDataType.DISPLAY_Var:
            property_values_bytes[:4] = struct.pack("f", float(property_values[0]))
            property_values_bytes[4] = property_values[1]
            property_values_bytes[5] = 0x00
            property_values_bytes[6] = property_values[2]
            property_values_bytes[7] = 0x00

        else:
            raise RuntimeError("Not supported property data type.")

        msg["b"] = base64.b64encode(bytes(property_values_bytes)).decode("utf-8")
        msg["l"] = 8

        return json.dumps(msg, separators=(",", ":"))

    def request_property(self, dst_id, property_type):
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
