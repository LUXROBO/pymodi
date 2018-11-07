# -*- coding: utf-8 -*-

"""Serial module."""

from __future__ import absolute_import

import serial 
import serial.tools.list_ports as stl 

def list_ports():
    """
    :return: an iterable that yields :py:class:`~serial.tools.list_ports.ListPortInfo` objects.

    The function returns an iterable that yields tuples of three strings:

    * port name as it can be passed to :py:class:`modi.modi.MODI`
    * description in human readable form
    * sort of hardware ID. E.g. may contain VID:PID of USB-serial adapters.

    Items are returned in no particular order. It may make sense to sort the items. Also note that the reported strings are different across platforms and operating systems, even for the same device.
    
    .. note:: Support is limited to a number of operating systems. On some systems description and hardware ID will not be available (``None``).

    :platform: Posix (/dev files)
    :platform: Linux (/dev files, sysfs)
    :platform: OSX (iokit)
    :platform: Windows (setupapi, registry)
    """
    ports = stl.comports()
    modi_ports = list()

    for port in ports:
        if port.manufacturer == "LUXROBO" or port.product == "MODI Network Module" or port.description == "MODI Network Module" or (port.vid == 12254 and port.pid == 2): 
            modi_ports.append(port)

    return modi_ports
