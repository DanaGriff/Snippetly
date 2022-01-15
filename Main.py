import DAL
from Window import Window
from MainFrame import MainFrame
from Abbreviations import Abbreviations

if __name__ == "__main__":
    data = DAL.retrieve_db()
    
    hotkeysMap = DAL.populate_hotkeys_map(data["hotkeys"])

    abbreviations = Abbreviations(hotkeysMap)
    window = Window(abbreviations)
    MainFrame(window, data, hotkeysMap)

    window.mainloop()

    ##TODO check empty db