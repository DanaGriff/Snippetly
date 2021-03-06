from pystray import MenuItem, Menu
import pystray
from PIL import Image
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import Abbreviations
import consts
import utils

class AppContainer(ttk.Window):
    def __init__(self):
        super().__init__(themename="litera")

        window_width = 295
        window_height = 300
        self.geometry(utils.set_window_size(self, window_width, window_height))

        utils.set_window_icon(self)
        
        self.title(consts.APP_NAME)
        
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.hide_window)

    # Define a function for quit the window
    def quit_window(self):
        self.icon.stop()
        self.destroy()

    # Define a function to show the window again
    def show_window(self):
        Abbreviations.unhook()

        self.icon.stop()
        self.after(0, self.deiconify())

    # Hide the window and show on the system taskbar
    def hide_window(self):
        Abbreviations.hook()

        self.withdraw()
        image = Image.open(consts.APP_ICON)

        menu = Menu(
            MenuItem('Show', self.show_window, default=True),  # set 'Show' as the default action
            MenuItem('Quit', self.quit_window)
        )

        self.icon = pystray.Icon("name", image, consts.APP_NAME, menu)
        self.icon.run()