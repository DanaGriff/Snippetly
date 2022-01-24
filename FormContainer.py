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

class FormContainer(tk.Toplevel):

    def __init__(self, master, state):
        tk.Toplevel.__init__(self)

        self.master = master
        self.state = state

        if state == FormState.ADD:
            self.action_title = "Add Snippet"
        else:
            self.action_title = "Edit Snippet"

        self.iconbitmap(Constants.APP_ICON)
        self.title(self.action_title)
        self.resizable(False, False)
        self.geometry(self.set_window_size())
        self.transient(self.master) # set to be on top of the main window
        self.grab_set() # hijack all commands from the master (clicks on the main window are ignored)

        Constants.LEFT_PAD = 15
        Constants.TOP_PAD = 15
        
    def quit_window(self):
        self.destroy()

    def set_window_size(self):
        window_width = 290
        window_height = 250

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)+20
        center_y = int(screen_height / 2 - window_height / 2)+20

        # return the position of the window to the center of the screen
        return f'{window_width}x{window_height}+{center_x}+{center_y}'