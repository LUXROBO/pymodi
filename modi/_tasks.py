# -*- coding: utf-8 -*-

"""Tasks."""

from __future__ import absolute_import

import modi._cmd as md_cmd 
from modi._stoppable_thread import StoppableThread
from modi._stoppable_proc import StoppableProc
from modi.serial import list_ports
from modi.module import *
import modi._util as md_util
from modi._threadpool import ThreadPool

import serial
import json
import weakref
import time
import base64
import struct
import multiprocessing 
from multiprocessing import Process, Queue, Pipe, Manager
import os
import threading
import queue


# Serial Task Work
# 1. Serial Read
# - put data serialqueue
# 3. get data writequeue
# - writedata serial

class SerialTask(object):
    def __init__(self, serial_read_q, serial_write_q, port):
        super(SerialTask, self).__init__()
        self._serial_read_q = serial_read_q
        self._serial_write_q = serial_write_q
        self._port = port
        #if os.name != 'nt':
        #    self.start_thread()
    
    def start_thread(self):
        # Sereial Connection Once
        if self._port is None:
            ports = list_ports()
            if len(ports) > 0:
                self._serial = serial.Serial(ports[0].device, 921600)
            else:
                raise serial.SerialException("No MODI network module connected.")
        else:
            self._serial = serial.Serial(port, 921600)
        
        # Main Thread 10ms loop
        while True:
            # read serial
            self.read_serial()
            # print('SerialTask',self._serial_read_q.qsize())
            # write serial
            self.write_serial()
            time.sleep(0.005)

##################################################################

    def read_serial(self):
        if self._serial.in_waiting != 0:
            read_temp = self._serial.read(self._serial.in_waiting).decode()
            self._serial_read_q.put(read_temp)
            # print(read_temp)

    def write_serial(self):

        try:
            writetemp = self._serial_write_q.get_nowait().encode()
        except queue.Empty:
            pass
        else:
            self._serial.write(writetemp)
            print(writetemp)
            time.sleep(0.001)

        # # # Write Display Data
        # try:
        #     writedisplaytemp = self._display_send_q.get_nowait().encode()
        # except queue.Empty:
        #     pass
        # else:
        #     self._serial.write(writedisplaytemp)
        #     time.sleep(0.001)


# Parsing Task Work
#1. Get queue serial read queue
#2. Json Box Add
#3. Put queue json recv_q

class ParsingTask(object):
    def __init__(self, serial_read_q, recv_q, json_box):
        super(ParsingTask, self).__init__()
        self._serial_read_q = serial_read_q
        self._recv_q = recv_q
        self._json_box = json_box
        #if os.name != 'nt':
        #    self.start_thread()
    
    def start_thread(self):
        while True:
            self.adding_json()

            time.sleep(0.005)

    def adding_json(self):
        try:
            self._json_box.add(self._serial_read_q.get(False))
        except:
            pass

        while self._json_box.has_json():
            json_temp = self._json_box.json
            self._recv_q.put(json_temp)
            #print('jsonread : ', json_temp)
        

