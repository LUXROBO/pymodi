# -*- coding: utf-8 -*-

"""Network module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import SetupModule

class PropertyType(Enum):
    RESERVED = 0

class Network(SetupModule):
    property_types = PropertyType

    def __init__(self, id, uuid, modi):
        super(Network, self).__init__(id, uuid, modi)
        self._type = "network"
