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
# along with FreeRGB.  If not, see <https://www.gnu.org/licenses/>.

# Serial threading
serial = None
serial_thread = None

# Serial information
connected_devices = None
board_data_lines = None
board_data_buffer = None
board_data = []

current_colour = None
current_brightness = None
device_name = None
com_port = None
num_strips = None
ardu_version = None
board_name = None
baudrate = None

# Logging
has_logged = False
logger = None

# Store currently hovered button
current_hovered_btn = None

# Store popup menus
edit_effect_menu = None
colour_picker = None
popup_view = None

# Store currently selected context menu items
popup_menu_selection = None
selected_device = None
selected_strip = None

# Store elements controlled by advanced mode
advanced_mode_elements = []

# Import location for effect definitions
effect_import_path = 'src.ui.effects.effect'

# Refresh menus from any package
refreshMenus = None
