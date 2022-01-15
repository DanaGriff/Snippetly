import DAL
from Window import Window
from MainFrame import MainFrame

if __name__ == "__main__":
    data = DAL.retrieve_db()

    window = Window()
    MainFrame(window, data)

    window.mainloop()

    ##TODO check empty db