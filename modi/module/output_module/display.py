"""Display module."""

from enum import Enum

from modi.module.output_module.output_module import OutputModule


class Display(OutputModule):

    class PropertyType(Enum):
        TEXT = 17
        CLEAR = 21
        VARIABLE = 22

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)

    def set_text(self, text):
        """
        :param text: Text to display.
        """
        self.clear()
        messages = self._set_property(
            self._id,
            self.PropertyType.TEXT.value,
            text,
            self.PropertyDataType.STRING
        )
        for message in messages:
            self._msg_send_q.put(message)
        return messages

    def set_variable(self, variable, position_x, position_y):
        """
        :param variable: Variable to display.
        """
        self.clear()
        message = self._set_property(
            self._id,
            self.PropertyType.VARIABLE.value,
            (variable, position_x, position_y),
            self.PropertyDataType.DISPLAY_VAR,
        )
        self._msg_send_q.put(message)
        return message

    def clear(self):
        """Clear the screen.
        """
        message = self._set_property(
            self._id,
            self.PropertyType.CLEAR.value,
            bytes(2),
            self.PropertyDataType.RAW
        )

        self._msg_send_q.put(message)
        return message
