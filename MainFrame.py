from pystray import MenuItem, Menu
import pystray
from PIL import Image
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import Abbreviations

class MainFrame(ttk.Window):
    def __init__(self):
        super().__init__(themename="litera")

        self.iconbitmap("./images/logo.ico")
        self.title('Hotkeys Manager')
        self.geometry(self.set_window_size())
        self.resizable(False, False)

        self.protocol('WM_DELETE_WINDOW', self.hide_window)
    def set_window_size(self):
        window_width = 485
        window_height = 270

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
        self.abbreviations.unhook()

        icon.stop()
        self.after(0, self.deiconify())

    # Hide the window and show on the system taskbar
    def hide_window(self):
        Abbreviations.hook()

        self.withdraw()
        image = Image.open("images/logo.ico")

        menu = Menu(
            MenuItem('Quit', self.quit_window),
            MenuItem('Show', self.show_window, default=True)  # set 'Show' as the default action
        )

        icon = pystray.Icon("name", image, "Hotkeys Manager", menu)
        icon.run()