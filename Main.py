import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.ttk import Frame, Button, Label, Style, Entry
from tkinter import Text, Listbox
import keyboard
import sys
import os
import json

data = ""
snippets = ""
snippetsMap = {}

def populate_snippets_map(snippets):
    for snippet in snippets:
        abbreviation = snippet["abbreviation"];
        text_to_copy = snippet["text"];

        if len(text_to_copy) > 0:
            snippetsMap[abbreviation] = text_to_copy;
        else:
            template = snippet["template"];

            if len(template) > 0:
                fo = open(full_path('snippets', template)).read()
                snippetsMap[abbreviation] = fo;

def full_path(sub_folder, file_name):
    if getattr(sys, 'frozen', False):  # running in a bundle
        if len(sub_folder) > 0:
            dir_path = os.path.join(os.path.dirname(sys.executable), sub_folder)
        else:
            dir_path = os.path.dirname(sys.executable)
        return os.path.join(dir_path, file_name)
    else:  # running live
        if len(sub_folder) > 0:
            dir_path = os.path.join(os.path.dirname(__file__), sub_folder)
        else:
            dir_path = os.path.dirname(__file__)
        return os.path.join(dir_path, file_name)

def retrieve_db():
    with open(full_path('', 'db.json')) as settings_file:
        try:
            json_data = json.load(settings_file)
            return json_data
        except ValueError:
            print('The JSON File is missing or corrupted')
            sys.exit()

def add_hotkeys():
    for key, value in snippetsMap.items():
        keyboard.add_abbreviation(key, value)

    #keyboard.wait()

class MainFrame(Frame):
    def __init__(self, container):
        super().__init__(container)

        # field options
        options = {'padx': 5, 'pady': 5}

        # abbreviation label
        self.abbreviation_label = Label(self, text='Abbreviation')
        self.abbreviation_label.grid(column=0, row=0, sticky=tk.W, **options)

        # snippet label
        self.snippet_label = Label(self, text='Snippet')
        self.snippet_label.grid(column=0, row=1, sticky=tk.W, **options)

        # abbreviation entry
        self.abbreviation = tk.StringVar()
        self.abbreviation_entry = Entry(self, textvariable=self.abbreviation)
        self.abbreviation_entry.grid(column=1, row=0, **options)
        self.abbreviation_entry.focus()

        # snippet text
        self.snippet_text = Text(self, height=5, width=30)
        self.snippet_text.grid(column=1, row=1, **options)

        # save button
        self.save_button = Button(self, text='save')
        self.save_button['command'] = self.save_button_clicked
        self.save_button.grid(column=2, row=0, sticky=tk.W, **options)

        # new button
        self.new_button = Button(self, text='new')
        self.new_button['command'] = self.new_button_clicked
        self.new_button.grid(column=2, row=1, sticky=tk.W, **options)

        # delete button
        self.delete_button = Button(self, text='delete')
        self.delete_button['command'] = self.delete_button_clicked
        self.delete_button.grid(column=2, row=2, sticky=tk.W, **options)

        #abbreviations list
        abbreviations_list = [*snippetsMap]

        self.selectedItem = tk.StringVar(value=abbreviations_list)

        self.listbox = Listbox(self,
            listvariable=self.selectedItem,
            height=10,
            selectmode='SINGLE')
        self.listbox.grid(column=0, row=3, sticky=tk.W, **options)
        self.listbox.bind('<<ListboxSelect>>', self.item_selected)


        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)

    def save_button_clicked(self):
        print('save clicked');

    def new_button_clicked(self):
        print('new clicked');

    def delete_button_clicked(self):
        print('delete clicked');

    def item_selected(self, event):
        selected = ",".join([self.listbox.get(i) for i in self.listbox.curselection()])

        self.snippet_text.delete('1.0', "end")
        self.snippet_text.insert(tk.END, snippetsMap[selected])

        self.abbreviation_entry.delete(0, "end")
        self.abbreviation_entry.insert(0, selected)



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Auto Snippet')
        self.geometry(self.set_window_size())
        self.resizable(False, False)

    def set_window_size(self):
        window_width = 500
        window_height = 400

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # return the position of the window to the center of the screen
        return f'{window_width}x{window_height}+{center_x}+{center_y}'

if __name__ == "__main__":
    data = retrieve_db()
    populate_snippets_map(data["snippets"])

    #add_hotkeys();  ##TODO work run when window not minimized, add label that hotkeys are disabled when window is open

    app = App()
    MainFrame(app)
    app.mainloop()