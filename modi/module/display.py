# -*- coding: utf-8 -*-

"""Display module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import OutputModule


class Display(OutputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """

    class PropertyType(Enum):
        CURSOR_X = 2
        CURSOR_Y = 3

    def __init__(self, id, uuid, modi, serial_write_q):
        super(Display, self).__init__(id, uuid, modi, serial_write_q)
        self._type = "display"
        self._serial_write_q = serial_write_q

    def text(self, text):
        """
        :param text: Text to display.
        """
        self.clear()

        for string in self._command.set_property(
            self.id, 17, text, self._command.PropertyDataType.STRING
        ):
            self._serial_write_q.put(string)

    def variable(self, var, axisx, axisy):
        """
        :param variable: variable to display.
        """
        self.clear()

        string = self._command.set_property(
            self.id, 22, (var, axisx, axisy), self._command.PropertyDataType.DISPLAY_Var
        )
        self._serial_write_q.put(string)

    def clear(self):
        """Clear the screen.
        """
        self._serial_write_q.put(
            self._command.set_property(
                self.id, 20, bytes(2), self._command.PropertyDataType.RAW
            )
        )
