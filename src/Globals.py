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

# Store currently hovered button
current_hovered_btn = None

# Store edit effect menu
edit_effect_menu = None

# Store colour picker menu
colour_picker = None

# Store currently selected context menu items
popup_menu_selection = None
selected_device = None
selected_strip = None
# Remove device and strip
# - just dynamically replace stylesheet
# of its UI element

# Import location for effect definitions
effect_import_path = 'ui.effects.effect'

# Refresh menus from any package
refreshMenus = None
