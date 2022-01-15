import keyboard

class Abbreviations():
    def __init__(self, hotkeysMap):
        super().__init__()

        self.hotkeysMap = hotkeysMap

    def add(self):
        for key, value in self.hotkeysMap.items():
            keyboard.add_abbreviation(key, value)
    
    def unhook(self):
        keyboard.unhook_all()


    