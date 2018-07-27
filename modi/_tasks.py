# -*- coding: utf-8 -*-

"""Tasks."""

from __future__ import absolute_import

import modi._cmd as md_cmd 
from modi._stoppable_thread import StoppableThread
from modi.serial import list_ports
from modi.module import *
import modi._util as md_util 
from modi._json_box import JsonBox
from modi._threadpool import ThreadPool

import json
import weakref
import time
import base64
import struct

class MODITask(StoppableThread):
    def __init__(self, modi):
        super(MODITask, self).__init__()
        self._modi = weakref.ref(modi)

class ReadDataTask(MODITask):
    def __init__(self, modi):
        super(ReadDataTask, self).__init__(modi)

    def run(self):
        modi = self._modi()
        json_box = JsonBox()

        while not self.stopped():
            try:
                waiting = modi._serial.in_waiting
                json_box.add(modi._serial.read(waiting).decode("utf-8"))

                while json_box.has_json():
                    modi._recv_q.put(json_box.json)
            except:
                pass

class ProcDataTask(MODITask):
    categories = ["network", "input", "output"]

    types = {
        "network": ["usb", "usb/wifi/ble"],
        "input": ["env", "gyro", "mic", "button", "dial", "ultrasonic", "ir"],
        "output": ["display", "motor", "led", "speaker"]
        }

    def __init__(self, modi):
        super(ProcDataTask, self).__init__(modi)

    def run(self):
        modi = self._modi()
        pool = ThreadPool(10)

        while not self.stopped():
            try:
                msg = json.loads(modi._recv_q.get())
                pool.add_task(self._handler(msg['c']), msg)
            except: 
                pass
        
        pool.wait_completion()

    def _handler(self, cmd):
        return {
            0x00: self._update_health,
            0x0A: self._update_health,
            0x05: self._update_modules,
            0x1F: self._update_property
        }.get(cmd, lambda _: None)

    def _update_health(self, msg):
        modi = self._modi()

        id = msg['s']
        time_ms = int(time.time() * 1000)

        modi._ids[id] = modi._ids.get(id, dict())
        modi._ids[id]['timestamp'] = time_ms
        modi._ids[id]['uuid'] = modi._ids[id].get('uuid', str())

        if not modi._ids[id]['uuid']:
            modi.write(md_cmd.request_uuid(id))

        for id, info in list(modi._ids.items()):
            if time_ms - info['timestamp'] > 3500:
                del modi._ids[id]

                module = next((module for module in modi.modules if module.uuid == info['uuid']), None)

                if module:
                    modi._modules.remove(module)
 
    def _update_modules(self, msg):
        modi = self._modi()

        id = msg['s']
        time_ms = int(time.time() * 1000)

        modi._ids[id] = modi._ids.get(id, dict())
        modi._ids[id]['timestamp'] = time_ms
        modi._ids[id]['uuid'] = modi._ids[id].get('uuid', str())

        decoded = bytearray(base64.b64decode(msg['b']))
        data1 = decoded[:4]
        data2 = decoded[-4:]

        info = (data2[1] << 8) + data2[0]
        version = (data2[3] << 8) + data2[2]

        category_idx = info >> 13
        type_idx = (info >> 4) & 0x1FF

        category = self.categories[category_idx]
        type = self.types[category][type_idx]
        uuid = md_util.append_hex(info, (data1[3] << 24) + (data1[2] << 16) + (data1[1] << 8) + data1[0])

        modi._ids[id]['uuid'] = uuid
        
        if not next((module for module in modi.modules if module.uuid == uuid), None):
            module = self._init_module(type)(id, uuid, modi)
            
            modi.pnp_off(module.id)
            modi._modules.append(module)
            modi._modules.sort(key=lambda x: x.uuid)

            for property_type in module.property_types:
                modi.write(md_cmd.get_property(module.id, property_type.value))

    def _init_module(self, type):
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
        }.get(type, lambda _: None)
    
    def _update_property(self, msg):
        modi = self._modi()

        try:
            property_number = msg['d']

            if property_number == 0 or property_number == 1:
                return

            id = msg['s']
            decoded = bytearray(base64.b64decode(msg['b']))

            module = next((module for module in modi.modules if module.id == id), None)

            if module:
                property_type = module.property_types(property_number)
                module._properties[property_type] = round(struct.unpack('f', bytes(decoded[:4]))[0], 2)
        except:
            pass

class WriteDataTask(MODITask):
    def __init__(self, modi):
        super(WriteDataTask, self).__init__(modi)

    def run(self):
        modi = self._modi()

        while not self.stopped():
            try:
                time.sleep(0.001)
                modi._serial.write(modi._send_q.get().encode())
            except: 
                pass
