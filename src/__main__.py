# This file is part of FreeRGB, an app to control lighting devices.
# Copyright (C) 2020 milan338.
#
# FreeRGB is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FreeRGB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the7
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FreeRGB.  If not, see <https://www.gnu.org/licenses/>.

# TODO add input type selector for input, add logic to either encode() or bytearray for serial direct

import sys

if __name__ == '__main__':
    from pathlib import Path
    sys.path.append(str(Path().absolute()))

import __version__

from src import Globals
from src import Settings

from src.serial.SerialIO import SerialIO

from src.rw.JsonIO import JsonIO
from src.rw.QssRead import QssRead

from src.ui import getPath
from src.ui.GenerateButtons import GenerateButtons
from src.ui.effects.Effects import Effects
from src.ui.generators.CreateMenuContext import CreateMenuContext
from src.ui.generators.CreateMenuEffectEdit import CreateMenuEffectEdit
from src.ui.generators.CreateMessageBox import CreateMessageBox
from src.ui.views.input.InputDialogue import InputDialogue
from src.ui.views.main.Ui_MainWindow import Ui_Form
from src.ui.views.monitor.SerialMonitor import SerialMonitor

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QColorDialog, QMessageBox, QApplication
from PyQt5.QtCore import QThread


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupFiles()
        Settings.reloadSettings()
        Effects()
        self.version = __version__.__version__
        Globals.refreshMenus = lambda: self.refreshMenus()
        Globals.serial_thread = QThread()
        # UI initialisation
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # Update available devices
        self.connected_dict = {'devices': 'device_1',
                               'strips': 'strip_1'}  # TODO tmp
        self.current_colour = None  # TODO tmp
        self.current_brightness = 0  # TODO tmp
        self.device_name = None
        self.com_port = None
        self.num_strips = None
        self.ardu_version = None
        self.board = None
        self.baud_rate = None
        # Initialise serial TODO reinitialise each time different port selected
        SerialIO('COM13', 9600)
        # Setup UI elements
        self.setRightClickMenu()
        self.setupButtons()
        Globals.colour_picker = QColorDialog(self)
        self.list_menu = CreateMenuContext(parent=self).makeMenu()

    def setupFiles(self):
        self.init_files = ['menus.json', 'settings.json', 'effects.json']
        # Copy all files from base dir if they don't already exist
        for file in self.init_files:
            if JsonIO(file).fileExists():
                pass
            else:
                JsonIO(file).copyFromBase()
        # Create fresh copy of connected devices list TODO tmp
        # JsonIO('connected_devices.json').copyFromBase() # TODO deal with empty device list?

    def refreshMenus(self):
        try:
            # Reset main menu
            GenerateButtons('menus.json', 'main_menu').removeButtons(
                self.ui.main_menu_button_layout)
            GenerateButtons('menus.json', 'main_menu').generateGenericButtons(self.ui.main_menu_button_layout,
                                                                              self.ui.effects_scroll_region, 'primary', self.right_click_menu_effects, spacer=True, effect_btn=True)
            # Reset settings menu
            GenerateButtons('settings.json', 'settings').removeButtons(
                self.ui.settings_button_layout)
            GenerateButtons('settings.json', 'settings').generateGenericButtons(
                self.ui.settings_button_layout, self.ui.settings_scroll_region, 'primary', spacer=True)
        except:
            if Settings.do_logs:
                Globals.logger.error(
                    'Failed to reload menu(s), are preferences corrupted?')

    def setupButtons(self):
        # Add elements controlled by advanced mode to global list
        Globals.advanced_mode_elements.append(self.ui.btn_device_debug)
        Globals.advanced_mode_elements.append(self.ui.btn_device_information)
        # Refresh menus
        self.refreshMenus()
        # Bottom bar
        self.ui.btn_version.setText(f'Version {self.version}')
        self.ui.btn_device_debug.clicked.connect(
            lambda: self.initSerialMonitor())
        self.ui.btn_effect_off.clicked.connect(self.toggleLeds)
        self.ui.btn_device_information.clicked.connect(
            lambda: QMessageBox.information(self, 'Device Information',
                                            f'Device Name: {self.device_name}\n'
                                            f'COM Port: {self.com_port}\n'
                                            f'Port Description: {None}\n'
                                            f'Strips Connected: {self.num_strips}\n'
                                            f'ArduRGB Version: {self.ardu_version}\n'
                                            f'Board: {self.board}\n'
                                            f'Baud Rate: {self.baud_rate}'))
        self.ui.slider_brightness.sliderReleased.connect(self.getBright)
        self.ui.slider_brightness.setValue(self.current_brightness)
        # Left bar
        self.ui.btn_menu_effects.clicked.connect(
            lambda: self.changePage(self.ui.main_menus, 0))
        self.ui.btn_menu_settings.clicked.connect(
            lambda: self.changePage(self.ui.main_menus, 1))
        self.ui.btn_list_device.clicked.connect(
            lambda: self.initListMenu('devices'))
        self.ui.btn_list_strip.clicked.connect(
            lambda: self.initListMenu('strips'))
        # Effects menu
        self.ui.btn_menu_effect_new.clicked.connect(
            lambda: self.initDialogue('main_menu', 'Create New Effect'))
        self.ui.btn_menu_effect_reset.clicked.connect(lambda: CreateMessageBox(
            'Reset Effects Menu', 'This action will erase all custom effects you have specified. Continue?').resetPreferences(
            file='menus.json', menu='main_menu', layout='main_menu_button_layout'))
        # Settings menu
        self.ui.btn_settings_reset.clicked.connect(lambda: CreateMessageBox(
            'Reset Settings', 'This action will revert all settings to their defaults. Continue?').resetPreferences(file='settings.json', reset_file=True, reload_settings=True))

    def changePage(self, widget, index):
        widget.setCurrentIndex(index)

    def setRightClickMenu(self):
        # Read entries from JSON
        self.right_click_menu_effects_options = JsonIO(
            'right_click_menu.json').readEntry('main_menu_right_click_menu')
        # Create new right click menu
        self.right_click_menu_effects = CreateMenuEffectEdit(
            parent=self).makeMenu()
        # Add all JSON entries as options to right click menu
        for entry_name, entry_payload in self.right_click_menu_effects_options.items():
            CreateMenuEffectEdit(parent=self).addOption(
                self.right_click_menu_effects, entry_name, entry_payload)

    def getBright(self):
        self.current_brightness = self.ui.slider_brightness.value()
        print(self.current_brightness)

    def toggleLeds(self, message):
        print('serial sent')

    def setWindowParams(self, window, title, icon=None):
        window.setWindowTitle(title)
        window.show()
        # window.setWindowIcon(icon)

    def initSerialMonitor(self):
        self.serial_monitor = SerialMonitor()
        self.setWindowParams(self.serial_monitor, 'Serial Port Debug View')

    def initDialogue(self, menu, window_title):
        self.input_dialogue = InputDialogue(menu)
        self.setWindowParams(self.input_dialogue, window_title)

    def initListMenu(self, menu):
        # Clear menu actions
        self.list_menu.clear()
        # Get actions from file
        self.connected_devices = JsonIO(
            'connected_devices.json').readEntry('main_devices')
        self.device_list = self.connected_devices[menu]
        for device_name, device_attributes in self.device_list.items():
            # Set highlighted entry
            if device_name == self.connected_dict[menu]:
                CreateMenuContext(parent=self).addOption(
                    self.list_menu, device_name, (None, device_attributes['text']), highlighted=True)
            # Set non-highlighted entry
            else:
                CreateMenuContext(parent=self).addOption(
                    self.list_menu, device_name, (None, device_attributes['text']))
        # Place context menu at cursor position
        self.list_menu.exec(QCursor.pos())

    def mousePressEvent(self, event):
        pass


def init():
    # Initialise application
    app = QApplication(sys.argv)
    # Setup main window
    window = MainWindow()
    window.setWindowTitle('title')
    # window.setWindowIcon()
    # Set main window styles
    QssRead('main')
    with open(getPath('main_ld.qss'), 'r') as style_file:
        window.setStyleSheet(style_file.read())
    # Display main window
    window.show()
    # Run application and provide exit code
    sys.exit(app.exec())


if __name__ == '__main__':
    init()
