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

    def __init__(self, id, uuid, modi):
        super(Display, self).__init__(id, uuid, modi)
        self._type = "display"

    def text(self, text):
        """
        :param text: Text to display.
        """
        self.clear()

        for cmd in self._command.set_property(
            self.id, 17, text, self._command.PropertyDataType.STRING
        ):
            self._modi.write(cmd, is_display=True)

    def variable(self, var):
        """
        :param variable: variable to display.
        """
        self.clear()
        for cmd in self._command.set_property(self.id, 21, var, (10, 20, var)):
            self._modi.write(cmd, is_display=True)

    def clear(self):
        """Clear the screen.
        """
        self._modi.write(
            self._command.set_property(
                self.id, 20, bytes(2), self._command.PropertyDataType.RAW
            ),
            is_display=True,
        )
