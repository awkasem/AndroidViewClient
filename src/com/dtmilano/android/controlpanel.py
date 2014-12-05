# -*- coding: utf-8 -*-
'''
    Copyright (C) 2012-2014  Diego Torres Milano
    Created on oct 30, 2014
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
    http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    
    @author: Diego Torres Milano
    @author: Ahmed Kasem
    '''

__version__ = '8.15.3'

import sys, os
import Tkinter
import tkFileDialog
from ttk import *

from com.dtmilano.android.viewclient import ViewClient, View
from com.dtmilano.android.culebron import Operation, Unit, Color


class Key:
    COMMA='KEYCODE_COMMA'
    PERIOD='KEYCODE_PERIOD'
    GO='KEYCODE_ENTER'

class ButtonWidth:
    KEYCODE_BUTTON_WIDTH=25
    KEYBOARD_BUTTON_WIDTH=1 

class ControlPanel(Tkinter.Toplevel):

    def __init__(self, culebron, vc, printOperation, **kwargs):
        self.culebron = culebron
        self.parent = culebron.window
        self.child_window = Tkinter.Toplevel(self.parent)
        self.notebook = Notebook(self.child_window)
        self.notebook.pack(fill=Tkinter.BOTH, padx=2, pady=3)
        self.keycode_tab = Frame(self.notebook)
        self.keyboard_tab = Frame(self.notebook)
        self.notebook.add(self.keycode_tab, text="KEYCODE")
        self.notebook.add(self.keyboard_tab, text="KEYBOARD")
        self.child_window.title("Control Panel")
        self.child_window.resizable(width=Tkinter.FALSE, height=Tkinter.FALSE)
        self.child_window.printOperation = printOperation
        self.child_window.vc = vc
        self.child_window.grid()
        self.child_window.column = 0
        self.child_window.row = 0
        self.keycode_list = [
                             'KEYCODE_1', 'KEYCODE_6', 'KEYCODE_BACK', 'KEYCODE_DPAD_UP', 'KEYCODE_PAGE_UP',
                             'KEYCODE_2', 'KEYCODE_7', 'KEYCODE_SPACE', 'KEYCODE_DPAD_DOWN', 'KEYCODE_PAGE_DOWN',
                             'KEYCODE_3', 'KEYCODE_8', 'KEYCODE_ENTER', 'KEYCODE_DPAD_LEFT', 'KEYCODE_VOLUME_UP',
                             'KEYCODE_4', 'KEYCODE_9', 'KEYCODE_DEL', 'KEYCODE_DPAD_RIGHT', 'KEYCODE_VOLUME_DOWN',
                             'KEYCODE_5', 'KEYCODE_0', 'KEYCODE_SEARCH', 'KEYCODE_DPAD_CENTER', 'KEYCODE_VOLUME_MUTE',
                             'KEYCODE_TV',  'KEYCODE_POWER', 'KEYCODE_EXPLORER', 'KEYCODE_MENU', 'KEYCODE_CALENDAR',
                             'KEYCODE_CHANNEL_UP', 'KEYCODE_GUIDE', 'KEYCODE_ZOOM_IN', 'KEYCODE_APP_SWITCH', 'KEYCODE_CALCULATOR',
                             'KEYCODE_CHANNEL_DOWN', 'KEYCODE_SETTINGS', 'KEYCODE_ZOOM_OUT', 'KEYCODE_HOME', 'KEYCODE_CAMERA',
                             'KEYCODE_MUSIC', 'KEYCODE_BOOKMARK', 'KEYCODE_CALL', 'KEYCODE_BRIGHTNESS_UP', 'KEYCODE_BRIGHTNESS_DOWN',
                             'KEYCODE_FORWARD', 'KEYCODE_BUTTON_MODE', 'SNAPSHOPT', 'REFRESH', 'QUIT'
                            ]

        self.keyboard_list = [
                              'KEYCODE_Q', 'KEYCODE_W', 'KEYCODE_E', 'KEYCODE_R', 'KEYCODE_T', 'KEYCODE_Y', 'KEYCODE_U', 'KEYCODE_I', 'KEYCODE_O', 'KEYCODE_P',
                              'KEYCODE_A', 'KEYCODE_S', 'KEYCODE_D', 'KEYCODE_F', 'KEYCODE_G', 'KEYCODE_H', 'KEYCODE_J', 'KEYCODE_K', 'KEYCODE_L',
                              'KEYCODE_Z', 'KEYCODE_X', 'KEYCODE_C', 'KEYCODE_V', 'KEYCODE_B', 'KEYCODE_N', 'KEYCODE_M', 'KEYCODE_DEL',
                              'KEYCODE_,', 'KEYCODE_.', 'KEYCODE_GO'
                             ]


        ### KEYCODE ###
        for keycode in self.keycode_list:
            self.keycode = ControlPanelButton(self.keycode_tab, culebron, vc, printOperation, value=keycode, text=keycode,
                                              width=ButtonWidth.KEYCODE_BUTTON_WIDTH, bg=Color.DARK_GRAY, fg=Color.LIGHT_GRAY,
                                              highlightbackground=Color.DARK_GRAY)

            if keycode == 'REFRESH':
                self.keycode.configure(fg=Color.BLUE, bg=Color.DARK_GRAY, command=self.keycode.refreshScreen)
                self.keycode.grid(column=self.child_window.column, row=self.child_window.row)
            elif keycode == 'SNAPSHOPT':
                self.keycode.configure(fg=Color.BLUE, bg=Color.DARK_GRAY, command=self.keycode.takeSnapshot)
                self.keycode.grid(column=self.child_window.column, row=self.child_window.row)
            elif keycode == 'QUIT':
                self.keycode.configure(fg=Color.BLUE, bg=Color.DARK_GRAY, command=self.child_window.destroy)
                self.keycode.grid(column=self.child_window.column, row=self.child_window.row)
            else:
                self.keycode.configure(command=self.keycode.pressKeyCode)
                self.keycode.grid(column=self.child_window.column, row=self.child_window.row)

            self.child_window.column += 1
            if self.child_window.column > 4:
                self.child_window.column = 0
                self.child_window.row += 1

        ### KEYBOARD ###
        for keyboard in self.keyboard_list:
            self.keyboard = ControlPanelButton(self.keyboard_tab, culebron, vc, printOperation, value=keyboard, text=keyboard[8:],
                                               width=ButtonWidth.KEYBOARD_BUTTON_WIDTH, bg=Color.DARK_GRAY, fg=Color.LIGHT_GRAY,
                                               highlightbackground=Color.DARK_GRAY)
                
            self.keyboard.configure(command=self.keyboard.pressKeyCode)
            self.keyboard.grid(column=self.child_window.column, row=self.child_window.row)

            self.child_window.column += 1
            if self.child_window.column > 9:
                self.child_window.column = 0
                self.child_window.row += 1


