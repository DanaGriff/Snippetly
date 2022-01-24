import DAL
from AppContainer import AppContainer
from AppFrame import AppFrame

if __name__ == "__main__":
    data = DAL.retrieve_db()

    appContainer = AppContainer()
    AppFrame(appContainer, data)

    appContainer.mainloop()