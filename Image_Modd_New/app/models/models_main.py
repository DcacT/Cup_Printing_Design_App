from .ConfigSheet import ConfigSheet
from .ImageProcessor import ImageProcessor
from .TemplateManager import TemplateManager
class Model:
    def __init__(self):
        # self.config_sheet = ConfigSheet()
        self.template_manager = TemplateManager()
        self.image_processor = ImageProcessor(self.template_manager)
        pass