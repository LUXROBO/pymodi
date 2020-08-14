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

    BUZZER = 0x0003
    CAMERA = 0x0101

    def __init__(self, id_, uuid, conn_task):
        super().__init__(id_, uuid, conn_task)
        self.__buzzer_flag = True

    @property
    def button_pressed(self):
        """Returns whether MODI Play button is pressed

        :return: True is pressed
        :rtype: bool
        """
        return self._get_property(Network.BUTTON) == 100

    @property
    def joystick(self):
        """Returns the direction of the MODI Play joystick

        :return: 'up', 'down', 'left', 'right'
        :rtype: str
        """
        return {
            20.0: 'up',
            30.0: 'down',
            40.0: 'left',
            50.0: 'right',
        }.get(self._get_property(Network.JOYSTICK))

    @property
    def dial(self):
        """Returns the current degree of MODI Play dial

        :return: Current degree
        :rtype: int
        """
        return self._get_property(Network.DIAL)

    @property
    def left_slider(self):
        """Returns the current percentage of MODI Play left slider

        :return: Current percentage
        :rtype: int
        """
        return self._get_property(Network.LEFT_SLIDER)

    @property
    def right_slider(self):
        """Returns the current percentage of MODI Play right slider

        :return: Current percentage
        :rtype: int
        """
        return self._get_property(Network.RIGHT_SLIDER)

    @property
    def timer(self):
        """Returns if the MODI Play timer ticks

        :return: True if timer is up
        :rtype: bool
        """
        return self._get_property(Network.TIMER) == 100

    def _set_property(self, command_type, value):
        self._conn.send(parse_message(
            0x04, command_type, self._id, (value, 0, 0, 0, 0, 0, 0, 0)
        ))

    def take_picture(self):
        """Takes a picture on MODI Play

        :return: None
        """
        self._set_property(Network.CAMERA, 100)

    def buzzer_on(self):
        """Turns on MODI Play buzzer

        :return: None
        """
        if self.__buzzer_flag:
            self.buzzer_off()
            self.__buzzer_flag = False
        self._set_property(Network.BUZZER, 100)

    def buzzer_off(self):
        """Turns off MODI Play buzzer

        :return: None
        """
        self._set_property(Network.BUZZER, 0)
        self.__buzzer_flag = False
