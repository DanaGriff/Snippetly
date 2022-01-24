import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.ttk import Frame, Button, Label, Entry
from tkinter import Text, Listbox, Menu, Toplevel, Message
from tkinter.messagebox import askyesno
import DAL
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webbrowser
from SnippetsForm import SnippetsForm
from Enums import FormState
import Constants
from FormContainer import FormContainer

class FormFrame(ttk.Frame):
    def __init__(self, container, state, key, value, data, hotkeysMap):
        super().__init__(container)

        self.key = key
        self.value = value
        self.hotkeysMap = hotkeysMap
        self.data = data
        self.container = container

        if state == FormState.ADD:
            self.action_button_label = "Add"
            self.old_key = None
        else:
            self.action_button_label = "Save"
            self.old_key = key

        Constants.LEFT_PAD = 15
        Constants.TOP_PAD = 15
        
        # hotkey label
        self.hotkey_label = Label(self.container, text='Hotkey')
        self.hotkey_label.place(x=Constants.LEFT_PAD, y=Constants.TOP_PAD+3)

        # hotkey entry
        self.hotkey = tk.StringVar()
        self.key_entry = Entry(self.container, textvariable=self.hotkey)
        self.key_entry.insert(END, self.key)
        self.key_entry.place(x=Constants.LEFT_PAD+60, y=Constants.TOP_PAD)
        self.key_entry.focus()

        # text label
        self.text_label = Label(self.container, text='Text')
        self.text_label.place(x=Constants.LEFT_PAD, y=Constants.TOP_PAD+46)

        # hotkey text
        self.value_text = Text(self.container, height=7, width=30)
        self.value_text.insert(END, self.value)
        self.value_text.place(x=Constants.LEFT_PAD+60, y=Constants.TOP_PAD+46)
        

        # cancel button
        self.cancel_button = Button(self.container, text='Cancel', width=7, command = self.container.quit_window, bootstyle="danger")
        self.cancel_button.place(x=Constants.LEFT_PAD+120, y=Constants.TOP_PAD+180)

        # save button
        self.action_button = Button(self.container, text=self.action_button_label, width=7)
        self.action_button['command'] = self.action_button_clicked
        self.action_button.place(x=Constants.LEFT_PAD+190, y=Constants.TOP_PAD+180)

    def action_button_clicked(self):
        key = self.key_entry.get()
        if key != None and len(key) > 0:
            if self.old_key != None:
                self.hotkeysMap.pop(self.old_key)
                
            self.hotkeysMap[key] = self.value_text.get("1.0", "end").rstrip("\n")

            DAL.save_hotkeys_to_db(self.data, self.hotkeysMap)

            self.container.master.refresh_listbox()

            self.container.quit_window()