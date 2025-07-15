from .ConfigSheet import ConfigSheet
from .ImageProcessor import ImageProcessor
from .TemplateManager import TemplateManager
from .project import Project
class Model:
    def __init__(self):
        # self.config_sheet = ConfigSheet()
        self.template_manager = TemplateManager()
        self.image_processor = ImageProcessor(self.template_manager)
        self.project = Project()
        pass