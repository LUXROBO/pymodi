import os
import random

import threading as th


from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from modi.util.firmware_updater import STM32FirmwareUpdater
from modi.util.firmware_updater import ESP32FirmwareUpdater


class Form(QtWidgets.QDialog):
    """
    GUI Form of MODI Firmware Updater
    """

    def handle_key_press_event(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        # TODO: Fix an issue with, (Qt.ControlModifier | Qt.ShiftModifier)
        if modifiers == Qt.ShiftModifier:
            if not self.is_dev_mode:
                self.ui.developer_frame.show()
                self.is_dev_mode = True
            else:
                self.ui.developer_frame.hide()
                self.is_dev_mode = False

    def __init__(self, parent=None, installer=False):
        QtWidgets.QDialog.__init__(self, parent)
        ui_path = (
            os.path.join(
                os.path.dirname(__file__),
                '..', 'assets', 'modi_firmware_updater.ui'
            )
        )
        if installer:
            ui_path = os.path.dirname(__file__).replace(
                'util', 'modi_firmware_updater.ui'
            )
        self.ui = uic.loadUi(ui_path)
        self.ui.setWindowTitle("MODI Firmware Updater")
        icon_path = os.path.join(
            os.path.dirname(__file__), '..', 'assets', 'image', 'network.png'
        )
        self.ui.setWindowIcon(QIcon(icon_path))
        self.setFixedSize(self.size())
        self.ui.show()

        # Init variable to check if the program is in installation mode
        self.ui.installation = installer

        # Connect up the buttons
        self.ui.update_network_esp32.clicked.connect(self.update_network_esp32)
        self.ui.update_stm32_modules.clicked.connect(self.update_stm32_modules)
        self.ui.update_network_stm32.clicked.connect(self.update_network_stm32)
        self.ui.update_network_esp32.setFocus(False)
        self.ui.update_stm32_modules.setFocus(False)
        self.ui.update_network_stm32.setFocus(False)

        self.ui.push_button.clicked.connect(self.push)
        self.ui.push_button.setAutoDefault(True)
        self.ui.push_button.setFocus(True)

        # Init module image
        module_image_path = os.path.join(
            os.path.dirname(__file__),
            '..', 'assets', 'image', 'network.png'
        )
        if installer:
            module_image_path = os.path.dirname(__file__).replace(
                'util', 'network.png'
            )
        module_pixmap = QPixmap(module_image_path)
        self.ui.curr_module_img.setPixmap(module_pixmap)

        # Init password field for enabling developer mode
        self.ui.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.password_field.returnPressed.connect(self.process_password)

        # Init radio button states
        self.ui.bootloader_rbutton.setEnabled(False)
        self.ui.esp32_rbutton.setEnabled(False)
        self.ui.modi_ota_factory_rbutton.setEnabled(False)
        self.ui.ota_data_initial_rbutton.setEnabled(False)
        self.ui.partitions_rbutton.setEnabled(False)

        # Hide ui available in the developer mode
        self.ui.developer_frame.hide()

        # Set up field variables
        self.firmware_updater = None
        self.is_dev_mode = False

    def push(self):
        curr_val = self.ui.push_bar.value()
        self.ui.push_bar.setValue(curr_val + 1)
        if self.ui.push_bar.value() >= 50 and random.uniform(0, 10) <= 3:
            self.ui.push_bar.setValue(curr_val - 5)
        self.handle_key_press_event()

    def process_password(self):
        password = self.ui.password_field.text()
        if password == "19940929":
            self.ui.bootloader_rbutton.setEnabled(True)
            self.ui.esp32_rbutton.setEnabled(True)
            self.ui.modi_ota_factory_rbutton.setEnabled(True)
            self.ui.ota_data_initial_rbutton.setEnabled(True)
            self.ui.partitions_rbutton.setEnabled(True)

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