class ControlPanelButton(Tkinter.Button):

    def __init__(self, parent, culebron, vc, printOperation, value=None, **kwargs):
        Tkinter.Button.__init__(self, parent, kwargs)
        self.culebron = culebron
        self.printOperation = printOperation
        self.value = value
        self.vc = vc
        self.device = vc.device

    def pressKeyCode(self):
        keycode = self.value
        if keycode == 'KEYCODE_,':
            self.device.press(Key.COMMA)
            self.printOperation(None, Operation.PRESS, Key.COMMA)
        elif keycode == 'KEYCODE_.':
            self.device.press(Key.PERIOD)
            self.printOperation(None, Operation.PRESS, Key.PERIOD)
        elif keycode == 'KEYCODE_GO':
            self.device.press(Key.GO)
            self.printOperation(None, Operation.PRESS, Key.GO)
        else:
            self.device.press(keycode)
            self.printOperation(None, Operation.PRESS, keycode)

    def refreshScreen(self):
        self.culebron.showVignette()
        self.culebron.takeScreenshotAndShowItOnWindow()

    def takeSnapshot(self):
        #FIXME: Add printOperation <printSaveViewScreenshot(view, foldername)>
        path = tkFileDialog.asksaveasfilename(parent=self.master, defaultextension=".png", initialfile='Snapshot')
        if path:
            self.device.takeSnapshot(reconnect=True).save(path)
