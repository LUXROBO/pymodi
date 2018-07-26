# -*- coding: utf-8 -*-

"""Led module."""

from __future__ import absolute_import

from enum import Enum

from modi.module._module import OutputModule

from modi._cmd import set_property

class PropertyType(Enum):
    RED = 2
    GREEN = 3
    BLUE = 4

class Led(OutputModule):
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Led, self).__init__(id, uuid, modi)
        self._type = "led"

    def rgb(self, red=None, green=None, blue=None):
        if red == None and green == None and blue == None:
            return (self.red(), self.green(), self.blue())
        else:
            self._modi().write(set_property(self.id, 16, (
                red if red != None else self.red(), 
                green if green != None else self.green(), 
                blue if blue != None else self.blue()
                )))

    def on(self):
        self.rgb(255, 255, 255)
    
    def off(self):
        self.rgb(0, 0, 0)

    def red(self, red=None):
        if red == None:
            return self._properties[PropertyType.RED]
        else:
            self.rgb(red=red)

    def green(self, green=None):
        if green == None:
            return self._properties[PropertyType.GREEN]
        else:
            self.rgb(green=green)

    def blue(self, blue=None):
        if blue == None:
            return self._properties[PropertyType.BLUE]
        else:
            self.rgb(blue=blue)
