import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.ttk import Frame, Button, Label, Entry
from tkinter import Text, Listbox
import DAL

class MainFrame(Frame):
    def __init__(self, container, data, hotkeysMap):
        super().__init__(container)

        self.hotkeysMap = hotkeysMap
        self.data = data

        # field options
        options = {'padx': 5, 'pady': 5}

        # hotkey label
        self.hotkey_label = Label(self, text='Hotkey')
        self.hotkey_label.grid(column=2, row=0, sticky=tk.W, **options)

        # hotkey entry
        self.hotkey = tk.StringVar()
        self.key_entry = Entry(self, textvariable=self.hotkey)
        self.key_entry.grid(column=3, row=0, **options)
        
        # text label
        self.text_label = Label(self, text='Text')
        self.text_label.grid(column=2, row=1, sticky=tk.W, **options)

        # hotkey text
        self.value_text = Text(self, height=5, width=30)
        self.value_text.grid(column=3, row=1, columnspan=2, **options)

        # save button
        self.save_button = Button(self, text='save', width=10)
        self.save_button['command'] = self.save_button_clicked
        self.save_button.grid(column=4, row=2, sticky=tk.W, **options)

        # Add button
        self.add_button = Button(self, text='Add', width=10)
        self.add_button['command'] = self.add_button_clicked
        self.add_button.grid(column=0, row=2, sticky=tk.W, **options)

        # delete button
        self.delete_button = Button(self, text='delete', width=10)
        self.delete_button['command'] = self.delete_button_clicked
        self.delete_button.grid(column=1, row=2, sticky=tk.W, **options)

        #hotkeys listbox
        items = tk.StringVar(value=[*self.hotkeysMap])

        self.listbox = Listbox(self,
            listvariable=items,
            height=10,
            selectmode='SINGLE')
        self.listbox.grid(column=0, row=0, columnspan=2, rowspan=2, sticky=tk.W, **options)
        self.listbox.bind('<<ListboxSelect>>', self.item_selected)
        self.listbox.focus()

        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)

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