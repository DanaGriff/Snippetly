import base64, os
import consts

def set_window_size(root, window_width, window_height):
    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)+20
    center_y = int(screen_height / 2 - window_height / 2)+20

    # return the position of the window to the center of the screen
    return f'{window_width}x{window_height}+{center_x}+{center_y}'

def set_window_icon(root):
    icondata = base64.b64decode(consts.APP_ICON_BASE_64)
    ## The temp file is icon.ico
    tempFile= "icon.ico"
    iconfile= open(tempFile,"wb")
    ## Extract the icon
    iconfile.write(icondata)
    iconfile.close()
    root.wm_iconbitmap(tempFile)
    ## Delete the tempfile
    os.remove(tempFile)