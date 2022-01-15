import keyboard
import DAL

def hook():
    data = DAL.retrieve_db()
    hotkeysMap = DAL.populate_hotkeys_map(data["hotkeys"])

    for key, value in hotkeysMap.items():
        keyboard.add_abbreviation(key, value)

def unhook(self):
    keyboard.unhook_all()
