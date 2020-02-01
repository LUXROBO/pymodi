"""Module module."""

import json
import time
import base64
import struct

from enum import Enum


class Module:
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI  `
    :param serial_write_q: multiprocessing.queue of the serial writing
    """

    class ModuleProperty:
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

    class ModulePnpState(Enum):
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
    def module_id(self):
        return self._module_id

    @property
    def module_uuid(self):
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
        """ Get module property value and request
        """

        # Register property if not exists
        if not property_type in self._properties.keys():
            self._properties[property_type] = self.ModuleProperty()
            modi_serialtemp = self.request_property(
                self._module_id, property_type.value
            )
            self._serial_write_q.put(modi_serialtemp)
            self._properties[property_type].last_request_time = time.time()

        # Request property value if not updated for 0.5 sec
        duration = time.time() - self._properties[property_type].last_update_time
        if duration > 0.5:
            modi_serialtemp = self.request_property(
                self._module_id, property_type.value
            )
            self._serial_write_q.put(modi_serialtemp)
            self._properties[property_type].last_request_time = time.time()

        return self._properties[property_type].value

    def update_property(self, property_type, property_value):
        """ Update property value and time
        """

        if property_type in self._properties.keys():
            self._properties[property_type].value = property_value
            self._properties[property_type].last_update_time = time.time()

    def request_property(self, destination_id, property_type):
        """ Generate message for request property
        """

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

