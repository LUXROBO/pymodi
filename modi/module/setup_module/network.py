"""Network module."""

from enum import IntEnum

from modi.module.setup_module.setup_module import SetupModule


class Network(SetupModule):
    class PropertyType(IntEnum):
        BUTTON = 3
        # JOYSTICK = 3 Why TF are these the same
        DIAL = 4
        LEFT_SLIDER = 5
        RIGHT_SLIDER = 6
        TIMER = 7
        BUTTON_CLICK = 0x0102
        BUTTON_DOUBLE_CLICK = 0x0103
        TOGGLE = 0x00104

    class CommandType(IntEnum):
        BUZZER = 0x0100
        CAMERA = 0x0101

    @property
    def button_pressed(self):
        return self._get_property(self.PropertyType.BUTTON)

    @property
    def dial(self):
        return self._get_property(self.PropertyType.DIAL)

    @property
    def left_slider(self):
        return self._get_property(self.PropertyType.LEFT_SLIDER)

    @property
    def right_slider(self):
        return self._get_property(self.PropertyType.RIGHT_SLIDER)

    @property
    def timer(self):
        return self._get_property(self.PropertyType.TIMER)
