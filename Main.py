import DAL
from Window import Window
from MainApp import MainApp

if __name__ == "__main__":
    data = DAL.retrieve_db()

    window = Window()
    MainApp(window, data)

    window.mainloop()