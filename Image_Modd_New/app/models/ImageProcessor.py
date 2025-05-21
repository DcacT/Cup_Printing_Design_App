import os
import cv2
import numpy as np
from PIL import Image,ImageTk
from scipy.optimize import leastsq
import logging
class ImageProcessor:
    def __init__(self, template_manager):
        self.template_name = ""
        self.template = {}
        self.template_manager = template_manager
        
        self.base_template_image = None
        self.processed_template_image = None
        
        self.all_contours = []
        
        
        self.resize_ratio = 0.5
        pass
    
    def get_config(self, key):
        return float(self.template[key])
    
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
    
    def load_template(self, template_name = None, template = None):

        self.template_name = template_name if template_name is not None else template['folder_name']
        self.template = template if template is not None else self.template_manager.templates[template_name] 
        logging.debug(f'template: {self.template}')
        self.load_base_template_image()
        self.processed_template_image = self.base_template_image
        self.generate_contours()

    
    def load_base_template_image(self):
        self_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(self_path, f'../../data/templates/template_{self.template_name}.png', )
        self.base_template_image = cv2.imread(path, cv2.IMREAD_COLOR)

    def get_display_image(self):
        h, w = self.processed_template_image.shape[:2]
        img_rgb = cv2.cvtColor(self.processed_template_image, cv2.COLOR_BGR2RGB)
        img_resize = cv2.resize(img_rgb, (int(w*self.resize_ratio), int(h*self.resize_ratio)) )
        img_pil = Image.fromarray(img_resize)
        img_tk = ImageTk.PhotoImage(img_pil)
        return img_tk
    
        
    def generate_border(self, action, selected_contour_idx_list = []):
        location = action.split(' ')[0] 
        print(location)
        
        if location == 'Left' or location == 'Right':
            result = self.calculate_straight(selected_contour_idx_list)
        elif location == 'Top' or location == 'Bottom':
            result = self.calculate_arc(selected_contour_idx_list)
        return result
    
    
    def calculate_straight(self, selected_contour_index_list = []):
        straight_contours = [self.all_contours[idx] for idx in selected_contour_index_list]
        best_fit_straight_lines = []

        for contour in straight_contours:
                    [vx, vy, x0, y0] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
                    best_fit_straight_lines.append((float(vx), float(vy), float(x0), float(y0)))        
        data_array = np.array(best_fit_straight_lines)  # get ag
        
        (avg_vx, avg_vy, avg_x0, avg_y0) = np.mean(data_array, axis=0)
        print('avg_line1 stats: ', avg_vx, avg_vy, avg_x0, avg_y0)
        return (avg_vx, avg_vy, avg_x0, avg_y0)
    
    
    def calculate_arc(self, elected_contour_index_list = []):
        arc_contours = [self.all_contours[idx] for idx in elected_contour_index_list]

        x = []
        y = []
        for contour in arc_contours:
            for point in contour:
                x.append(point[0].tolist()[0])
                y.append(point[0].tolist()[1])
        x_m = np.mean(x)
        y_m = np.mean(y)

        def calc_R(xc, yc):
            return np.sqrt((x - xc) ** 2 + (y - yc) ** 2)

        def f(c):
            """Calculate the algebraic distance between the fitted circle and the data points."""
            Ri = calc_R(*c)
            return Ri - Ri.mean()
        
        # Solve for the best-fitting center
        center_estimate = x_m, y_m
        center, _ = leastsq(f, center_estimate)

        # Compute final radius
        Ri = calc_R(*center)
        radius = Ri.mean()

        #round
        center_x = int(round(center[0]))
        center_y = int(round(center[1]))
        radius = int(round(radius))
        print(center_x, center_y, radius)
        
        return (center_x, center_y, radius)
    


    def display_border(self, display = False):
        if display:
            #potential bug where value is actually -1.0
            display_arc1 = '-1' not in [self.template['Arc_1_x'], self.template['Arc_1_y'], self.template['Arc_1_r']]
            display_arc2 = '-1' not in [self.template['Arc_2_x'], self.template['Arc_2_y'], self.template['Arc_2_r']]
            display_line1 = '-1' not in [self.template['Line_1_vx'], self.template['Line_1_vy'], self.template['Line_1_x0'], self.template['Line_1_y0']]
            display_line2 = '-1' not in [self.template['Line_2_vx'], self.template['Line_2_vy'], self.template['Line_2_x0'], self.template['Line_2_y0'], ]
            self.apply_arc(display_arc1, display_arc2)
            self.apply_straight(display_line1, display_line2)

    def apply_arc(self, display_arc1 = False, display_arc2 = False):
        img = self.processed_template_image        
        
        if display_arc1:
            x = self.template['Arc_1_x']
            y = self.template['Arc_1_y']
            r = self.template['Arc_1_r']
            
            cv2.circle(img, (int(x), int(y)), int(r) ,(0, 0, 255), 2)
        
        if display_arc2:
            x = self.template['Arc_2_x']
            y = self.template['Arc_2_y']
            r = self.template['Arc_2_r']
            cv2.circle(img, (int(x), int(y)), int(r) ,(0, 0, 255), 2)
        
        self.processed_template_image = img

    def apply_straight(self,display_line1 = False, display_line2 = False):
        img = self.processed_template_image        

        height, width = img.shape[:2]
        line_length = max(width, height)  # Extend long enough

        if display_line1:
            x0 = float(self.template['Line_1_x0'])
            y0 = float(self.template['Line_1_y0'])
            vx = float(self.template['Line_1_vx'])
            vy = float(self.template['Line_1_vy'])
            x1, y1 = int(x0 - vx * line_length), int(y0 - vy * line_length)
            x2, y2 = int(x0 + vx * line_length), int(y0 + vy * line_length)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)        

        if display_line2:
            x0 = float(self.template['Line_2_x0'])
            y0 = float(self.template['Line_2_y0'])
            vx = float(self.template['Line_2_vx'])
            vy = float(self.template['Line_2_vy'])
            x1, y1 = int(x0 - vx * line_length), int(y0 - vy * line_length)
            x2, y2 = int(x0 + vx * line_length), int(y0 + vy * line_length)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  
        
        self.processed_template_image = img
