# -*- coding: utf-8 -*-

"""Json Excute module."""

from __future__ import absolute_import

import time
import json
import modi._cmd as md_cmd
from modi.module import *
import base64
import struct
import queue


class ExcuteTask(object):

    categories = ["network", "input", "output"]
    types = {
        "network": ["usb", "usb/wifi/ble"],
        "input": ["env", "gyro", "mic", "button", "dial", "ultrasonic", "ir"],
        "output": ["display", "motor", "led", "speaker"],
    }
    # _modules = list()

    def __init__(self, serial_write_q, recv_q, ids, modules):
        super(ExcuteTask, self).__init__()
        self._serial_write_q = serial_write_q
        self._recv_q = recv_q
        self._ids = ids
        self._modules = modules

    def start_thread(self):

        try:
            msg = json.loads(self._recv_q.get_nowait())
        except queue.Empty:
            pass
        else:
            self._handler(msg["c"])(msg)

        time.sleep(0.001)

    def _handler(self, cmd):
        return {
            0x00: self._update_health,
            0x0A: self._update_health,
            0x05: self._update_modules,
            0x1F: self._update_property,
        }.get(cmd, lambda _: None)

    def _update_health(self, msg):

        module_id = msg["s"]
        time_ms = int(time.time() * 1000)

        # TODO : manager().dict -> dict()
        self._ids[module_id] = self._ids.get(module_id, dict())
        self._ids[module_id]["timestamp"] = time_ms
        self._ids[module_id]["uuid"] = self._ids[module_id].get("uuid", str())
        # moduledict = self._ids[module_id]
        # moduledict["timestamp"] = time_ms
        # moduledict["uuid"] = self._ids[module_id].get("uuid", str())
        # self._ids[module_id] = moduledict

        if not self._ids[module_id]["uuid"]:
            write_temp = md_cmd.request_uuid(module_id)
            self._serial_write_q.put(write_temp)
            write_temp = md_cmd.request_network_uuid(module_id)
            self._serial_write_q.put(write_temp)

        for module_id, info in list(self._ids.items()):
            # if module is not connected for 3.5s, set the module's state to not_connected
            if time_ms - info["timestamp"] > 2000:
                module = next(
                    (module for module in self._modules if module.uuid == info["uuid"]),
                    None,
                )
                if module:
                    module.set_connected(False)
                    print("disconecting : ", module)

    def _update_modules(self, msg):

        time_ms = int(time.time() * 1000)

        # TODO : manager().dict -> dict()
        # TODO : id -> module_id
        module_id = msg["s"]
        self._ids[module_id] = self._ids.get(module_id, dict())
        self._ids[module_id]["timestamp"] = time_ms
        self._ids[module_id]["uuid"] = self._ids[module_id].get("uuid", str())
        # moduledict = self._ids[module_id]
        # moduledict["timestamp"] = time_ms
        # moduledict["uuid"] = self._ids[module_id].get("uuid", str())
        # self._ids[module_id] = moduledict

        decoded = bytearray(base64.b64decode(msg["b"]))
        data1 = decoded[:4]
        data2 = decoded[-4:]

        info = (data2[1] << 8) + data2[0]
        version = (data2[3] << 8) + data2[2]

        category_idx = info >> 13
        type_idx = (info >> 4) & 0x1FF

        category = self.categories[category_idx]
        type_ = self.types[category][type_idx]
        uuid = self.append_hex(
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
                # print(type_)
                module = self._init_module(type_)(
                    module_id, uuid, self, self._serial_write_q
                )
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
            "ultrasonic": ultrasonic.Ultrasonic,
        }.get(type_, None)

    def _update_property(self, msg):

        property_number = msg["d"]
        # print(property_number)
        if property_number == 0 or property_number == 1:
            return

        module_id = msg["s"]
        module = next(
            (module for module in self._modules if module.id == module_id), None
        )
        # print(module)
        if module:
            decoded = bytearray(base64.b64decode(msg["b"]))
            property_type = module.property_types(property_number)
            module.update_property(
                property_type, round(struct.unpack("f", bytes(decoded[:4]))[0], 2)
            )

    def pnp_on(self, module_id=None):
        """Turn on PnP mode of the module.

        :param int id: The id of the module to turn on PnP mode or ``None``.

        All connected modules' PnP mode will be turned on if the `id` is ``None``.
        """
        if module_id is None:
            for _id in self._ids:
                # self.write(md_cmd.module_state(_id, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.ON))
                pnp_temp = md_cmd.module_state(
                    _id, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.ON
                )
                self._serial_write_q.put(pnp_temp)
        else:
            # self.write(md_cmd.module_state(id, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.ON))
            pnp_temp = md_cmd.module_state(
                module_id, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.ON
            )
            self._serial_write_q.put(pnp_temp)

    def pnp_off(self, module_id=None):
        """Turn off PnP mode of the module.

        :param int id: The id of the module to turn off PnP mode or ``None``.

        All connected modules' PnP mode will be turned off if the `id` is ``None``.
        """
        if module_id is None:
            for _id in self._ids:
                pnp_temp = md_cmd.module_state(
                    _id, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.OFF
                )
                self._serial_write_q.put(pnp_temp)
        else:
            pnp_temp = md_cmd.module_state(
                module_id, md_cmd.ModuleState.RUN, md_cmd.ModulePnp.OFF
            )
            self._serial_write_q.put(pnp_temp)

    def append_hex(self, a, b):
        sizeof_b = 0

        while (b >> sizeof_b) > 0:
            sizeof_b += 1
        sizeof_b += sizeof_b % 4
        return (a << sizeof_b) | b
