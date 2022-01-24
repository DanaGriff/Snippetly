import keyboard
import DAL

def hook():
    data = DAL.retrieve_db()
    snippetsMap = DAL.get_snippets_dict(data)

    for key, value in snippetsMap.items():
        keyboard.add_abbreviation(key, value)

def unhook():
    keyboard.unhook_all()