class ExcuteTask(object):

    categories = ["network", "input", "output"]

    types = {
        "network": ["usb", "usb/wifi/ble"],
        "input": ["env", "gyro", "mic", "button", "dial", "ultrasonic", "ir"],
        "output": ["display", "motor", "led", "speaker"]
        }
    # _modules = list()

    def __init__(self, serial_write_q, recv_q, ids, modules):
        super(ExcuteTask, self).__init__()
        self._serial_write_q = serial_write_q
        self._recv_q = recv_q
        self._ids = ids
        self._modules = modules
        #if os.name != 'nt':
        #    self.start_thread()
    
    def start_thread(self):
        while True:
            # msg = json.loads(self._recv_q.get_nowait())
            try:
                msg = json.loads(self._recv_q.get_nowait())
            except queue.Empty:
                pass
            else:
                self._handler(msg['c'])(msg)
            #print('ExcuteTask!!!!')
            time.sleep(0.002)

    def _handler(self, cmd):
        return {
            0x00: self._update_health,
            0x0A: self._update_health,
            0x05: self._update_modules,
            0x1F: self._update_property
        }.get(cmd, lambda _: None)
        
    def _update_health(self, msg):

        id = msg['s']
        time_ms = int(time.time() * 1000)

        self._ids[id] = self._ids.get(id, dict())
        moduledict = self._ids[id]
        moduledict['timestamp'] = time_ms
        moduledict['uuid'] = self._ids[id].get('uuid', str())
        self._ids[id] = moduledict

        if not self._ids[id]['uuid']:
            write_temp = md_cmd.request_uuid(id)
            self._serial_write_q.put(write_temp)
            write_temp = md_cmd.request_network_uuid(id)
            self._serial_write_q.put(write_temp)

        for id, info in list(self._ids.items()):
            # if module is not connected for 3.5s, set the module's state to not_connected
            if time_ms - info['timestamp'] > 3500:
                module = next((module for module in self._modules if module.uuid == info['uuid']), None)
                if module:
                    module.set_connected(False)
                    # print('disconecting')

    def _update_modules(self, msg):

        time_ms = int(time.time() * 1000)

        id = msg['s']
        self._ids[id] = self._ids.get(id, dict())
        moduledict = self._ids[id]
        moduledict['timestamp'] = time_ms
        moduledict['uuid'] = self._ids[id].get('uuid', str())
        self._ids[id] = moduledict

        decoded = bytearray(base64.b64decode(msg['b']))
        data1 = decoded[:4]
        data2 = decoded[-4:]

        info = (data2[1] << 8) + data2[0]
        version = (data2[3] << 8) + data2[2]

        category_idx = info >> 13
        type_idx = (info >> 4) & 0x1FF

        category = self.categories[category_idx]
        type_ = self.types[category][type_idx]
        uuid = md_util.append_hex(info, (data1[3] << 24) + (data1[2] << 16) + (data1[1] << 8) + data1[0])

        moduledict = self._ids[id]
        moduledict['uuid'] = uuid
        self._ids[id] = moduledict

        # handling re-connected modules
        for module in self._modules:
            if module.uuid == uuid and not module.connected:
                module.set_connected(True)

        # handling newly-connected modules
        if not next((module for module in self._modules if module.uuid == uuid), None):
            if category != "network":
                # print(type_)
                module = self._init_module(type_)(id, uuid, self, self._serial_write_q)
                self.pnp_off(module.id)
                self._modules.append(module)
                self._modules.sort(key=lambda x: x.uuid)

     

        #     # TODO: check why modules are sorted by its uuid
        #     # self._modules.sort(key=lambda x: x.uuid)

    def _init_module(self, type_):
        return {
            "button": button.Button,
            "dial": dial.Dial,
            "display": display.Display,
            "env": env.Env,
            "gyro": gyro.Gyro,
            "ir": ir.Ir,
            "led": led.Led,
            "mic": mic.Mic,
            "motor": motor.Motor,
            "speaker": speaker.Speaker,
            "ultrasonic": ultrasonic.Ultrasonic
        }.get(type_, None)
    
    def _update_property(self, msg):

        property_number = msg['d']
        # print(property_number)
        if property_number == 0 or property_number == 1:
            return
        
        id = msg['s']
        module = next((module for module in self._modules if module.id == id), None)
        # print(module)
        if module:
            decoded = bytearray(base64.b64decode(msg['b']))
            property_type = module.property_types(property_number)
            module.update_property(property_type, round(struct.unpack('f', bytes(decoded[:4]))[0], 2))

    def pnp_on(self, id=None):
        """Turn on PnP mode of the module.

        :param int id: The id of the module to turn on PnP mode or ``None``.

        All connected modules' PnP mode will be turned on if the `id` is ``None``.
        """
        if id is None:
            for _id in self._ids:
                # self.write(md_cmd.module_state(_id, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.ON))
                pnp_temp = md_cmd.module_state(_id, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.ON)
                self._serial_write_q.put(pnp_temp)
        else:
            # self.write(md_cmd.module_state(id, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.ON))
            pnp_temp = md_cmd.module_state(id, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.ON)
            self._serial_write_q.put(pnp_temp)

    def pnp_off(self, id=None):
        """Turn off PnP mode of the module.

        :param int id: The id of the module to turn off PnP mode or ``None``.

        All connected modules' PnP mode will be turned off if the `id` is ``None``.
        """
        if id is None:
            for _id in self._ids:
                pnp_temp = md_cmd.module_state(_id, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.OFF)
                self._serial_write_q.put(pnp_temp)
        else:
            pnp_temp = md_cmd.module_state(id, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.OFF)
            self._serial_write_q.put(pnp_temp)
