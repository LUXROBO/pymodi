# -*- coding: utf-8 -*-

"""Led module."""

from enum import Enum

from modi.module.module import OutputModule


class Led(OutputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """

    class PropertyType(Enum):
        RED = 2
        GREEN = 3
        BLUE = 4

    def __init__(self, module_id, module_uuid, modi, serial_write_q):
        super(Led, self).__init__(module_id, module_uuid, modi, serial_write_q)
        self._module_type = "led"
        self._serial_write_q = serial_write_q
        self._module_id = module_id

    def rgb(self, red=None, green=None, blue=None):
        """
        * If either *red*, *green*, or *blue* is not ``None``,

        :param int red: Red component to set or ``None``.
        :param int green: Green component to set or ``None``.
        :param int blue: Blue component to set or ``None``.

        The ``None`` component retains its previous value.

        * If *red*, *green* and *blue* are ``None``,

        :return: Tuple of red, green and blue.
        :rtype: tuple
        """
        if not (red is None and green is None and blue is None):
            self._serial_write_q.put(
                self._set_property(
                    self._module_id,
                    16,
                    (
                        red if red is not None else self.red(),
                        green if green is not None else self.green(),
                        blue if blue is not None else self.blue(),
                    ),
                )
            )
        return self.red(), self.green(), self.blue()

    def on(self):
        """Turn on at maximum brightness.
        """
        return self.rgb(255, 255, 255)

    def off(self):
        """Turn off.
        """
        return self.rgb(0, 0, 0)

    def red(self, red=None):
        """
        :param int red: Red component to set or ``None``.

        If *red* is ``None``.

        :return: Red component.
        :rtype: float
        """
        if red is not None:
            self.rgb(red=red)
        return self._get_property(self.PropertyType.RED)

    def green(self, green=None):
        """
        :param int green: Green component to set or ``None``.

        If *green* is ``None``.

        :return: Green component.
        :rtype: float
        """
        if green is not None:
            self.rgb(green=green)
        return self._get_property(self.PropertyType.GREEN)

    def blue(self, blue=None):
        """
        :param int blue: Blue component to set or ``None``.

        If *blue* is ``None``.

        :return: Blue component.
        :rtype: float
        """
        if blue is not None:
            self.rgb(blue=blue)
        return self._get_property(self.PropertyType.BLUE)
