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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FreeRGB. If not, see <https://www.gnu.org/licenses/>.

import Globals

from ui.widgets.HoverButton import HoverButton
from ui.widgets.ToggleSwitch import ToggleSwitch

from PyQt5.QtCore import Qt, QCoreApplication, QSize, QRect
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QLayout, QHBoxLayout, QLabel


class CreateLargeButton():
    def __init__(self, vertical_element, spacer=False, effect_btn=False):
        self.vertical_element = vertical_element
        self.effect_btn = effect_btn
        # Add spacer between buttons
        if spacer:
            self.vertical_element.addItem(QSpacerItem(
                20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))
        self.translate = QCoreApplication.translate

    def createGenericButton(self, text, obj_name, scroll_element, style_sheet, right_click_menu, action):
        # Initialise button
        self.btn = HoverButton(scroll_element)
        self.vertical_element.addWidget(self.btn)
        self.btn.setObjectName(obj_name)
        self.btn.setText(self.translate("Form", text))
        # Set size
        self.sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.btn.setSizePolicy(self.sizePolicy)
        self.btn.setMinimumSize(QSize(0, 100))
        self.btn.setMaximumSize(QSize(700, 100))
        # Create context menu
        self.btn.setContextMenuPolicy(Qt.CustomContextMenu)
        self.btn.customContextMenuRequested.connect(
            lambda: self.contextMenu(right_click_menu))
        # Set style
        with open(style_sheet) as style_file:
            self.btn.setStyleSheet(style_file.read())
        # Set up hover detection
        self.btn.mouse_hovered.connect(self.setCurrentHoverButton)
        if self.effect_btn:
            # Connect click action
            self.btn.clicked.connect(lambda: self.runEffect(action))
        # Show button
        self.btn.show()

    def createToggleButton(self, text, obj_name, scroll_element, style_sheet, action):
        # Initialise button
        self.btn = QWidget(scroll_element)
        self.vertical_element.addWidget(self.btn)
        self.btn.setObjectName(obj_name)
        # Set size
        self.sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.btn.setSizePolicy(self.sizePolicy)
        self.btn.setMinimumSize(QSize(0, 100))
        self.btn.setMaximumSize(QSize(700, 100))
        # Set style
        with open(style_sheet) as style_file:
            self.btn.setStyleSheet(style_file.read())
        # Create horizontal layout for elements
        self.horizontal_layout_widget = QWidget(self.btn)
        self.horizontal_layout_widget.setGeometry(QRect(10, 3, 631, 102))
        self.horizontal_layout_widget.setObjectName(
            f'{obj_name}_h_layout_widget')
        self.btn_layout = QHBoxLayout(self.horizontal_layout_widget)
        self.btn_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        # Maybe try replacing spacers with margins?
        self.btn_layout.setContentsMargins(100, 37, 0, 0)
        self.btn_layout.setObjectName(f'{obj_name}_layout')
        # Create spacers for boundaries
        # self.spacer_left = QSpacerItem(
        #     100, 100, QSizePolicy.Fixed, QSizePolicy.Minimum)
        # self.spacer_right = QSpacerItem(
        #     100, 100, QSizePolicy.Fixed, QSizePolicy.Minimum)  # Maybe use only one spacer and place twice
        # self.btn_layout.addItem(self.spacer_right)
        # Create toggle switch element
        self.switch = ToggleSwitch()
        self.btn_layout.addWidget(self.switch)
        # Add button label
        self.btn_label = QLabel(self.horizontal_layout_widget)
        self.btn_label.setMaximumSize(QSize(200, 100))
        self.btn_label.setObjectName(f'{obj_name}_label')
        # self.btn_layout.addWidget(self.btn_label)
        # self.btn_layout.addItem(self.spacer_left)
        # Show button
        self.btn.show()

    def runEffect(self, effect):
        try:
            # Import effect file
            self.module = __import__(
                f'{Globals.effect_import_path}.{effect}', fromlist=[None])
            # Create new effect instance
            self.effect_class = getattr(self.module, effect)
            self.effect_class()
        except:
            pass

    def setCurrentHoverButton(self, hovered):
        if hovered:
            Globals.current_hovered_btn = self.btn
        else:
            pass

    def contextMenu(self, menu):
        menu.exec(QCursor.pos())
