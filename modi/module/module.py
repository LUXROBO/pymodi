"""Module module."""

import json
import time
import base64

from enum import Enum


class Module:
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param serial_write_q: multiprocessing.queue of the serial writing
    """

    class Property:
        def __init__(self):
            self.value = 0
            self.last_update_time = 0
            self.last_request_time = 0

    class State(Enum):
        RUN = 0
        WARNING = 1
        FORCED_PAUSE = 2
        ERROR_STOP = 3
        UPDATE_FIRMWARE = 4
        UPDATE_FIRMWARE_READY = 5
        REBOOT = 6
        PNP_ON = 7
        PNP_OFF = 8

    def __init__(self, id_, uuid, msg_send_q):
        self._id = id_
        self._uuid = uuid
        self._msg_send_q = msg_send_q

        self._properties = dict()

        self._is_connected = True

    @property
    def id(self):
        return self._id

    @property
    def uuid(self):
        return self._uuid

    @property
    def is_connected(self):
        return self._is_connected

    def set_connection_state(self, connection_state):
        self._is_connected = connection_state

    def _get_property(self, property_type):
        """ Get module property value and request
        """

        # Register property if not exists
        if property_type not in self._properties.keys():
            self._properties[property_type] = self.Property()
            modi_serialtemp = self.request_property(
                self._id, property_type.value
            )
            self._msg_send_q.put(modi_serialtemp)
            self._properties[property_type].last_request_time = time.time()

        # Request property value if not updated for 0.5 sec
        duration = time.time() - \
            self._properties[property_type].last_update_time
        if duration > 1:
            modi_serialtemp = self.request_property(
                self._id, property_type.value
            )
            self._msg_send_q.put(modi_serialtemp)
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
