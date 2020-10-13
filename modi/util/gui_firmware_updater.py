import os
import random

import threading as th


from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

from modi.util.firmware_updater import STM32FirmwareUpdater
from modi.util.firmware_updater import ESP32FirmwareUpdater


class Form(QtWidgets.QDialog):
    """
    GUI Form of MODI Firmware Updater
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        ui_path = (
            os.path.join(
                os.path.dirname(__file__),
                '../assets', 'modi_firmware_updater.ui'
            )
        )
        self.ui = uic.loadUi(ui_path)
        self.ui.setWindowTitle("MODI Firmware Updater")
        self.ui.show()

        # Connect up the buttons
        self.ui.update_network_esp32.clicked.connect(self.update_network_esp32)
        self.ui.update_stm32_modules.clicked.connect(self.update_stm32_modules)
        self.ui.update_network_stm32.clicked.connect(self.update_network_stm32)
        self.ui.update_network_esp32.setFocus(False)
        self.ui.update_stm32_modules.setFocus(False)
        self.ui.update_network_stm32.setFocus(False)

        self.ui.push_button.clicked.connect(self.push)
        self.ui.push_button.setFocus(True)

        # Init module image
        module_pixmap = QPixmap(
            os.path.join(
                os.path.dirname(__file__), '../assets/image', 'network.png'
            )
        )
        self.ui.curr_module_img.setPixmap(module_pixmap)

        # Init password field for enabling developer mode
        self.ui.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.password_field.returnPressed.connect(self.process_password)

        # Set up field variables
        self.firmware_updater = None
        self.dev_mode = False

    def push(self):
        curr_val = self.ui.push_bar.value()
        self.ui.push_bar.setValue(curr_val + 1)
        if random.uniform(0, 10) <= 2:
            self.ui.push_bar.setValue(curr_val - 5)

    def process_password(self):
        password = self.ui.password_field.text()
        if password == "19940929":
            self.dev_mode = True

    # TODO: Fix serial issue in ESP32 Firmware Updater
    def update_network_esp32(self):
        if self.firmware_updater and self.firmware_updater.update_in_progress:
            return
        esp32_updater = ESP32FirmwareUpdater()
        esp32_updater.set_ui(self.ui)
        th.Thread(target=esp32_updater.update_firmware, daemon=True).start()
        self.firmware_updater = esp32_updater

    def update_stm32_modules(self):
        if self.firmware_updater and self.firmware_updater.update_in_progress:
            return
        stm32_updater = STM32FirmwareUpdater()
        stm32_updater.set_ui(self.ui)
        th.Thread(
            target=stm32_updater.update_module_firmware, daemon=True
        ).start()
        self.firmware_updater = stm32_updater

    def update_network_stm32(self):
        if self.firmware_updater and self.firmware_updater.update_in_progress:
            return
        stm32_updater = STM32FirmwareUpdater()
        stm32_updater.set_ui(self.ui)
        th.Thread(
            target=stm32_updater.update_module_firmware,
            args=True,
            daemon=True
        ).start()
        self.firmware_updater = stm32_updater
