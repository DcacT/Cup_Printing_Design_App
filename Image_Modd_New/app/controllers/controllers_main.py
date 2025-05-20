from ..models.models_main import Model
from ..views.views_main import View
from .HomeController import HomeController
from .NewTempController import NewTempController
from .CfgTempController import CfgTempController
from .NewProjectController import NewProjController

class Controller: 
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.home_controller = HomeController(model, view)
        self.new_temp_controller = NewTempController(model, view)
        self.cfg_temp_controller = CfgTempController(model, view)
        self.new_proj_controller = NewProjController(model, view)

    def start(self):
        self.view.start_mainloop()