import DAL
from AppContainer import AppContainer
from AppFrame import AppFrame

if __name__ == "__main__":
    data = DAL.retrieve_db()

    AppContainer = AppContainer()
    AppFrame(AppContainer, data)

    AppContainer.mainloop()