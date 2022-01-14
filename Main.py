import DAL
from App import App
from MainFrame import MainFrame

data = ""
hotkeys = ""
hotkeysMap = {}

def populate_hotkeys_map(hotkeys):
    for hotkey_i in hotkeys:
        hotkey = hotkey_i["hotkey"]
        text_to_copy = hotkey_i["text"]

        hotkeysMap[hotkey] = text_to_copy

if __name__ == "__main__":
    data = DAL.retrieve_db()
    populate_hotkeys_map(data["hotkeys"])

    app = App()
    MainFrame(app, hotkeysMap)

    app.mainloop()