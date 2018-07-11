# -*- coding: utf-8 -*-

"""Serial module."""

from __future__ import absolute_import

import serial 
import serial.tools.list_ports as stl 

def list_ports():
    ports = stl.comports()
    modi_ports = list()

    for port in ports:
        if port.manufacturer == "LUXROBO" and port.product == "MODI Network Module":
            modi_ports.append(port.device)

    return modi_ports
