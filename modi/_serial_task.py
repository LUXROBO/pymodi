# -*- coding: utf-8 -*-

"""Serial Task module."""

from __future__ import absolute_import

import time
import serial
import serial.tools.list_ports as stl

from queue import Empty


class SerialTask(object):
    def __init__(self, serial_read_q, serial_write_q, port):
        super(SerialTask, self).__init__()
        self._serial_read_q = serial_read_q
        self._serial_write_q = serial_write_q
        self.__port = port

    def list_ports(self):
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
            if (
                port.manufacturer == "LUXROBO"
                or port.product == "MODI Network Module"
                or port.description == "MODI Network Module"
                or (port.vid == 12254 and port.pid == 2)
            ):
                modi_ports.append(port)

        return modi_ports

    def open_serial(self):
        if self.__port is None:
            ports = self.list_ports()
            if len(ports) > 0:
                self._serial = serial.Serial(ports[0].device, 921600)
            else:
                raise serial.SerialException("No MODI network module connected.")
        else:
            self._serial = serial.Serial(self.__port, 921600)

    def close_serial(self):
        self._serial.close()

    def start_thread(self):
        self.__read_serial()
        self.__write_serial()
        time.sleep(0.008)

    ##################################################################

    def __read_serial(self):
        if self._serial.in_waiting != 0:
            msg_to_read = self._serial.read(self._serial.in_waiting).decode()
            self._serial_read_q.put(msg_to_read)

    def __write_serial(self):
        try:
            msg_to_write = self._serial_write_q.get_nowait().encode()
        except Empty:
            pass
        else:
            self._serial.write(msg_to_write)
