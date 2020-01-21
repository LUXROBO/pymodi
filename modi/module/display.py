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
        msgs = self._command.set_property(
            self.id, 17, text, self._command.PropertyDataType.STRING
        )
        for msg_str in msgs:
            self._serial_write_q.put(msg_str)
        return msgs

    def variable(self, var, pos_x, pos_y):
        """
        :param variable: variable to display.
        """
        self.clear()
        msg = self._command.set_property(
            self.id, 22, (var, pos_x, pos_y), self._command.PropertyDataType.DISPLAY_Var
        )
        self._serial_write_q.put(msg)
        return msg

    def clear(self):
        """Clear the screen.
        """
        self._serial_write_q.put(
            self._command.set_property(
                self.id, 20, bytes(2), self._command.PropertyDataType.RAW
            )
        )
