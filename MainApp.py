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

class MainApp(Frame):
    def __init__(self, container, data):
        super().__init__(container)

        self.selectedItem = None
        self.hotkeysMap = DAL.get_hotkeys_dict(data)
        self.data = data
        self.container = container
        
        # hotkey label
        self.available_Snippets_label = Label(container, text='Available Snippets:')
        self.available_Snippets_label.place(x=Constants.LEFT_PAD, y=Constants.TOP_PAD)

        #hotkeys listbox
        items = tk.StringVar(value=[*self.hotkeysMap])
        self.listbox = Listbox(container, listvariable=items, height=10, width=20, font=('TkDefaultFont', 11), selectmode='SINGLE')
        self.listbox.bind('<<ListboxSelect>>', self.item_selected)
        self.listbox.place(x=Constants.LEFT_PAD, y=Constants.TOP_PAD+20)

        # Add button
        self.add_button = Button(container, text='Add', width=7, command = lambda: self.open_snippets_form(FormState.ADD), bootstyle="success")
        self.add_button.place(x=Constants.LEFT_PAD+170, y=Constants.TOP_PAD+20)

        # edit button
        self.edit_button = Button(container, text='Edit', width=7, command = lambda: self.open_snippets_form(FormState.EDIT) , bootstyle="default", state = "disabled")
        self.edit_button.place(x=Constants.LEFT_PAD+170, y=Constants.TOP_PAD+60)

        # delete button
        self.delete_button = Button(container, text='Delete', width=7, command = self.delete_button_clicked, bootstyle="danger", state = "disabled")
        self.delete_button.place(x=Constants.LEFT_PAD+170, y=Constants.TOP_PAD+100)

        self.copyrights_label = Label(container, text=Constants.COPYRIGHTS_TEXT, foreground="blue", cursor="hand2")
        self.copyrights_label.bind("<Button-1>", lambda e: self.open_url(Constants.GITHUB_LINK))
        self.copyrights_label.place(x=Constants.LEFT_PAD+180, y=Constants.TOP_PAD+230)

    def item_selected(self, event):
        self.selectedItem = event.widget.get(event.widget.curselection()[0])
        self.changeButtonsState("normal")

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)

        for i in self.hotkeysMap.keys():
            self.listbox.insert(tk.END, i)
    
    def delete_button_clicked(self):
        if self.selectedItem != None:
            answer = askyesno(title='Delete Snippet',
                          message='Are you sure that you want to delete?')
            if answer:
                self.hotkeysMap.pop(self.selectedItem)
                self.refresh_listbox()
                DAL.save_hotkeys_to_db(self.data, self.hotkeysMap)
                self.changeButtonsState("disabled")

    def open_url(self, url):
        webbrowser.open_new(url)
    
    def open_snippets_form(self, state):
        if state == FormState.ADD:
            SnippetsForm(tk.Toplevel(self.container), state, '', '', self.data, self.hotkeysMap)
        elif self.selectedItem != None:
            value = self.hotkeysMap[self.selectedItem]
            SnippetsForm(tk.Toplevel(self.container), state, self.selectedItem, value, self.data, self.hotkeysMap)

    def changeButtonsState(self, buttonState):
        self.edit_button.configure(state = buttonState)
        self.delete_button.configure(state = buttonState)