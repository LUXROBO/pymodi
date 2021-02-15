"""IR module."""

from modi.module.input_module.input_module import InputModule


class Ir(InputModule):

    PROXIMITY = 2

    @property
    def proximity(self) -> float:
        """Returns the proximity value between 0 and 100

        :return: Distance to object.
        :rtype: float
        """
        return self._get_property(Ir.PROXIMITY)
