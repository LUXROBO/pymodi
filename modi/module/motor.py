# -*- coding: utf-8 -*-

"""Motor module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import OutputModule

from modi._cmd import set_property

class PropertyType(Enum):
    FIRST_DEGREE = 4
    SECOND_DEGREE = 12
    FIRST_SPEED = 3
    SECOND_SPEED = 11
    FIRST_TORQUE = 2
    SECOND_TORQUE = 10

class Motor(OutputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Motor, self).__init__(id, uuid, modi)
        self._type = "motor"

    def first_degree(self, degree=None):
        """
        :param int degree: Angle to set the first motor.

        If *degree* is ``None``,

        :return: Angle of the first motor.
        :rtype: float
        """
        if degree != None:
            self._modi().write(set_property(self.id, 18, (degree, self.second_degree(), 0)))
        else:
            return self._properties[PropertyType.FIRST_DEGREE]

    def second_degree(self, degree=None):
        """
        :param int degree: Angle to set the second motor.

        If *degree* is ``None``,

        :return: Angle of the second motor.
        :rtype: float
        """
        if degree != None:
            self._modi().write(set_property(self.id, 18, (self.first_degree(), degree, 0)))
        else:
            return self._properties[PropertyType.SECOND_DEGREE]

    def first_speed(self, speed=None):
        """
        :param int degree: Angular speed to set the first motor.

        If *speed* is ``None``,

        :return: Angular speed of the first motor.
        :rtype: float
        """
        if speed != None:
            self._modi().write(set_property(self.id, 17, (speed, self.second_speed(), 0)))
        else:
            return self._properties[PropertyType.FIRST_SPEED]

    def second_speed(self, speed=None):
        """
        :param int degree: Angular speed to set the second motor.

        If *speed* is ``None``,

        :return: Angular speed of the second motor.
        :rtype: float
        """
        if speed != None:
            self._modi().write(set_property(self.id, 17, (self.first_speed(), speed, 0)))
        else:    
            return self._properties[PropertyType.SECOND_SPEED]

    def first_torque(self, torque=None):
        """
        :param int degree: Torque to set the first motor.

        If *torque* is ``None``,

        :return: Torque of the first motor.
        :rtype: float
        """
        if torque != None:
            self._modi().write(set_property(self.id, 16, (torque, self.second_torque(), 0)))
        else:
            return self._properties[PropertyType.FIRST_TORQUE]

    def second_torque(self, torque=None):
        """
        :param int degree: Torque to set the second motor.

        If *torque* is ``None``,

        :return: Torque of the second motor.
        :rtype: float
        """
        if torque != None:
            self._modi().write(set_property(self.id, 16, (self.first_torque(), torque, 0)))
        else:
            return self._properties[PropertyType.SECOND_TORQUE]
        
    def torque(self, first_torque=None, second_torque=None):
        """
        :param int first_torque: Torque to set the first motor.
        :param int second_torque: Torque to set the second motor.

        If *first_torque* is ``None`` and *second_torque* is ``None``,

        :return: Torque of the first motor , Torque of the second motor.
        :rtype: float
        """
        if first_torque != None or second_torque != None :
            first_torque = self.first_torque() if first_torque == None else first_torque
            second_torque = self.second_torque() if second_torque == None else second_torque
            self._modi().write(set_property(self.id, 16, (first_torque, second_torque, 0)))
        else:
            return (self._properties[PropertyType.FIRST_TORQUE] , self._properties[PropertyType.SECOND_TORQUE])

    def speed(self, first_speed=None, second_speed=None):
        """
        :param int first_speed: Speed to set the first motor.
        :param int second_speed: Speed to set the second motor.

        If *first_speed* is ``None`` and *second_speed* is ``None``,

        :return: Speed of the first motor , Speed of the second motor.
        :rtype: float
        """
        if first_speed != None or second_speed != None :
            first_speed = self.first_speed() if first_speed == None else first_speed
            second_speed = self.second_speed() if second_speed == None else second_speed
            self._modi().write(set_property(self.id, 17, (first_speed, second_speed, 0)))
        else:
            return (self._properties[PropertyType.FIRST_SPEED] , self._properties[PropertyType.SECOND_SPEED])
            
    def degree(self, first_degree=None, second_degree=None):
        """
        :param int first_degree: Degree to set the first motor.
        :param int second_degree: Degree to set the second motor.

        If *first_degree* is ``None`` and *second_degree* is ``None``,

        :return: Degree of the first motor , Degree of the second motor.
        :rtype: float
        """
        if first_degree != None or second_degree != None :
            first_degree = self.first_degree() if first_degree == None else first_degree
            second_degree = self.second_degree() if second_degree == None else second_degree
            self._modi().write(set_property(self.id, 18, (first_degree, second_degree, 0)))
        else:
            return (self._properties[PropertyType.FIRST_DEGREE] , self._properties[PropertyType.SECOND_DEGREE])
