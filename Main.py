import DAL
from MainContainer import MainContainer
from MainApp import MainApp

if __name__ == "__main__":
    data = DAL.retrieve_db()

    MainContainer = MainContainer()
    MainApp(MainContainer, data)

    MainContainer.mainloop()