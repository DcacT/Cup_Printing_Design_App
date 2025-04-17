from .models.models_main import Model
from .views.views_main import View
from .controllers.controllers_main import Controller

def main():
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.start()

if __name__ == "__main__":
    main()