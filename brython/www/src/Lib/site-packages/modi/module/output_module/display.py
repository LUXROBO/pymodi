"""Display module."""

from modi.module.output_module.output_module import OutputModule


class Display(OutputModule):

    TEXT = 17
    CLEAR = 21
    VARIABLE = 22
    SET_HORIZONTAL = 25
    SET_VERTICAL = 26

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)
        self._text = ""

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        """Clears the display and show the input string on the display.
        Returns the json serialized signal sent to the module
        to display the text

        :param text: Text to display.
        :type text: str
        :return: None
        """
        self.clear()
        self._set_property(
            self._id,
            Display.TEXT,
            str(text)[:27] + '\0',  # 27 characters can be shown on the display
            OutputModule.STRING
        )
        self._text = text

    def show_variable(self, variable: float, position_x: int,
                      position_y: int) -> None:
        """Clears the display and show the input variable on the display.
        Returns the json serialized signal sent to
        the module to display the text

        :param variable: variable to display.
        :type variable: float
        :param position_x: x coordinate of the desired position
        :type position_x: int
        :param position_y: y coordinate of te desired position
        :type position_y: int
        :return: A json serialized signal to module
        :rtype: string
        """
        self._set_property(
            self._id,
            Display.VARIABLE,
            (variable, position_x, position_y),
            OutputModule.DISPLAY_VAR,
        )
        self._text += str(variable)

    def set_horizontal(self, offset) -> None:
        """Set the horizontal offset on the screen

        :param offset: offset in pixels
        :type offset: float
        :return: None
        """
        self._set_property(
            self.id,
            Display.SET_HORIZONTAL, (offset, ),
            OutputModule.FLOAT,
        )

    def set_vertical(self, offset) -> None:
        """Set the vertical offset on the screen

        :param offset: offset in pixels
        :type offset: float
        :return: None
        """
        self._set_property(
            self.id,
            Display.SET_VERTICAL, (offset, ),
            OutputModule.FLOAT,
        )

    def clear(self) -> None:
        """Clear the screen.

        :return: json serialized message to te module
        :rtype: string
        """
        self._set_property(
            self._id,
            Display.CLEAR,
            (0, 0),
            OutputModule.RAW
        )
        self._text = ""
