import tkinter as tk
from tkinter.ttk import Button, Label, Entry
from tkinter import Text
from tkinter.messagebox import askyesno
import DAL
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from Enums import FormState
import consts

class FormFrame(ttk.Frame):
    def __init__(self, container, state, key, value, data, snippetsMap):
        super().__init__(container)

        self.key = key
        self.value = value
        self.snippetsMap = snippetsMap
        self.data = data
        self.container = container

        if state == FormState.ADD:
            self.action_button_label = "Add"
            self.old_key = None
        else:
            self.action_button_label = "Save"
            self.old_key = key

        consts.LEFT_PAD = 15
        consts.TOP_PAD = 15
        
        # snippet label
        self.snippet_label = Label(self.container, text='Snippet')
        self.snippet_label.place(x=consts.LEFT_PAD, y=consts.TOP_PAD+3)

        # snippet entry
        self.snippet = tk.StringVar()
        self.key_entry = Entry(self.container, textvariable=self.snippet)
        self.key_entry.insert(END, self.key)
        self.key_entry.place(x=consts.LEFT_PAD+60, y=consts.TOP_PAD)
        self.key_entry.focus()

        # text label
        self.text_label = Label(self.container, text='Text')
        self.text_label.place(x=consts.LEFT_PAD, y=consts.TOP_PAD+46)

        # snippet text
        self.value_text = Text(self.container, height=7, width=30)
        self.value_text.insert(END, self.value)
        self.value_text.place(x=consts.LEFT_PAD+60, y=consts.TOP_PAD+46)
        

        # cancel button
        self.cancel_button = Button(self.container, text='Cancel', width=7, command = self.container.quit_window, bootstyle="danger")
        self.cancel_button.place(x=consts.LEFT_PAD+120, y=consts.TOP_PAD+180)

        # save button
        self.action_button = Button(self.container, text=self.action_button_label, width=7)
        self.action_button['command'] = self.action_button_clicked
        self.action_button.place(x=consts.LEFT_PAD+190, y=consts.TOP_PAD+180)

    def action_button_clicked(self):
        key = self.key_entry.get()
        if key != None and len(key) > 0:
            if self.old_key != None:
                self.snippetsMap.pop(self.old_key)
                
            self.snippetsMap[key] = self.value_text.get("1.0", "end").rstrip("\n")

            DAL.save_snippets_to_db(self.data, self.snippetsMap)

            self.container.master.refresh_listbox()

            self.container.quit_window()