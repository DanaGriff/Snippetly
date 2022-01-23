import keyboard
import DAL

def hook():
    data = DAL.retrieve_db()
    hotkeysMap = DAL.get_hotkeys_dict(data)

    for key, value in hotkeysMap.items():
        keyboard.add_abbreviation(key, value)

def unhook():
    keyboard.unhook_all()
