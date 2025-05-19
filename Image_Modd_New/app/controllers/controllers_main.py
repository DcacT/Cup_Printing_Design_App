from ..models.models_main import Model
from ..views.views_main import View
from .HomeController import HomeController
from .NewTempController import NewTempController
from .CfgTempController import CfgTempController
class Controller: 
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.home_controller = HomeController(model, view)
        self.newtemp_controller = NewTempController(model, view)
        self.CfgTempController = CfgTempController(model, view)

    def start(self):
        self.view.start_mainloop()