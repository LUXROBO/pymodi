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


class ExcutableTask(object):

    # variables shared across all class instances
    module_categories = ["network", "input", "output"]
    module_types = {
        "network": ["usb", "usb/wifi/ble"],
        "input": ["env", "gyro", "mic", "button", "dial", "ultrasonic", "ir"],
        "output": ["display", "motor", "led", "speaker"],
    }

    def __init__(self, serial_write_q, recv_q, module_ids, modules, command):
        super(ExcutableTask, self).__init__()
        self._serial_write_q = serial_write_q
        self._recv_q = recv_q
        self._module_ids = module_ids
        self._modules = modules
        self._command = command

    def start_thread(self):
        try:
            msg = json.loads(self._recv_q.get_nowait())
        except queue.Empty:
            pass
        else:
            self.__handler(msg["c"])(msg)
            time.sleep(0.004)

    def __handler(self, command):
        return {
            0x00: self.__update_health,
            0x0A: self.__update_health,
            0x05: self.__update_modules,
            0x1F: self.__update_property,
        }.get(command, lambda _: None)

    def __update_health(self, msg):
        module_id = msg["s"]
        current_time_ms = int(time.time() * 1000)
        msg_decoded = bytearray(base64.b64decode(msg["b"]))

        self._module_ids[module_id] = self._module_ids.get(module_id, dict())
        self._module_ids[module_id]["timestamp"] = current_time_ms
        self._module_ids[module_id]["uuid"] = self._module_ids[module_id].get(
            "uuid", str()
        )
        self._module_ids[module_id]["battery"] = int(msg_decoded[3])

        if not self._module_ids[module_id]["uuid"]:
            msg_to_write = self._command.request_uuid(
                module_id, is_network_module=False
            )
            self._serial_write_q.put(msg_to_write)
            msg_to_write = self._command.request_uuid(module_id, is_network_module=True)
            self._serial_write_q.put(msg_to_write)

        for module_id, info in list(self._module_ids.items()):
            if current_time_ms - info["timestamp"] > 2000:
                for module in self._modules:
                    if module.uuid == info["uuid"]:
                        module.set_connection_state(
                            state=module.ConnectionState.CONNECTED
                        )
                        print("disconnecting : ", module)

    def __update_modules(self, msg):
        time_ms = int(time.time() * 1000)

        module_id = msg["s"]
        self._module_ids[module_id] = self._module_ids.get(module_id, dict())
        self._module_ids[module_id]["timestamp"] = time_ms
        self._module_ids[module_id]["uuid"] = self._module_ids[module_id].get(
            "uuid", str()
        )

        msg_decoded = bytearray(base64.b64decode(msg["b"]))
        module_uuid_bytes = msg_decoded[:4]
        module_info_bytes = msg_decoded[-4:]

        module_info = (module_info_bytes[1] << 8) + module_info_bytes[0]

        module_category_idx = module_info >> 13
        module_type_idx = (module_info >> 4) & 0x1FF

        category = self.module_categories[module_category_idx]
        module_type = self.module_types[category][module_type_idx]
        module_uuid = self.__append_hex(
            module_info,
            (
                (module_uuid_bytes[3] << 24)
                + (module_uuid_bytes[2] << 16)
                + (module_uuid_bytes[1] << 8)
                + module_uuid_bytes[0]
            ),
        )

        self._module_ids[module_id]["uuid"] = module_uuid

        # handling re-connected modules
        for module in self._modules:
            if module.uuid == module_uuid and not module.connected:
                module.set_connection_state(state=module.ConnectionState.CONNECTED)

        # handling newly-connected modules
        if not next(
            (module for module in self._modules if module.uuid == module_uuid), None
        ):
            if category != "network":
                module_template = self.__init_module(module_type)
                module_instance = module_template(
                    module_id, module_uuid, self, self._serial_write_q
                )

                self.__set_pnp(
                    module_id=module_instance.id,
                    module_pnp_state=self._command.ModulePnp.OFF,
                )
                self._modules.append(module_instance)
                self._modules.sort(key=lambda module: module.uuid)

    def __init_module(self, module_type):
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
        }.get(module_type)
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

    def __set_pnp(self, module_id, module_pnp_state):
        # pnp_state = (
        #    self._command.ModulePnp.ON if pnp_on else self._command.ModulePnp.OFF
        # )
        if module_id is None:
            for curr_module_id in self._module_ids:
                msg_to_write = self._command.set_module_state(
                    curr_module_id, self._command.ModuleState.RUN, module_pnp_state
                )
                self._serial_write_q.put(msg_to_write)
        else:
            msg_to_write = self._command.set_module_state(
                module_id, self._command.ModuleState.RUN, module_pnp_state
            )
            self._serial_write_q.put(msg_to_write)

    def __append_hex(self, a, b):
        sizeof_b = 0
        while (b >> sizeof_b) > 0:
            sizeof_b += 1
        sizeof_b += sizeof_b % 4
        return (a << sizeof_b) | b
