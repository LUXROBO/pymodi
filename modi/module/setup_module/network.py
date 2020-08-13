"""Network module."""
from modi.module.setup_module.setup_module import SetupModule
from modi.util.msgutil import parse_message


class Network(SetupModule):

    BUTTON = 3
    JOYSTICK = 3
    DIAL = 4
    LEFT_SLIDER = 5
    RIGHT_SLIDER = 6
    TIMER = 7
    BUTTON_CLICK = 0x0102
    BUTTON_DOUBLE_CLICK = 0x0103
    TOGGLE = 0x00104

    BUZZER = 0x0003
    CAMERA = 0x0101

    @property
    def button_pressed(self):
        return self._get_property(Network.BUTTON) == 100

    @property
    def joystick(self):
        return {
            20.0: 'up',
            30.0: 'down',
            40.0: 'left',
            50.0: 'right',
        }.get(self._get_property(Network.JOYSTICK))

    @property
    def dial(self):
        return self._get_property(Network.DIAL)

    @property
    def left_slider(self):
        return self._get_property(Network.LEFT_SLIDER)

    @property
    def right_slider(self):
        return self._get_property(Network.RIGHT_SLIDER)

    @property
    def timer(self):
        return self._get_property(Network.TIMER) == 100

    @property
    def button_clicked(self):
        return self._get_property(Network.BUTTON_CLICK) == 100

    @property
    def button_double_clicked(self):
        return self._get_property(Network.BUTTON_DOUBLE_CLICK) == 100

    @property
    def button_toggled(self):
        return self._get_property(Network.TOGGLE) == 100

    def _set_property(self, command_type, value):
        self._conn.send(parse_message(
            0x04, command_type, self._id, (value, 0, 0, 0, 0, 0, 0, 0)
        ))

    def take_picture(self):
        self._set_property(Network.CAMERA, 100)

    def buzzer_on(self):
        self._set_property(Network.BUZZER, 100)

    def buzzer_off(self):
        self._set_property(Network.BUZZER, 0)
