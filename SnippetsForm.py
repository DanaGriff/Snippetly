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
    def __init__(self, root, AppFrame, state, key, value, data, hotkeysMap):
        self.key = key
        self.value = value
        self.hotkeysMap = hotkeysMap
        self.data = data
        self.AppFrame = AppFrame

        if state == FormState.ADD:
            self.action_button_label = "Add"
            self.action_title = "Add Snippet"
            self.old_key = None
        else:
            self.action_button_label = "Save"
            self.action_title = "Edit Snippet"
            self.old_key = key

        self.root = root
        self.root.iconbitmap(Constants.APP_ICON)
        self.root.title(self.action_title)
        self.root.resizable(False, False)
        self.root.geometry(self.set_window_size())
        self.root.transient(self.AppFrame) # set to be on top of the main window
        self.root.grab_set() # hijack all commands from the master (clicks on the main window are ignored)

        Constants.LEFT_PAD = 15
        Constants.TOP_PAD = 15
        
        # hotkey label
        self.hotkey_label = Label(self.root, text='Hotkey')
        self.hotkey_label.place(x=Constants.LEFT_PAD, y=Constants.TOP_PAD+3)

        # hotkey entry
        self.hotkey = tk.StringVar()
        self.key_entry = Entry(self.root, textvariable=self.hotkey)
        self.key_entry.insert(END, self.key)
        self.key_entry.place(x=Constants.LEFT_PAD+60, y=Constants.TOP_PAD)
        self.key_entry.focus()

        # text label
        self.text_label = Label(self.root, text='Text')
        self.text_label.place(x=Constants.LEFT_PAD, y=Constants.TOP_PAD+46)

        # hotkey text
        self.value_text = Text(self.root, height=7, width=30)
        self.value_text.insert(END, self.value)
        self.value_text.place(x=Constants.LEFT_PAD+60, y=Constants.TOP_PAD+46)
        

        # cancel button
        self.cancel_button = Button(self.root, text='Cancel', width=7, command = self.quit_window, bootstyle="danger")
        self.cancel_button.place(x=Constants.LEFT_PAD+120, y=Constants.TOP_PAD+180)

        # save button
        self.action_button = Button(self.root, text=self.action_button_label, width=7)
        self.action_button['command'] = self.action_button_clicked
        self.action_button.place(x=Constants.LEFT_PAD+190, y=Constants.TOP_PAD+180)

    def action_button_clicked(self):
        key = self.key_entry.get()
        if key != None and len(key) > 0:
            if self.old_key != None:
                self.hotkeysMap.pop(self.old_key)
                
            self.hotkeysMap[key] = self.value_text.get("1.0", "end").rstrip("\n")

            DAL.save_hotkeys_to_db(self.data, self.hotkeysMap)

            self.AppFrame.refresh_listbox()

            self.quit_window()
        

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