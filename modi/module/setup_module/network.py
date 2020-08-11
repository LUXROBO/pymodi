"""Network module."""

from enum import IntEnum

from modi.module.setup_module.setup_module import SetupModule
from modi.util.msgutil import parse_message


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
        BUZZER = 0x0003
        CAMERA = 0x0101

    @property
    def button_pressed(self):
        return self._get_property(self.PropertyType.BUTTON) == 100

    @property
    def joystick(self):
        return {
            20.0: 'up',
            30.0: 'down',
            40.0: 'left',
            50.0: 'right',
        }.get(self._get_property(self.PropertyType.BUTTON))

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
        return self._get_property(self.PropertyType.TIMER) == 100

    @property
    def button_clicked(self):
        return self._get_property(self.PropertyType.BUTTON_CLICK) == 100

    @property
    def button_double_clicked(self):
        return self._get_property(self.PropertyType.BUTTON_DOUBLE_CLICK) == 100

    @property
    def button_toggled(self):
        return self._get_property(self.PropertyType.BUTTON.TOGGLE) == 100

    def take_picture(self):
        cam_msg = parse_message(
            0x04, self.CommandType.CAMERA, self._id,
            (0x64, 0, 0, 0, 0, 0, 0, 0)
        )
        self._conn.send(cam_msg)

    def buzzer_on(self):
        buz_msg = parse_message(
            0x04, self.CommandType.BUZZER, self._id,
            (0x64, 0, 0, 0, 0, 0, 0, 0)
        )
        self._conn.send(buz_msg)

    def buzzer_off(self):
        buz_msg = parse_message(
            0x04, self.CommandType.BUZZER, self._id,
            (0, 0, 0, 0, 0, 0, 0, 0)
        )
        self._conn.send(buz_msg)
