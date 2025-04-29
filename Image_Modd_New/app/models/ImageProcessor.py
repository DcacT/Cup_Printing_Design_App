import os
import cv2

from PIL import Image,ImageTk

class ImageProcessor:
    def __init__(self, config_sheet):
        self.template_folder_name = ""
        self.template_data = {}
        self.config_sheet = config_sheet
        
        self.base_template_image = None
        self.processed_template_image = None
        
        self.resize_ratio = 0.5
        pass
    
    def load_template(self, template_folder_name, template_data = None):
        
        self.template_folder_name = template_folder_name
        self.template_data = template_data if template_data is not None else self.config_sheet.read_rows(folder_name = template_folder_name)
        
        self.load_base_template_image()
        self.processed_template_image = self.base_template_image

    
    def load_base_template_image(self):
        self_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(self_path, f'../../data/templates/{self.template_folder_name}/template_image.png', )
        self.base_template_image = cv2.imread(path, cv2.IMREAD_COLOR)

    def get_display_image(self):
        h, w = self.processed_template_image.shape[:2]
        img_rgb = cv2.cvtColor(self.processed_template_image, cv2.COLOR_BGR2RGB)
        img_resize = cv2.resize(img_rgb, (int(w*self.resize_ratio), int(h*self.resize_ratio)) )
        img_pil = Image.fromarray(img_resize)
        img_tk = ImageTk.PhotoImage(img_pil)
        return img_tk