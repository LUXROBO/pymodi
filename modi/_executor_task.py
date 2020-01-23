# -*- coding: utf-8 -*-

"""Json Excute module."""

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

from modi.module.module import Module


class ExecutorTask:
    """
    This task execute incoming commands
    """

    # variables shared across all class instances
    module_categories = ["network", "input", "output"]
    module_types = {
        "network": ["usb", "usb/wifi/ble"],
        "input": ["env", "gyro", "mic", "button", "dial", "ultrasonic", "ir"],
        "output": ["display", "motor", "led", "speaker"],
    }

    def __init__(self, serial_write_q, json_recv_q, module_ids, modules):
        super(ExecutorTask, self).__init__()
        self._serial_write_q = serial_write_q
        self._json_recv_q = json_recv_q
        self._module_ids = module_ids
        self._modules = modules

    def start_thread(self):
        try:
            message = json.loads(self._json_recv_q.get_nowait())
        except queue.Empty:
            pass
        else:
            self.__handler(message["c"])(message)
            time.sleep(0.004)

    def __handler(self, command):
        return {
            0x00: self.__update_health,
            0x0A: self.__update_health,
            0x05: self.__update_modules,
            0x1F: self.__update_property,
        }.get(command, lambda _: None)

    def __update_health(self, message):
        module_id = message["s"]
        curr_time_ms = int(time.time() * 1000)
        message_decoded = bytearray(base64.b64decode(message["b"]))

        self._module_ids[module_id] = self._module_ids.get(module_id, dict())
        self._module_ids[module_id]["timestamp"] = curr_time_ms
        self._module_ids[module_id]["uuid"] = self._module_ids[module_id].get(
            "uuid", str()
        )
        self._module_ids[module_id]["battery"] = int(message_decoded[3])

        if not self._module_ids[module_id]["uuid"]:
            message_to_write = self.__request_uuid(module_id, is_network_module=False)
            self._serial_write_q.put(message_to_write)
            message_to_write = self.__request_uuid(module_id, is_network_module=True)
            self._serial_write_q.put(message_to_write)

        for module_id, module_info in list(self._module_ids.items()):
            if curr_time_ms - module_info["timestamp"] > 2000:
                for module in self._modules:
                    if module.uuid == module_info["uuid"]:
                        module.set_connection_state(state=True)
                        print("disconnecting : ", module)

    def __update_modules(self, message):
        curr_time_ms = int(time.time() * 1000)

        module_id = message["s"]
        self._module_ids[module_id] = self._module_ids.get(module_id, dict())
        self._module_ids[module_id]["timestamp"] = curr_time_ms
        self._module_ids[module_id]["uuid"] = self._module_ids[module_id].get(
            "uuid", str()
        )

        message_decoded = bytearray(base64.b64decode(message["b"]))
        module_uuid_bytes = message_decoded[:4]
        module_info_bytes = message_decoded[-4:]

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
                module.set_connection_state(state=True)

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
                    module_id=module_instance.id, module_pnp_state=Module.ModulePnp.OFF
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

    def __update_property(self, message):
        # TODO: comment
        property_number = message["d"]
        if property_number == 0 or property_number == 1:
            return

        # TODO: comment
        for module in self._modules:
            if module.id == message["s"]:
                decoded = bytearray(base64.b64decode(message["b"]))
                property_type = module.PropertyType(property_number)
                module.update_property(
                    property_type, round(struct.unpack("f", bytes(decoded[:4]))[0], 2)
                )

    def __set_pnp(self, module_id, module_pnp_state):
        # if no module_id is specified, it will broadcast incoming pnp state
        if module_id is None:
            for curr_module_id in self._module_ids:
                message_to_write = self.__set_module_state(
                    curr_module_id, Module.ModuleState.RUN, module_pnp_state
                )
                self._serial_write_q.put(message_to_write)
        # otherwise, it sets pnp state of the given module
        else:
            message_to_write = self.__set_module_state(
                module_id, Module.ModuleState.RUN, module_pnp_state
            )
            self._serial_write_q.put(message_to_write)

    def __append_hex(self, a, b):
        # TODO: comment
        sizeof_b = 0
        while (b >> sizeof_b) > 0:
            sizeof_b += 1
        sizeof_b += sizeof_b % 4
        return (a << sizeof_b) | b

    def __set_module_state(self, dst_id, module_state, pnp_state):
        if type(module_state) is Module.ModuleState:
            message = dict()

            message["c"] = 0x09
            message["s"] = 0
            message["d"] = dst_id

            state_bytes = bytearray(2)
            state_bytes[0] = module_state.value
            state_bytes[1] = pnp_state.value

            message["b"] = base64.b64encode(bytes(state_bytes)).decode("utf-8")
            message["l"] = 2

            return json.dumps(message, separators=(",", ":"))
        else:
            raise RuntimeError("The type of state is not ModuleState")

    def init_modules(self):
        BROADCAST_ID = 0xFFF

        message_to_send = self.__set_module_state(
            BROADCAST_ID, Module.ModuleState.REBOOT, Module.ModulePnp.OFF
        )
        self._serial_write_q.put(message_to_send)
        self.__delay()

        message_to_send = self.__set_module_state(
            BROADCAST_ID, Module.ModuleState.RUN, Module.ModulePnp.OFF
        )
        self._serial_write_q.put(message_to_send)
        self.__delay()

        message_to_send = self.__request_uuid(BROADCAST_ID)
        self._serial_write_q.put(message_to_send)
        self.__delay()

    def __delay(self):
        time.sleep(1)

    def __request_uuid(self, source_id, is_network_module=False):
        BROADCAST_ID = 0xFFF

        message = dict()
        message["c"] = 0x28 if is_network_module else 0x08
        message["s"] = source_id
        message["d"] = BROADCAST_ID

        id_bytes = bytearray(8)
        id_bytes[0] = 0xFF
        id_bytes[1] = 0x0F

        message["b"] = base64.b64encode(bytes(id_bytes)).decode("utf-8")
        message["l"] = 8

        return json.dumps(message, separators=(",", ":"))
