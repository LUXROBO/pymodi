import os
from typing import List

import serial.tools.list_ports as stl
from serial.tools.list_ports_common import ListPortInfo


def list_modi_ports() -> List[ListPortInfo]:
    """Returns a list of connected MODI ports

    :return: List[ListPortInfo]
    """

    def __is_modi_port(port):
        return (
            (port.manufacturer and port.manufacturer.upper() == "LUXROBO")
            or port.product in (
                "MODI Network Module",
                "MODI Network Module(BootLoader)",
                "STM32 Virtual ComPort",
                "STMicroelectronics Virtual COM Port",
            )
            or (port.vid == 0x2fde and port.pid == 0x2)
            or (port.vid == 0x483 and port.pid == 0x5740)
        )

    return [port for port in stl.comports() if __is_modi_port(port)]


def is_on_pi() -> bool:
    """Returns whether connected to pi

    :return: true if connected to pi
    :rtype: bool
    """
    return os.name != "nt" and os.uname()[4][:3] == "arm"


def is_network_module_connected() -> bool:
    """Returns whether network module is connected

    :return: true if connected
    :rtype: bool
    """
    return bool(list_modi_ports())


class MODIConnectionError(Exception):
    pass
