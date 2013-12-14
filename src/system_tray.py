#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import qApp, QSystemTrayIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from deepin_menu.menu import Menu, MenuSeparator, CheckboxMenuItem
from config import setting_config
from xutils import delete_selection
from nls import _

class SystemTrayIcon(QSystemTrayIcon):
    
    showSettingView = pyqtSignal()
    
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.activated.connect(self.on_activated) 
        
    @pyqtSlot(str, bool)
    def click_menu(self, menu_id, state):
        if menu_id == "quit":
            qApp.quit()
        elif menu_id == "wizard":
            pass
        elif menu_id == "about":
            pass
        elif menu_id == "settings":
            self.showSettingView.emit()
        else:
            if menu_id == "pause":
                if not state:
                    delete_selection()
                
                self.set_menu_active(state)    
                
            setting_config.update_trayicon_config(menu_id, state)
            
    def set_menu_active(self, state):
        self.menu.setItemActivity("toggle_speech", not state)
        self.menu.setItemActivity("key_trigger_select", not state)
        
    def on_activated(self, reason):
        if reason in [QSystemTrayIcon.Context, QSystemTrayIcon.Trigger]:
            geometry = self.geometry()
            mouse_x = int(geometry.x() / 2 + geometry.width() / 2)
            mouse_y = int(geometry.y() / 2)
            
            self.menu = Menu([
                    CheckboxMenuItem("pause", _("Pause translate"), 
                                     setting_config.get_trayicon_config("pause")),
                    CheckboxMenuItem("toggle_speech", _("Voice after translate"), 
                                     setting_config.get_trayicon_config("toggle_speech")),
                    CheckboxMenuItem("key_trigger_select", _("Press ctrl to translate selection"), 
                                     setting_config.get_trayicon_config("key_trigger_select")),
                    MenuSeparator(),
                    ("settings", _("Settings")),
                    ("wizard", _("Wizard")),
                    ("about", _("About")),
                    MenuSeparator(),
                    ("quit", _("Exit")),
                    ])
            self.menu.itemClicked.connect(self.click_menu)
            self.menu.showDockMenu(mouse_x, mouse_y)
            self.set_menu_active(setting_config.get_trayicon_config("pause"))
            
    def get_trayarea(self):
        geometry = self.geometry()
        return (geometry.y() / 2, geometry.y() / 2 + geometry.height())
