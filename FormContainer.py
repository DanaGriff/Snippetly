import tkinter as tk
from ttkbootstrap.constants import *
from Enums import FormState
import consts
import utils

class FormContainer(tk.Toplevel):
    def __init__(self, master, state):
        tk.Toplevel.__init__(self)

        self.master = master
        self.state = state

        if state == FormState.ADD:
            self.action_title = "Add Snippet"
        else:
            self.action_title = "Edit Snippet"

        window_width = 290
        window_height = 250

        utils.set_window_icon(self)

        self.title(self.action_title)
        self.resizable(False, False)
        self.geometry(utils.set_window_size(self, window_width, window_height))
        self.transient(self.master) # set to be on top of the main window
        self.grab_set() # hijack all commands from the master (clicks on the main window are ignored)

        consts.LEFT_PAD = 15
        consts.TOP_PAD = 15
        
    def quit_window(self):
        self.destroy()