"""Display module."""

from enum import Enum

from modi.module.output_module.output_module import OutputModule


class Display(OutputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param serial_write_q: multiprocessing.queue of the serial writing
    """

    class PropertyType(Enum):
        TEXT = 17
        CLEAR = 21
        VARIABLE = 22

    def __init__(self, id_, uuid, serial_write_q):
        super(Display, self).__init__(id_, uuid, serial_write_q)
        self._type = "display"

    def set_text(self, text):
        """
        :param text: Text to display.
        """
        self.clear()
        messages = self._set_property(
            self._id, self.PropertyType.TEXT, text, self.PropertyDataType.STRING
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
            self._id,
            self.PropertyType.VARIABLE,
            (variable, position_x, position_y),
            self.PropertyDataType.DISPLAY_VAR,
        )
        self._serial_write_q.put(message)
        return message

    def clear(self):
        """Clear the screen.
        """
        message = self._set_property(
            self._id, self.PropertyType.CLEAR, bytes(2), self.PropertyDataType.RAW
        )
        self._serial_write_q.put(message)
        return message
