import os
import sys
import time
import logging

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
        self.logger = None

    def stop(self):
        sys.stdout.write = self.sysstdout
        sys.stderr.write = self.sysstderr

    def start(self):
        sys.stdout.write = self.write
        sys.stderr.write = lambda msg: self.write(msg, color='red')

    def write(self, s, color="black"):
        sys.stdout.flush()
        self.printOccur.emit(s, color)
        if self.logger and not self.__is_redundant_line(s):
            self.logger.info(s)

    @staticmethod
    def __is_redundant_line(line):
        if line.startswith('\rUpdating'):
            return True

        if line.startswith('\rFirmware Upload: ['):
            return True

        if len(line) < 3:
            return True

        return False


class Form(QtWidgets.QDialog):
    """
    GUI Form of MODI Firmware Updater
    """

    def __init__(self, installer=False):
        self.logger = self.__init_logger()
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
        self.stdout.logger = self.logger

        # Init variable to check if the program is in installation mode
        self.ui.installation = installer

        # Connect up the buttons
        self.ui.update_network_esp32.clicked.connect(self.update_network_esp32)
        self.ui.update_stm32_modules.clicked.connect(self.update_stm32_modules)
        self.ui.update_network_stm32.clicked.connect(self.update_network_stm32)
        self.ui.translate_button.clicked.connect(self.translate_button_text)

        self.buttons = [
            self.ui.update_network_esp32,
            self.ui.update_stm32_modules,
            self.ui.update_network_stm32,
            self.ui.translate_button,
        ]

        # Disable the first button to be focused when UI is loaded
        self.ui.update_network_esp32.setAutoDefault(False)
        self.ui.update_network_esp32.setDefault(False)

        # Print init status
        time_now_str = time.strftime('[%Y/%m/%d@%X]', time.localtime())
        print(time_now_str + ' GUI MODI Firmware Updater has been started!')

        # Set up field variables
        self.firmware_updater = None
        self.button_in_english = False

    #
    # Main methods
    #
    def update_network_esp32(self):
        if self.firmware_updater and self.firmware_updater.update_in_progress:
            return
        self.ui.console.clear()
        print(
            'ESP32 Firmware Updater has been initialized for esp update!'
        )
        esp32_updater = ESP32FirmwareUpdater()
        esp32_updater.set_ui(self.ui)
        th.Thread(target=esp32_updater.update_firmware, daemon=True).start()
        self.firmware_updater = esp32_updater

    def update_stm32_modules(self):
        if self.firmware_updater and self.firmware_updater.update_in_progress:
            return
        self.ui.console.clear()
        print(
            'STM32 Firmware Updater has been initialized for module update!'
        )
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
        print(
            'STM32 Firmware Updater has been initialized for base update!'
        )
        stm32_updater = STM32FirmwareUpdater()
        stm32_updater.set_ui(self.ui)
        th.Thread(
            target=stm32_updater.update_module_firmware,
            args=(True,),
            daemon=True
        ).start()
        self.firmware_updater = stm32_updater

    def translate_button_text(self):
        button_en = [
            'Update Network ESP32',
            'Update STM32 Modules',
            'Update Network STM32',
            'Translate Button Text To Korean',
        ]
        button_kr = [
            '네트워크 모듈 업데이트',
            '모듈 초기화',
            '네트워크 모듈 초기화',
            '버튼 텍스트를 영어로 변경',
        ]
        appropriate_translation = \
            button_kr if self.button_in_english else button_en
        self.button_in_english = not self.button_in_english
        for i, button in enumerate(self.buttons):
            button.setText(appropriate_translation[i])

    #
    # Helper functions
    #
    @staticmethod
    def __init_logger():
        logger = logging.getLogger('GUI MODI Firmware Updater Logger')
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler = logging.FileHandler('gmfu.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        return logger

    def __append_text_line(self, line):
        self.ui.console.moveCursor(
            QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor
        )
        self.ui.console.moveCursor(
            QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.MoveAnchor
        )
        self.ui.console.moveCursor(
            QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor
        )

        # Remove new line character if current line represents update_progress
        if self.__is_update_progress_line(line):
            self.ui.console.textCursor().removeSelectedText()
            self.ui.console.textCursor().deletePreviousChar()

        # Display user text input
        self.ui.console.moveCursor(QtGui.QTextCursor.End)
        self.ui.console.insertPlainText(line)
        QtWidgets.QApplication.processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents
        )

    @staticmethod
    def __is_update_progress_line(line):
        if line.startswith('\rUpdating'):
            return True

        if line.startswith('\rFirmware Upload: ['):
            return True

        return False
