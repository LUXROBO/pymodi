"""Button module."""

from modi.module.input_module.input_module import InputModule


class Button(InputModule):

    CLICKED = 2
    DOUBLE_CLICKED = 3
    PRESSED = 4
    TOGGLED = 5

    @property
    def clicked(self) -> bool:
        """Returns true when button is clicked

        :return: `True` if clicked or `False`.
        :rtype: bool
        """
        return self._get_property(Button.CLICKED) == 100.

    @property
    def double_clicked(self) -> bool:
        """Returns true when button is double clicked

        :return: `True` if double clicked or `False`.
        :rtype: bool
        """
        return self._get_property(Button.DOUBLE_CLICKED) == 100.

    @property
    def pressed(self) -> bool:
        """Returns true while button is pressed

        :return: `True` if pressed or `False`.
        :rtype: bool
        """
        return self._get_property(Button.PRESSED) == 100.

    @property
    def toggled(self) -> bool:
        """Returns true when button is toggled

        :return: `True` if toggled or `False`.
        :rtype: bool
        """
        return self._get_property(Button.TOGGLED) == 100.
