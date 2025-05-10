import os
import cv2
import numpy as np
from PIL import Image,ImageTk

class ImageProcessor:
    def __init__(self, config_sheet):
        self.template_folder_name = ""
        self.template_data = {}
        self.config_sheet = config_sheet
        
        self.base_template_image = None
        self.processed_template_image = None
        
        self.all_contours = []
        
        
        self.resize_ratio = 0.5
        pass
    
    def get_config(self, key):
        return float(self.template_data[key])
    
    def generate_contours(self):
        gray = cv2.cvtColor(self.base_template_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)    
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        new_contours = []
        for contour in contours:
            if (len(contour) > self.get_config('PX_Min') 
            and len(contour) < self.get_config('PX_Max')):
                x, y, w, h = cv2.boundingRect(contour)  # Get bounding box (x, y, width, height)
                aspect_ratio = w / h  # Width divided by height

                if ((aspect_ratio < self.get_config('Horizontal_Limit') and not self.get_config('Horizontal_Limit') == -1)
                    or (aspect_ratio > self.get_config('Vertical_Limit')and not self.get_config('Vertical_Limit') == -1)
                    or (self.get_config('Horizontal_Limit') == -1 and self.get_config('Vertical_Limit') == -1)):
                    new_contours.append(contour)
        self.all_contours = new_contours
        
    def display_contours(self, target_contour= -1, highlight_contour_list = [], display = True):
        highlight_index_list = highlight_contour_list
        target_index = target_contour
        shape_mask = np.zeros_like(self.base_template_image)
        cv2.drawContours(shape_mask, self.all_contours, -1, (255, 255, 255), thickness=cv2.FILLED)

        shape_image = np.zeros_like(self.base_template_image)
        shape_image[shape_mask[:, :, 0] > 0] = self.base_template_image[shape_mask[:, :, 0] > 0]


        for highlight_index in highlight_index_list:
            
            highlight_mask = np.zeros_like(self.base_template_image)
            cv2.drawContours(highlight_mask, [self.all_contours[highlight_index]], -1, (255, 255, 255), thickness=cv2.FILLED)
            
            shape_image[highlight_mask[:, :, 0] > 0] = [255,255,0]
        
        if target_index != -1:
            highlight_mask = np.zeros_like(self.base_template_image)
            contour = self.all_contours[target_index]
            cv2.drawContours(highlight_mask, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
            shape_image[highlight_mask[:, :, 0] > 0] = [255,0,0]
            
            center_x = int(np.mean(contour[:, 0, 0]))
            center_y = int(np.mean(contour[:, 0, 1]))
            cv2.circle(shape_image, (center_x, center_y), 30, (0, 255, 0), 1)

        self.processed_template_image = shape_image if display else self.base_template_image
    
    def load_template(self, template_folder_name = None, template_data = None):
        
        self.template_folder_name = template_folder_name if template_folder_name is not None else template_data['folder_name']
        self.template_data = template_data if template_data is not None else self.config_sheet.data[template_folder_name] 
        
        self.load_base_template_image()
        self.processed_template_image = self.base_template_image
        self.generate_contours()

    
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