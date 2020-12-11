import os
import sys

import threading as th


from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QObject, pyqtSignal

from modi.util.firmware_updater import STM32FirmwareUpdater
from modi.util.firmware_updater import ESP32FirmwareUpdater


class StdoutRedirect(QObject):
    printOccur = pyqtSignal(str, str, name='print')

    def __init__(self):
        QObject.__init__(self, None)
        self.daemon = True
        self.sysstdout = sys.stdout.write
        self.sysstderr = sys.stderr.write

    def stop(self):
        sys.stdout.write = self.sysstdout
        sys.stderr.write = self.sysstderr

    def start(self):
        sys.stdout.write = self.write
        sys.stderr.write = lambda msg: self.write(msg, color='red')

    def write(self, s, color="black"):
        sys.stdout.flush()
        self.printOccur.emit(s, color)


class Form(QtWidgets.QDialog):
    """
    GUI Form of MODI Firmware Updater
    """

    def __init__(self, installer=False):
        QtWidgets.QDialog.__init__(self)
        if installer:
            ui_path = os.path.dirname(__file__).replace(
                'util', 'modi_firmware_updater.ui'
            )
        else:
            ui_path = (
                os.path.join(
                    os.path.dirname(__file__),
                    '..', 'assets', 'modi_firmware_updater.ui'
                )
            )
        self.ui = uic.loadUi(ui_path)
        self.ui.setWindowTitle('MODI Firmware Updater')
        self.setFixedSize(self.size())
        self.ui.show()

        # Redirect stdout to text browser (i.e. console in our UI)
        self.stdout = StdoutRedirect()
        self.stdout.start()
        self.stdout.printOccur.connect(
            lambda line: self.__append_text_line(line)
        )

        # Init variable to check if the program is in installation mode
        self.ui.installation = installer

        # Connect up the buttons
        self.ui.update_network_esp32.clicked.connect(self.update_network_esp32)
        self.ui.update_stm32_modules.clicked.connect(self.update_stm32_modules)
        self.ui.update_network_stm32.clicked.connect(self.update_network_stm32)

        # Disable the first button to be focused when UI is loaded
        self.ui.update_network_esp32.setAutoDefault(False)
        self.ui.update_network_esp32.setDefault(False)

        # Set up field variables
        self.firmware_updater = None

    #
    # Main methods
    #
    def update_network_esp32(self):
        if self.firmware_updater and self.firmware_updater.update_in_progress:
            return
        self.ui.console.clear()
        print('ESP32 Firmware Updater has been initialized for esp update!')
        esp32_updater = ESP32FirmwareUpdater()
        esp32_updater.set_ui(self.ui)
        th.Thread(target=esp32_updater.update_firmware, daemon=True).start()
        self.firmware_updater = esp32_updater

    def update_stm32_modules(self):
        if self.firmware_updater and self.firmware_updater.update_in_progress:
            return
        self.ui.console.clear()
        print('STM32 Firmware Updater has been initialized for module update!')
        stm32_updater = STM32FirmwareUpdater()
        stm32_updater.set_ui(self.ui)
        th.Thread(
            target=stm32_updater.update_module_firmware, daemon=True
        ).start()
        self.firmware_updater = stm32_updater

    def update_network_stm32(self):
        if self.firmware_updater and self.firmware_updater.update_in_progress:
            return
        self.ui.console.clear()
        print('STM32 Firmware Updater has been initialized for base update!')
        stm32_updater = STM32FirmwareUpdater()
        stm32_updater.set_ui(self.ui)
        th.Thread(
            target=stm32_updater.update_module_firmware,
            args=(True,),
            daemon=True
        ).start()
        self.firmware_updater = stm32_updater

    #
    # Helper functions
    #
    def __append_text_line(self, line):
        self.ui.console.moveCursor(QtGui.QTextCursor.End)
        self.ui.console.insertPlainText(line)
        QtWidgets.QApplication.processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents
        )
