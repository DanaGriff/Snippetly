import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.ttk import Frame, Button, Label, Entry
from tkinter import Text, Listbox, Menu, Toplevel, Message
import DAL
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webbrowser

class MainApp(Frame):

    def __init__(self, container, data):
        super().__init__(container)

        self.selectedItem = None
        self.hotkeysMap = DAL.get_hotkeys_dict(data)
        self.data = data

        LEFT_PAD = 15
        TOP_PAD = 15
        
        #hotkeys listbox
        items = tk.StringVar(value=[*self.hotkeysMap])

        self.listbox = Listbox(container,
            listvariable=items,
            height=9,
            width=18,
            font=('TkDefaultFont', 11),
            selectmode='SINGLE')
        self.listbox.place(x=LEFT_PAD, y=TOP_PAD)
        self.listbox.bind('<<ListboxSelect>>', self.item_selected)
        self.listbox.focus()

        # Add button
        self.add_button = Button(container, text='Add', width=7, bootstyle="success")
        self.add_button['command'] = self.add_button_clicked
        self.add_button.place(x=LEFT_PAD, y=TOP_PAD+175)

        # edit button
        self.edit_button = Button(container, text='Edit', width=7, bootstyle="default")
        self.edit_button['command'] = self.edit_button_clicked
        self.edit_button.place(x=LEFT_PAD+75, y=TOP_PAD+175)

        # delete button
        self.delete_button = Button(container, text='Delete', width=7, bootstyle="danger")
        self.delete_button['command'] = self.delete_button_clicked
        self.delete_button.place(x=LEFT_PAD+120, y=TOP_PAD+175)

        # hotkey label
        self.hotkey_label = Label(container, text='Hotkey')
        self.hotkey_label.place(x=LEFT_PAD+200, y=TOP_PAD+3)

        # hotkey entry
        self.hotkey = tk.StringVar()
        self.key_entry = Entry(container, textvariable=self.hotkey, state = "disabled")
        self.key_entry.place(x=LEFT_PAD+260, y=TOP_PAD)
        
        # text label
        self.text_label = Label(container, text='Text')
        self.text_label.place(x=LEFT_PAD+200, y=TOP_PAD+46)

        # hotkey text
        self.value_text = Text(container, height=7, width=30, state = "disabled")
        self.value_text.place(x=LEFT_PAD+260, y=TOP_PAD+46)

        # save button
        self.save_button = Button(container, text='Save', width=10)
        self.save_button['command'] = self.save_button_clicked
        self.save_button['state'] = tk.DISABLED
        self.save_button.place(x=LEFT_PAD+370, y=TOP_PAD+175)

        
        self.copyrights_label = Label(container, text="© Dana Griff", foreground="blue", cursor="hand2")
        self.copyrights_label.bind("<Button-1>", lambda e: self.open_url("https://github.com/DanaGriff"))
        self.copyrights_label.place(x=LEFT_PAD+390, y=TOP_PAD+230)


    def item_selected(self, event):
        # self.switch_form_state("normal")
        self.selectedItem = event.widget.get(event.widget.curselection()[0])

        # selectedText = self.hotkeysMap[self.selectedItem]

        # self.value_text.delete('1.0', "end")
        # self.value_text.insert(tk.END, selectedText)

        # self.key_entry.delete(0, "end")
        # self.key_entry.insert(0, self.selectedItem)

    def save_button_clicked(self):
        key = self.key_entry.get()
        if key != None and len(key) > 0:
            self.hotkeysMap[key] = self.get_hotkey_value()

            self.save_hotkeys_to_db()

        self.reset_form()
        self.refresh_listbox()
        
            
    def add_button_clicked(self):
        self.selectedItem = None
        self.listbox.selection_clear(0, tk.END)
        self.listbox.insert(tk.END, "")
        self.listbox.selection_set(self.listbox.size()-1)

        self.reset_form()
        self.switch_form_state("normal")
        self.key_entry.focus_set()

    def delete_button_clicked(self):
        if self.selectedItem != None:
            self.hotkeysMap.pop(self.selectedItem)
        
        self.reset_form()
        self.refresh_listbox()
        self.save_hotkeys_to_db()

    def edit_button_clicked(self):
        if self.selectedItem != None:
            self.switch_form_state("normal")

            selectedText = self.hotkeysMap[self.selectedItem]

            self.value_text.delete('1.0', "end")
            self.value_text.insert(tk.END, selectedText)

            self.key_entry.delete(0, "end")
            self.key_entry.insert(0, self.selectedItem)

    def get_hotkey_value(self):
        return self.value_text.get("1.0", "end").rstrip("\n")

    def reset_form(self):
        self.value_text.delete('1.0', "end")
        self.value_text.insert(tk.END, "")

        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, "")

        self.switch_form_state("disabled")

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)

        for i in self.hotkeysMap.keys():
            self.listbox.insert(tk.END, i)

    def save_hotkeys_to_db(self):
        self.data['hotkeys'] = []
        for key, value in self.hotkeysMap.items():
            attribute = { 'hotkey' : key, 'text' : value}

            self.data['hotkeys'].append(attribute)

        DAL.save_to_db(self.data)

    def open_url(self, url):
        webbrowser.open_new(url)

    def switch_form_state(self, set_state):
        self.save_button['state'] = set_state
        self.value_text.configure(state = set_state)
        self.key_entry.configure(state = set_state, )