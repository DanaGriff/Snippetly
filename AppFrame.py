import tkinter as tk
from tkinter.ttk import Button, Label
from tkinter import Listbox, Menu
from tkinter.messagebox import askyesno, showinfo
import DAL
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webbrowser
from Enums import FormState
import consts
from FormContainer import FormContainer
from FormFrame import FormFrame

class AppFrame(ttk.Frame):
    def __init__(self, container, data):
        super().__init__(container)

        self.selectedItem = None
        self.snippetsMap = DAL.get_snippets_dict(data)
        self.data = data
        self.container = container
        
        # snippet label
        self.available_Snippets_label = Label(container, text='Available Snippets:')
        self.available_Snippets_label.place(x=consts.LEFT_PAD, y=consts.TOP_PAD)

        #snippets listbox
        items = tk.StringVar(value=[*self.snippetsMap])
        self.listbox = Listbox(container, listvariable=items, height=10, width=15, font=('TkDefaultFont', 11), selectmode='SINGLE')
        self.listbox.bind('<<ListboxSelect>>', self.item_selected)
        self.listbox.place(x=consts.LEFT_PAD, y=consts.TOP_PAD+20)

        # Add button
        self.add_button = Button(container, text='Add', width=7, command = lambda: self.open_form(FormState.ADD), bootstyle="success")
        self.add_button.place(x=consts.LEFT_PAD+185, y=consts.TOP_PAD+20)

        # edit button
        self.edit_button = Button(container, text='Edit', width=7, command = lambda: self.open_form(FormState.EDIT) , bootstyle="default", state = "disabled")
        self.edit_button.place(x=consts.LEFT_PAD+185, y=consts.TOP_PAD+60)

        # delete button
        self.delete_button = Button(container, text='Delete', width=7, command = self.delete_button_clicked, bootstyle="danger", state = "disabled")
        self.delete_button.place(x=consts.LEFT_PAD+185, y=consts.TOP_PAD+100)

        self.copyrights_label = Label(container, text=consts.COPYRIGHTS_TEXT, foreground="blue", cursor="hand2")
        self.copyrights_label.bind("<Button-1>", lambda e: self.open_url(consts.GITHUB_LINK))
        self.copyrights_label.place(x=consts.LEFT_PAD+180, y=consts.TOP_PAD+230)

        menubar = Menu(container)  
        help = Menu(menubar, tearoff=0)  
        help.add_command(label="About",  command=lambda: showinfo(
                                        title='About Snippetly',
                                        message='Snippetly is an app that replaces text by listening to your keyboard input.\n\nDefine which snippet you want to be replaced, and the text you want to replace it with.\n\nPlease keep the app running in the background.'))  
        menubar.add_cascade(label="Help", menu=help)  
        self.container.config(menu=menubar)  

    def item_selected(self, event):
        if len(event.widget.curselection()) > 0: 
            self.selectedItem = event.widget.get(event.widget.curselection()[0])
            self.change_buttons_state("normal")

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)

        for i in self.snippetsMap.keys():
            self.listbox.insert(tk.END, i)
    
    def delete_button_clicked(self):
        if self.selectedItem != None:
            answer = askyesno(title='Delete Snippet',
                          message='Are you sure that you want to delete?',
                          icon = 'warning')
            if answer:
                self.snippetsMap.pop(self.selectedItem)
                self.refresh_listbox()
                DAL.save_snippets_to_db(self.data, self.snippetsMap)
                self.change_buttons_state("disabled")

    def open_url(self, url):
        webbrowser.open_new(url)
    
    def open_form(self, state):
        key = ''
        value = ''
        
        if state == FormState.EDIT:
            key = self.selectedItem
            value = self.snippetsMap[self.selectedItem]
        
        formContainer = FormContainer(self, state)
        FormFrame(formContainer, state, key, value, self.data, self.snippetsMap)

    def change_buttons_state(self, buttonState):
        self.edit_button.configure(state = buttonState)
        self.delete_button.configure(state = buttonState)