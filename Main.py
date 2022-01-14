import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.ttk import Frame, Button, Label, Style, Entry
from tkinter import Text, Listbox
import keyboard
import sys
import os
import json
from pystray import MenuItem, Menu
import pystray
from PIL import Image, ImageTk

data = ""
snippets = ""
snippetsMap = {}

def populate_snippets_map(snippets):
    for snippet in snippets:
        abbreviation = snippet["abbreviation"];
        text_to_copy = snippet["text"];

        snippetsMap[abbreviation] = text_to_copy;

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

        # snippet text
        self.snippet_text = Text(self, height=5, width=30)
        self.snippet_text.grid(column=1, row=1, **options)

        # save button
        self.save_button = Button(self, text='save', width=10)
        self.save_button['command'] = self.save_button_clicked
        self.save_button.grid(column=2, row=0, sticky=tk.W, **options)

        # Add button
        self.add_button = Button(self, text='Add', width=10)
        self.add_button['command'] = self.add_button_clicked
        self.add_button.grid(column=2, row=1, sticky=tk.W, **options)

        # delete button
        self.delete_button = Button(self, text='delete', width=10)
        self.delete_button['command'] = self.delete_button_clicked
        self.delete_button.grid(column=2, row=2, sticky=tk.W, **options)

        #abbreviations list
        self.abbreviations_list = [*snippetsMap]

        selectedItem = tk.StringVar(value=self.abbreviations_list)

        self.listbox = Listbox(self,
            listvariable=selectedItem,
            height=10,
            selectmode='SINGLE')
        self.listbox.grid(column=0, row=3, sticky=tk.W, **options)
        self.listbox.bind('<<ListboxSelect>>', self.item_selected)
        self.listbox.focus()

        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)

    def save_button_clicked(self):
        key = self.abbreviation_entry.get()
        snippetsMap[key] = self.get_snippet_value()
        ##TODO refresh list box

    def add_button_clicked(self):
        self.save_button_clicked()
        ##TODO refresh list box

    def delete_button_clicked(self):
        snippetsMap.pop(self.selectedItem)
        ##TODO refresh list box


    def get_snippet_value(self):
        return self.snippet_text.get("1.0", "end")

    def item_selected(self, event):
        selectedItem = ",".join([self.listbox.get(i) for i in self.listbox.curselection()])

        self.snippet_text.delete('1.0', "end")
        self.snippet_text.insert(tk.END, snippetsMap[selectedItem])

        self.abbreviation_entry.delete(0, "end")
        self.abbreviation_entry.insert(0, selectedItem)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Auto Snippet')
        self.geometry(self.set_window_size())
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.hide_window)
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

    # Define a function for quit the window
    def quit_window(self, icon, item):
        icon.stop()
        self.destroy()

    # Define a function to show the window again
    def show_window(self, icon, item):
        keyboard.unhook_all()

        icon.stop()
        self.after(0, self.deiconify())

    # Hide the window and show on the system taskbar
    def hide_window(self):
        add_hotkeys();

        self.withdraw()
        image = Image.open("C:\\Users\\Dana\\Downloads\\1768528-200.png")

        menu = Menu(
            MenuItem('Quit', self.quit_window),
            MenuItem('Show', self.show_window, default=True)  # set 'Show' as the default action
        )

        icon = pystray.Icon("name", image, "My System Tray Icon", menu)
        icon.run()


if __name__ == "__main__":
    data = retrieve_db()
    populate_snippets_map(data["snippets"])

    app = App()
    MainFrame(app)

    app.mainloop()


#add button
#delete button
#save json
#add start\stop button
#double clicking text removes it
#\n not written properly
