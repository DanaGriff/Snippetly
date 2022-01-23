import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.ttk import Frame, Button, Label, Entry
from tkinter import Text, Listbox, Menu, Toplevel, Message
import DAL
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webbrowser
from Enums import FormState
import Constants

class SnippetsForm:
    def __init__(self, root, state, key, value, data, hotkeysMap):
        self.root = root
        self.root.iconbitmap(Constants.APP_ICON)
        self.root.title(Constants.APP_NAME)
        self.root.resizable(False, False)
        self.root.geometry(self.set_window_size())

        self.key = key
        self.value = value
        self.hotkeysMap = hotkeysMap
        self.data = data

        Constants.LEFT_PAD = 15
        Constants.TOP_PAD = 15
        
        # hotkey label
        self.hotkey_label = Label(self.root, text='Hotkey')
        self.hotkey_label.place(x=Constants.LEFT_PAD, y=Constants.TOP_PAD+3)

        # hotkey entry
        self.hotkey = tk.StringVar()
        self.key_entry = Entry(self.root, textvariable=self.hotkey)
        self.key_entry.place(x=Constants.LEFT_PAD+60, y=Constants.TOP_PAD)
        
        # text label
        self.text_label = Label(self.root, text='Text')
        self.text_label.place(x=Constants.LEFT_PAD, y=Constants.TOP_PAD+46)

        # hotkey text
        self.value_text = Text(self.root, height=7, width=30)
        self.value_text.place(x=Constants.LEFT_PAD+60, y=Constants.TOP_PAD+46)

        # save button

        # cancel button
        self.cancel_button = Button(self.root, text='Cancel', width=7, command = self.quit_window, bootstyle="danger")
        self.cancel_button.place(x=Constants.LEFT_PAD+120, y=Constants.TOP_PAD+180)

        self.save_button = Button(self.root, text='Save', width=7)
        self.save_button['command'] = self.save_button_clicked
        self.save_button.place(x=Constants.LEFT_PAD+190, y=Constants.TOP_PAD+180)

    def save_button_clicked(self):
        key = self.key_entry.get()
        if key != None and len(key) > 0:
            self.hotkeysMap[key] = self.value_text.get("1.0", "end").rstrip("\n")

            DAL.save_hotkeys_to_db(self.data, self.hotkeysMap)

        ##TODO Close window
        ##TODO refresh list box

    def quit_window(self):
        self.root.destroy()

    def set_window_size(self):
        window_width = 290
        window_height = 250

        # get the screen dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)+20
        center_y = int(screen_height / 2 - window_height / 2)+20

        # return the position of the window to the center of the screen
        return f'{window_width}x{window_height}+{center_x}+{center_y}'