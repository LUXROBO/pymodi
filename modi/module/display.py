# -*- coding: utf-8 -*-

"""Display module."""

from enum import Enum

from modi.module.module import OutputModule


class Display(OutputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """

    def __init__(self, module_id, module_uuid, modi, serial_write_q):
        super(Display, self).__init__(module_id, module_uuid, modi, serial_write_q)
        self._module_type = "display"
        self._serial_write_q = serial_write_q
        self._module_id = module_id

    def set_text(self, text):
        """
        :param text: Text to display.
        """
        self.clear()
        messages = self._set_property(
            self._module_id, 17, text, self.PropertyDataType.STRING
        )
        for message in messages:
            self._serial_write_q.put(message)
        return messages

    def set_variable(self, variable, position_x, position_y):
        """
        :param variable: Variable to display.
        """
        self.clear()
        message = self._set_property(
            self._module_id,
            22,
            (variable, position_x, position_y),
            self.PropertyDataType.DISPLAY_Var,
        )
        self._serial_write_q.put(message)
        return message

    def clear(self):
        """Clear the screen.
        """
        self._serial_write_q.put(
            self._set_property(self._module_id, 21, bytes(2), self.PropertyDataType.RAW)
        )
