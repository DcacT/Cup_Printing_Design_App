from .ConfigSheet import ConfigSheet
from .ImageProcessor import ImageProcessor
class Model:
    def __init__(self):
        self.config_sheet = ConfigSheet()
        self.image_processor = ImageProcessor(self.config_sheet)
        pass