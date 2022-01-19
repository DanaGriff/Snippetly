import DAL
from MainFrame import MainFrame
from MainApp import MainApp

if __name__ == "__main__":
    data = DAL.retrieve_db()

    mainFrame = MainFrame()
    MainApp(mainFrame, data)

    mainFrame.mainloop()