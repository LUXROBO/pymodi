# -*- coding: utf-8 -*-

"""Json Excute module."""

from __future__ import absolute_import

import time
import json
import queue
import base64
import struct

from modi.module import (
    button,
    dial,
    display,
    env,
    gyro,
    ir,
    led,
    mic,
    motor,
    network,
    speaker,
    ultrasonic,
)


class ExcuteTask(object):

    categories = ["network", "input", "output"]
    types = {
        "network": ["usb", "usb/wifi/ble"],
        "input": ["env", "gyro", "mic", "button", "dial", "ultrasonic", "ir"],
        "output": ["display", "motor", "led", "speaker"],
    }

    def __init__(self, serial_write_q, recv_q, ids, modules, cmd):
        super(ExcuteTask, self).__init__()
        self._serial_write_q = serial_write_q
        self._recv_q = recv_q
        self._ids = ids
        self._modules = modules
        self._cmd = cmd

    def start_thread(self):
        try:
            msg = json.loads(self._recv_q.get_nowait())
        except queue.Empty:
            pass
        else:
            self.__handler(msg["c"])(msg)

        time.sleep(0.001)

    def __handler(self, cmd):
        return {
            0x00: self.__update_health,
            0x0A: self.__update_health,
            0x05: self.__update_modules,
            0x1F: self.__update_property,
        }.get(cmd, lambda _: None)

    def __update_health(self, msg):
        module_id = msg["s"]
        time_ms = int(time.time() * 1000)

        self._ids[module_id] = self._ids.get(module_id, dict())
        self._ids[module_id]["timestamp"] = time_ms
        self._ids[module_id]["uuid"] = self._ids[module_id].get("uuid", str())

        if not self._ids[module_id]["uuid"]:
            write_temp = self._cmd.request_uuid(module_id)
            self._serial_write_q.put(write_temp)
            write_temp = self._cmd.request_network_uuid(module_id)
            self._serial_write_q.put(write_temp)

        for module_id, info in list(self._ids.items()):
            # if module is not connected for 2s, set the module's state to not_connected
            if time_ms - info["timestamp"] > 2000:
                module = next(
                    (module for module in self._modules if module.uuid == info["uuid"]),
                    None,
                )
                if module:
                    module.set_connected(False)
                    print("disconecting : ", module)

    def __update_modules(self, msg):
        time_ms = int(time.time() * 1000)

        module_id = msg["s"]
        self._ids[module_id] = self._ids.get(module_id, dict())
        self._ids[module_id]["timestamp"] = time_ms
        self._ids[module_id]["uuid"] = self._ids[module_id].get("uuid", str())

        decoded = bytearray(base64.b64decode(msg["b"]))
        data1 = decoded[:4]
        data2 = decoded[-4:]

        info = (data2[1] << 8) + data2[0]
        # version = (data2[3] << 8) + data2[2]

        category_idx = info >> 13
        type_idx = (info >> 4) & 0x1FF

        category = self.categories[category_idx]
        type_ = self.types[category][type_idx]
        uuid = self.__append_hex(
            info, ((data1[3] << 24) + (data1[2] << 16) + (data1[1] << 8) + data1[0])
        )

        moduledict = self._ids[module_id]
        moduledict["uuid"] = uuid
        self._ids[module_id] = moduledict

        # handling re-connected modules
        for module in self._modules:
            if module.uuid == uuid and not module.connected:
                module.set_connected(True)

        # handling newly-connected modules
        if not next((module for module in self._modules if module.uuid == uuid), None):
            if category != "network":
                module = self.__init_module(type_)(
                    module_id, uuid, self, self._serial_write_q
                )
                self.__set_pnp(module_id=module.id, pnp_on=False)
                self._modules.append(module)
                # TODO: check why modules are sorted by its uuid
                self._modules.sort(key=lambda x: x.uuid)

    def __init_module(self, mtype):
        module = {
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
            "ultrasonic": ultrasonic.Ultrasonic,
        }.get(mtype)
        return module

    def __update_property(self, msg):
        property_number = msg["d"]
        if property_number == 0 or property_number == 1:
            return

        for module in self._modules:
            if module.id == msg["s"]:
                decoded = bytearray(base64.b64decode(msg["b"]))
                property_type = module.PropertyType(property_number)
                module.update_property(
                    property_type, round(struct.unpack("f", bytes(decoded[:4]))[0], 2)
                )

    def __set_pnp(self, module_id, pnp_on=False):
        state = self._cmd.ModulePnp.ON if pnp_on else self._cmd.ModulePnp.OFF
        if module_id is None:
            for _id in self._ids:
                pnp_temp = self._cmd.module_state(_id, self._cmd.ModuleState.RUN, state)
                self._serial_write_q.put(pnp_temp)
        else:
            pnp_temp = self._cmd.module_state(
                module_id, self._cmd.ModuleState.RUN, state
            )
            self._serial_write_q.put(pnp_temp)

    def __append_hex(self, a, b):
        sizeof_b = 0

        while (b >> sizeof_b) > 0:
            sizeof_b += 1
        sizeof_b += sizeof_b % 4
        return (a << sizeof_b) | b
