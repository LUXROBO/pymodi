"""Module module."""

import time
from typing import Union

from modi.util.msgutil import parse_message

BROADCAST_ID = 0xFFF


class Module:

    class Property:
        def __init__(self, value: Union[int, float] = 0):
            self.value = value
            self.last_update_time = time.time()

    RUN = 0
    WARNING = 1
    FORCED_PAUSE = 2
    ERROR_STOP = 3
    UPDATE_FIRMWARE = 4
    UPDATE_FIRMWARE_READY = 5
    REBOOT = 6
    PNP_ON = 1
    PNP_OFF = 2

    def __init__(self, id_, uuid, conn_task):
        self._id = id_
        self._uuid = uuid
        self._conn = conn_task

        self.module_type = str()
        self._properties = dict()

        # sampling_rate = (100 - property_sampling_frequency) * 11, in ms
        self.prop_samp_freq = 91

        self.is_connected = True
        self.has_printed = False
        self.last_updated = time.time()
        self.battery = 100
        self.position = (0, 0)
        self.__version = None
        self.user_code_status = -1  # 1 if user code and 0 if not

    def __gt__(self, other):
        if self.order == other.order:
            if self.position[0] == other.position[0]:
                return self.position[1] < other.position[1]
            else:
                return self.position[0] > other.position[0]
        else:
            return self.order > other.order

    def __lt__(self, other):
        if self.order == other.order:
            if self.position[0] == other.position[0]:
                return self.position[1] > other.position[1]
            else:
                return self.position[0] < other.position[0]
        else:
            return self.order < other.order

    def __str__(self):
        return f"{self.__class__.__name__} ({self._id})"

    @property
    def version(self):
        print("Verison info is not supported in the demo version!")
        return None

    @property
    def order(self):
        return self.position[0] ** 2 + self.position[1] ** 2

    @property
    def id(self) -> int:
        return self._id

    @property
    def uuid(self) -> int:
        return self._uuid

    def _get_property(self, property_type: int) -> float:
        # Register property if not exists
        if property_type not in self._properties:
            self._properties[property_type] = self.Property()
            self.__request_property(self._id, property_type)

        # Request property value if not updated for 1.5 sec
        last_update = self._properties[property_type].last_update_time
        if time.time() - last_update > 1.5:
            self.__request_property(self._id, property_type)

        return self._properties[property_type].value

    def update_property(self, property_type: int,
                        property_value: float) -> None:
        if property_type not in self._properties:
            self._properties[property_type] = self.Property()
        self._properties[property_type].value = property_value
        self._properties[property_type].last_update_time = time.time()

    def __request_property(self, destination_id: int,
                           property_type: int) -> None:
        self._properties[property_type].last_update_time = time.time()
        req_prop_msg = parse_message(
            0x03, 0, destination_id,
            (property_type, None, self.prop_samp_freq, None)
        )
        self._conn.send(req_prop_msg)
