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
        return (
            line.startswith('\rUpdating') or
            line.startswith('\rFirmware Upload: [') or
            len(line) < 3
        )


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
            self.component_path = (
                os.path.join(os.path.dirname(__file__), 'util', 'component')
            )
        else:
            ui_path = (
                os.path.join(
                    os.path.dirname(__file__),
                    '..', 'assets', 'modi_firmware_updater.ui'
                )
            )
            self.component_path = (
                os.path.join(
                    os.path.dirname(__file__),
                    '..', 'assets', 'image', 'component'
                )
            )
        self.ui = uic.loadUi(ui_path)

        self.ui.setStyleSheet('background-color: white')
        self.ui.console.hide()
        self.ui.setFixedHeight(600)

        # Set LUXROBO logo image
        logo_path = os.path.join(self.component_path, 'luxrobo_logo.png')
        qPixmapVar = QtGui.QPixmap()
        qPixmapVar.load(logo_path)
        self.ui.lux_logo.setPixmap(qPixmapVar)

        # Buttons image
        self.active_path = os.path.join(self.component_path, 'btn_frame_active.png')
        self.inactive_path = os.path.join(self.component_path, 'btn_frame_inactive.png')
        self.pressed_path = os.path.join(self.component_path, 'btn_frame_pressed.png')
        self.language_frame_path = os.path.join(self.component_path, 'lang_frame.png')
        self.language_frame_pressed_path = os.path.join(
            self.component_path, 'lang_frame_pressed.png'
        )

        self.ui.update_network_esp32.setStyleSheet(
            f'border-image: url({self.active_path})'
        )
        self.ui.update_stm32_modules.setStyleSheet(
            f'border-image: url({self.active_path})'
        )
        self.ui.update_network_stm32.setStyleSheet(
            f'border-image: url({self.active_path})'
        )
        self.ui.translate_button.setStyleSheet(
            f'border-image: url({self.language_frame_path})'
        )
        self.ui.devmode_button.setStyleSheet(
            f'border-image: url({self.language_frame_path})'
        )

        self.ui.setWindowTitle('MODI Firmware Updater')

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
        self.ui.devmode_button.clicked.connect(self.dev_mode_button)

        self.buttons = [
            self.ui.update_network_esp32,
            self.ui.update_stm32_modules,
            self.ui.update_network_stm32,
            self.ui.devmode_button,
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
        self.console = False

        # Set up ui field variables
        self.ui.is_english = False
        self.ui.active_path = self.active_path
        self.ui.pressed_path = self.pressed_path
        self.ui.language_frame_path = self.language_frame_path
        self.ui.language_frame_pressed_path = self.language_frame_pressed_path

        self.translate_button_text()
        self.translate_button_text()
        self.dev_mode_button()
        self.dev_mode_button()
        self.ui.show()

    #
    # Main methods
    #
    def update_network_esp32(self):
        button_start = time.time()
        if self.firmware_updater and self.firmware_updater.update_in_progress:
            return
        self.ui.update_network_esp32.setStyleSheet(
            f'border-image: url({self.pressed_path})'
        )
        self.ui.console.clear()
        print(
            'ESP32 Firmware Updater has been initialized for esp update!'
        )
        th.Thread(
            target=self.__click_motion, args=(0,button_start), daemon=True
        ).start()
        esp32_updater = ESP32FirmwareUpdater()
        esp32_updater.set_ui(self.ui)
        th.Thread(target=esp32_updater.update_firmware, daemon=True).start()
        self.firmware_updater = esp32_updater

    def update_stm32_modules(self):
        button_start = time.time()
        if self.firmware_updater and self.firmware_updater.update_in_progress:
            return
        self.ui.update_stm32_modules.setStyleSheet(
            f'border-image: url({self.pressed_path})'
        )
        self.ui.console.clear()
        print(
            'STM32 Firmware Updater has been initialized for module update!'
        )
        th.Thread(
            target=self.__click_motion, args=(1,button_start), daemon=True
        ).start()
        stm32_updater = STM32FirmwareUpdater()
        stm32_updater.set_ui(self.ui)
        th.Thread(
            target=stm32_updater.update_module_firmware, daemon=True
        ).start()
        self.firmware_updater = stm32_updater

    def update_network_stm32(self):
        button_start = time.time()
        if self.firmware_updater and self.firmware_updater.update_in_progress:
            return
        self.ui.update_network_stm32.setStyleSheet(
            f'border-image: url({self.pressed_path})'
        )
        self.ui.console.clear()
        print(
            'STM32 Firmware Updater has been initialized for base update!'
        )
        th.Thread(
            target=self.__click_motion, args=(2,button_start), daemon=True
        ).start()
        stm32_updater = STM32FirmwareUpdater()
        stm32_updater.set_ui(self.ui)
        th.Thread(
            target=stm32_updater.update_module_firmware,
            args=(True,),
            daemon=True
        ).start()
        self.firmware_updater = stm32_updater

    def dev_mode_button(self):
        button_start = time.time()
        self.ui.devmode_button.setStyleSheet(
            f'border-image: url({self.language_frame_pressed_path})'
        )
        th.Thread(
            target=self.__click_motion, args=(3,button_start), daemon=True
        ).start()
        if self.console:
            self.ui.console.hide()
            self.ui.setFixedHeight(600)
        else:
            self.ui.console.show()
            self.ui.setFixedHeight(780)
        self.console = not self.console

    def translate_button_text(self):
        button_start = time.time()
        self.ui.translate_button.setStyleSheet(
            f'border-image: url({self.language_frame_pressed_path})'
        )
        th.Thread(
            target=self.__click_motion, args=(4,button_start), daemon=True
        ).start()
        button_en = [
            'Update Network ESP32',
            'Update STM32 Modules',
            'Update Network STM32',
            'Dev Mode',
            '한글',
        ]
        button_kr = [
            '네트워크 모듈 업데이트',
            '모듈 초기화',
            '네트워크 모듈 초기화',
            '개발자 모드',
            'English',
        ]
        appropriate_translation = \
            button_kr if self.button_in_english else button_en
        self.button_in_english = not self.button_in_english
        self.ui.is_english = not self.ui.is_english
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

    def __click_motion(self, button_type, start_time):
        # Busy wait for 0.2 seconds
        while time.time() - start_time < 0.2:
            pass

        if button_type in [3, 4]:
            self.buttons[button_type].setStyleSheet(
                f'border-image: url({self.language_frame_path})'
            )
        else:
            self.buttons[button_type].setStyleSheet(
                f'border-image: url({self.active_path})'
            )
            for i, q_button in enumerate(self.buttons):
                if i in [button_type, 3, 4]:
                    continue
                q_button.setStyleSheet(f'border-image: url({self.inactive_path})')
                q_button.setEnabled(False)

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
        return (
            line.startswith('\rUpdating') or
            line.startswith('\rFirmware Upload: [')
        )
