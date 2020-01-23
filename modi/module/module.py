# -*- coding: utf-8 -*-

"""Module module."""

import json
import time
import base64
import struct

from enum import Enum


class Module:
    class Property:
        def __init__(self):
            self.value = 0
            self.last_update_time = 0
            self.last_request_time = 0

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

    def __init__(self, module_id, module_uuid, modi, serial_write_q):
        self._module_id = module_id
        self._module_uuid = module_uuid
        self._modi = modi
        self._module_type = str()
        self._category = str()
        self._properties = dict()
        self._connected = True
        self._serial_write_q = serial_write_q

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
        return self._module_type

    def set_connection_state(self, connection_state):
        self._connected = connection_state

    def _get_property(self, property_type):
        if not property_type in self._properties.keys():
            self._properties[property_type] = self.Property()
            modi_serialtemp = self.request_property(
                self._module_id, property_type.value
            )
            self._serial_write_q.put(modi_serialtemp)
            self._properties[property_type].last_request_time = time.time()

        duration = time.time() - self._properties[property_type].last_update_time
        if duration > 0.5:
            modi_serialtemp = self.request_property(
                self._module_id, property_type.value
            )
            self._serial_write_q.put(modi_serialtemp)
            self._properties[property_type].last_request_time = time.time()

        return self._properties[property_type].value

    def update_property(self, property_type, property_value):
        if property_type in self._properties.keys():
            self._properties[property_type].value = property_value
            self._properties[property_type].last_update_time = time.time()

    def request_property(self, destination_id, property_type):
        message = dict()

        message["c"] = 0x03
        message["s"] = 0
        message["d"] = destination_id

        property_bytes = bytearray(4)

        property_bytes[0] = property_type
        property_bytes[2] = 95

        message["b"] = base64.b64encode(bytes(property_bytes)).decode("utf-8")
        message["l"] = 4

        return json.dumps(message, separators=(",", ":"))


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

    class PropertyDataType(Enum):
        INT = 0
        FLOAT = 1
        STRING = 2
        RAW = 3
        DISPLAY_Var = 4

    def _set_property(
        self, destination_id, property_type, property_values, property_data_type=None
    ):
        message = dict()

        message["c"] = 0x04
        message["s"] = property_type
        message["d"] = destination_id

        property_values_bytes = bytearray(8)
        if (
            property_data_type is None
            or property_data_type == self.PropertyDataType.INT
        ):
            for index, property_value in enumerate(property_values):
                property_value = int(property_value)
                property_values_bytes[index * 2] = property_value & 0xFF
                property_values_bytes[index * 2 + 1] = (property_value & 0xFF00) >> 8

        elif property_data_type == self.PropertyDataType.FLOAT:
            for index, property_value in enumerate(property_values):
                property_values_bytes[index * 4 : index * 4 + 4] = struct.pack(
                    "f", float(property_value)
                )

        elif property_data_type == self.PropertyDataType.STRING:
            messages = list()
            property_value = str(property_values)[:27]
            num_of_chunks = int(len(property_value) / 8) + 1

            for i in range(num_of_chunks):
                property_values_bytes[:] = [
                    ord(i) for i in property_value[i * 8 : i * 8 + 8]
                ]
                message["b"] = base64.b64encode(bytes(property_values_bytes)).decode(
                    "utf-8"
                )
                message["l"] = len(property_values_bytes)
                messages.append(json.dumps(message, separators=(",", ":")))
            return messages

        elif property_data_type == self.PropertyDataType.RAW:
            message["b"] = base64.b64encode(bytearray(property_values)).decode("utf-8")
            message["l"] = len(property_values)

        elif property_data_type == self.PropertyDataType.DISPLAY_Var:
            property_values_bytes[:4] = struct.pack("f", float(property_values[0]))
            property_values_bytes[4] = property_values[1]
            property_values_bytes[5] = 0x00
            property_values_bytes[6] = property_values[2]
            property_values_bytes[7] = 0x00
        else:
            raise RuntimeError("Not supported property data type.")

        message["b"] = base64.b64encode(bytes(property_values_bytes)).decode("utf-8")
        message["l"] = 8

        return json.dumps(message, separators=(",", ":"))
