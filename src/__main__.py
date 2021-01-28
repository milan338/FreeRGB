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

import sys

if __name__ == '__main__':
    from pathlib import Path
    sys.path.append(str(Path().absolute()))

import __version__

from src import __globals__
from src import settings

from src.rw.jsonio import JsonIO
from src.rw.qssread import QssRead

from src.ui import getPath
from src.ui.button_actions import ButtonActions
from src.ui.generate_buttons import GenerateButtons
from src.ui.effects.effects import Effects
from src.ui.generators.create_menu_context import CreateMenuContext
from src.ui.generators.create_menu_effectedit import CreateMenuEffectEdit
from src.ui.generators.create_message_box import CreateMessageBox
from src.ui.views.input.input_dialogue import InputDialogue
from src.ui.views.main.Ui_main import Ui_Form
from src.ui.views.monitor.serial_monitor import SerialMonitor

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QColorDialog, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QThread


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        __globals__.parent = self
        self.setupFiles()
        settings.reloadSettings()
        Effects()
        self.version = __version__.__version__
        __globals__.refreshMenus = lambda: self.refreshMenus()
        __globals__.serial_thread = QThread()
        # UI initialisation
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # Setup UI elements
        self.createRightClickMenus()
        self.setupButtons()
        __globals__.colour_picker = QColorDialog(self)
        self.list_menu = CreateMenuContext(parent=self).makeMenu()
        # Initialise first communication
        self.DevicesJson = JsonIO('devices.json')
        self.comm_name = list(self.DevicesJson.readEntry(
            'selected_device')['devices'].keys())[0]
        self.comm_attr = list(self.DevicesJson.readEntry(
            'selected_device')['devices'].values())[0]
        __globals__.current_strip = int(
            list(self.DevicesJson.readEntry('selected_device')['strips'].keys())[0])
        if self.comm_name and self.comm_attr:
            ButtonActions.selectDevice(
                (self.comm_name, self.comm_attr))

    def setupFiles(self):
        self.init_files = ['menus.json', 'settings.json',
                           'effects.json', 'devices.json']
        # Copy all files from base dir if they don't already exist
        for file in self.init_files:
            if JsonIO(file).fileExists():
                pass
            else:
                JsonIO(file).copyFromBase()

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
            if settings.do_logs:
                __globals__.logger.error(
                    'Failed to reload menu(s), are preferences corrupted?')

    def setupButtons(self):
        # Add elements controlled by advanced mode to global list
        __globals__.advanced_mode_elements.append(self.ui.btn_device_debug)
        __globals__.advanced_mode_elements.append(
            self.ui.btn_device_information)
        # Refresh menus
        self.refreshMenus()
        # Bottom bar
        self.ui.btn_version.setText(f'Version {self.version}')
        self.ui.btn_device_debug.clicked.connect(
            lambda: self.initSerialMonitor())
        self.ui.btn_effect_off.clicked.connect(self.toggleLeds)
        self.ui.btn_device_information.clicked.connect(
            lambda: QMessageBox.information(self, 'Device Information',
                                            f'Device Name: {__globals__.board_data["name"]}\n'
                                            f'COM Port: {__globals__.board_data["port"]}\n'
                                            f'Physical Strips: {__globals__.board_data["physical_strips"]}\n'
                                            f'Virtual Strips: {__globals__.board_data["virtual_strips"]}\n'
                                            f'ArduRGB Version: {__globals__.board_data["version"]}\n'
                                            f'Board: {__globals__.board_data["type"]}\n'))
        self.ui.slider_brightness.sliderReleased.connect(self.getBright)
        # Left bar
        self.ui.btn_menu_effects.clicked.connect(
            lambda: self.changePage(self.ui.main_menus, 0))
        self.ui.btn_menu_settings.clicked.connect(
            lambda: self.changePage(self.ui.main_menus, 1))
        self.ui.btn_list_device.clicked.connect(
            lambda: self.initListMenu('devices'))
        self.ui.btn_list_device.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.btn_list_device.customContextMenuRequested.connect(
            lambda: self.contextMenu(self.right_click_menu_devices))
        __globals__.strips_menu = self.ui.btn_list_strip
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

    def createRightClickMenus(self):
        self.right_click_json = JsonIO('right_click_menu.json')
        self.right_click_create = CreateMenuEffectEdit(parent=self)
        # Effects right click menu
        self.right_click_menu_effects = self.genRightClickMenu(
            'main_menu_right_click_menu')
        # Devices right click menu
        self.right_click_menu_devices = self.genRightClickMenu(
            'devices_right_click_menu')

    def genRightClickMenu(self, menu):
        # Get menu options
        options = self.right_click_json.readEntry(menu)
        # Create new right click menu
        r_c_menu = self.right_click_create.makeMenu()
        # Add all JSON entries as options to right click menu
        for entry_name, entry_payload in options.items():
            self.right_click_create.addOption(
                r_c_menu, entry_name, entry_payload)
        return r_c_menu

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
        self.DevicesJson = JsonIO('devices.json')
        self.ContextMenuGen = CreateMenuContext(parent=self)
        # Clear menu actions
        self.list_menu.clear()
        # Get actions from file
        self.connected_devices = self.DevicesJson.readEntry('known_devices')
        self.device_list = self.connected_devices[menu]
        for device_name, device_attributes in self.device_list.items():
            self.selected_devices = list(self.DevicesJson.readEntry(
                'selected_device')['devices'].keys())
            try:
                # Set highlighted entry
                if device_name == list(self.DevicesJson.readEntry('selected_device')['devices'].keys())[0]:
                    self.ContextMenuGen.addOption(
                        self.list_menu, device_name, (None, ('selectDevice', (device_name, device_attributes))), highlighted=True)
                # Set non-highlighted entry
                else:
                    self.ContextMenuGen.addOption(
                        self.list_menu, device_name, (None, ('selectDevice', (device_name, device_attributes))))
            # Set non-highlighted entry
            except:
                self.ContextMenuGen.addOption(
                    self.list_menu, device_name, (None, ('selectDevice', (device_name, device_attributes))))
        # Place context menu at cursor position
        self.list_menu.exec(QCursor.pos())

    def contextMenu(self, menu):
        menu.exec(QCursor.pos())

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
