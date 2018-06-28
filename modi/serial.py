# -*- coding: utf-8 -*-
import serial.tools.list_ports

def list_ports():
    ports = serial.tools.list_ports.comports()
    modis = list()

    for port in ports:
        if port.manufacturer == "LUXROBO" and port.product == "MODI Network Module":
            modis.append(port)

    return modis
