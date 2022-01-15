import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.ttk import Frame, Button, Label, Entry
from tkinter import Text, Listbox, Menu, Toplevel, messagebox
import DAL
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class MainFrame(Frame):
    def __init__(self, container, data, hotkeysMap):
        super().__init__(container)

        self.hotkeysMap = hotkeysMap
        self.data = data

        menubar = Menu(container)
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Documnetation", command=self.documnetation_clicked)
        helpmenu.add_command(label="About..", command=self.about_clicked)
        menubar.add_cascade(label="Help", menu=helpmenu)

        container.config(menu=menubar)

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

        # delete button
        self.delete_button = Button(container, text='Delete', width=7, bootstyle="danger")
        self.delete_button['command'] = self.delete_button_clicked
        self.delete_button.place(x=LEFT_PAD+82, y=TOP_PAD+175)

        # hotkey label
        self.hotkey_label = Label(container, text='Hotkey')
        self.hotkey_label.place(x=LEFT_PAD+200, y=TOP_PAD+3)

        # hotkey entry
        self.hotkey = tk.StringVar()
        self.key_entry = Entry(container, textvariable=self.hotkey)
        self.key_entry.place(x=LEFT_PAD+260, y=TOP_PAD)
        
        # text label
        self.text_label = Label(container, text='Text')
        self.text_label.place(x=LEFT_PAD+200, y=TOP_PAD+46)

        # hotkey text
        self.value_text = Text(container, height=7, width=30)
        self.value_text.place(x=LEFT_PAD+260, y=TOP_PAD+46)

        # save button
        self.save_button = Button(container, text='Save', width=10)
        self.save_button['command'] = self.save_button_clicked
        self.save_button.place(x=LEFT_PAD+370, y=TOP_PAD+175)


    def item_selected(self, event):
        self.selectedItem = event.widget.get(event.widget.curselection()[0])

        selectedText = self.hotkeysMap[self.selectedItem]

        self.value_text.delete('1.0', "end")
        self.value_text.insert(tk.END, selectedText)

        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, self.selectedItem)

    def save_button_clicked(self):
        key = self.key_entry.get()
        self.hotkeysMap[key] = self.get_hotkey_value()

        self.reset_form()

        self.refresh_listbox()
        self.save_hotkeys_to_db()

    def add_button_clicked(self):
        self.listbox.selection_clear(0, tk.END)
        self.listbox.insert(tk.END, "")
        self.listbox.selection_set(self.listbox.size()-1)

        self.reset_form()

        self.key_entry.focus_set()

    def delete_button_clicked(self):
        self.hotkeysMap.pop(self.selectedItem)
        
        self.refresh_listbox()
        self.save_hotkeys_to_db()

    def get_hotkey_value(self):
        return self.value_text.get("1.0", "end")

    def reset_form(self):
        self.value_text.delete('1.0', "end")
        self.value_text.insert(tk.END, "")

        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, "")

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

    def documnetation_clicked(self):
        messagebox.showinfo(title="Documenation", message="PLACEHOLDER")

    def about_clicked(self):
        messagebox.showinfo(title="About", message="PLACEHOLDER")