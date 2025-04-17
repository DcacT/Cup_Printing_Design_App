import cv2
import numpy as np
import csv
import os
import random
import math
from scipy.optimize import leastsq
from PIL import Image, ImageTk
from tkinter import StringVar
default_tempalte_configuration = {
    'folder_name':'',
    'PX_Min':-1, #Pixel Count 
    'PX_Max':-1, 
    'Horizontal_Limit':-1, #Aspect Ratio
    'Vertical_Limit':-1,
    
    'Line_1_vx':-1,  #line1
    'Line_1_vy':-1,
    'Line_1_x0':-1,
    'Line_1_y0':-1,

    'Line_2_vx':-1, #line2
    'Line_2_vy':-1,
    'Line_2_x0':-1,
    'Line_2_y0':-1,
    
    'Arc_1_x':-1, #arc1
    'Arc_1_y':-1,
    'Arc_1_r':-1,
    
    'Arc_2_x':-1, #arc2
    'Arc_2_y':-1,
    'Arc_2_r':-1,                
}
image_state={
    'Display_Contour':False,
    'Display_Line1':False,
    'Display_Line2':False,
    'Display_Arc1':False,
    'Display_Arc2':False,
}

class TemplateImageProcessor:
    def __init__(self, template_configuration):
        self.image_state = image_state
        if type(template_configuration['folder_name']) == StringVar: 
            self.template_configuration = {k:v.get() for k, v in template_configuration.items()}
        else:
            self.template_configuration = template_configuration
        self.base_img = self.load_base_image() 
        self.selected_contour_index_list = []
        self.selected_contour = -1
        self.all_contours = []

    def load_template(self, template_configuration):
        if type(template_configuration['folder_name']) == StringVar: 
            self.template_configuration = {k:v.get() for k, v in template_configuration.items()}
        else:
            self.template_configuration = template_configuration
        self.base_img = self.load_base_image() 
        
        self.selected_contour_index_list = []
        self.selected_contour = -1
        self.all_contours = []

    def load_base_image(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        if self.template_configuration['folder_name'] != '':
            template_img_path = os.path.join(dir_path, '../../Templates', self.template_configuration['folder_name'], 'template_image.png')
        else:
            template_img_path = os.path.join(dir_path, './filler_image.png')

        self.base_img = cv2.imread(template_img_path, cv2.IMREAD_COLOR)

        return self.base_img
    
    def convert_cv2_to_tk(self, img_cv2 = None, default = True):
        h, w = self.base_img.shape[:2]
        
        img_rgb = cv2.cvtColor(
            self.get_dispay_image() if default else img_cv2, cv2.COLOR_BGR2RGB)
        
        img_resize = cv2.resize(img_rgb, (int(w*0.5), int(h*0.5)) )

        img_pil = Image.fromarray(img_resize)
        img_tk = ImageTk.PhotoImage(img_pil)
        return img_tk

    def generate_contour(self):

        gray = cv2.cvtColor(self.base_img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)    
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.all_contours = contours
        return contours
    
    def get_config(self, key):
        return int(self.template_configuration[key])
    
    def filter_contour(self):
        new_contours = []
        for contour in self.all_contours:
            if (len(contour) > self.get_config('PX_Min') 
            and len(contour) < self.get_config('PX_Max')):
                
                x, y, w, h = cv2.boundingRect(contour)  # Get bounding box (x, y, width, height)
                aspect_ratio = w / h  # Width divided by height

                if ((aspect_ratio < self.get_config('Horizontal_Limit') and not self.get_config('Horizontal_Limit') == -1)
                    or (aspect_ratio > self.get_config('Vertical_Limit')and not self.get_config('Vertical_Limit') == -1)
                    or (self.get_config('Horizontal_Limit') == -1 and self.get_config('Vertical_Limit') == -1)):
                    new_contours.append(contour)
        print(len(new_contours))
        self.all_contours = new_contours
        return new_contours
    
    def get_contouor_image(self):
        highlight_index_list = self.selected_contour_index_list
        target_index = self.selected_contour
        shape_mask = np.zeros_like(self.base_img)
        cv2.drawContours(shape_mask, self.all_contours, -1, (255, 255, 255), thickness=cv2.FILLED)

        shape_image = np.zeros_like(self.base_img)
        shape_image[shape_mask[:, :, 0] > 0] = self.base_img[shape_mask[:, :, 0] > 0]


        for highlight_index in highlight_index_list:
            
            highlight_mask = np.zeros_like(self.base_img)
            cv2.drawContours(highlight_mask, [self.all_contours[highlight_index]], -1, (255, 255, 255), thickness=cv2.FILLED)
            
            shape_image[highlight_mask[:, :, 0] > 0] = [255,255,0]
        
        if target_index != -1:
            highlight_mask = np.zeros_like(self.base_img)
            contour = self.all_contours[target_index]
            cv2.drawContours(highlight_mask, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
            shape_image[highlight_mask[:, :, 0] > 0] = [255,0,0]
            
            center_x = int(np.mean(contour[:, 0, 0]))
            center_y = int(np.mean(contour[:, 0, 1]))
            cv2.circle(shape_image, (center_x, center_y), 30, (0, 255, 0), 1)

        # if True:
        #     cv2.imshow(f"Edge Detection Result {highlight_index/len(contours)}", resized_image)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()

        return shape_image

    def update_image_state(self, key=None, val=None):
        if key is not None:
            self.image_state[key] = val if val is not None else not self.image_state[key]
        return self.image_state
    
    def update_template_configuration(self, new_template_configuration):
        self.template_configuration = new_template_configuration
        return new_template_configuration
    
    def get_base_image(self):
        return self.base_img
    
    def get_dispay_image(self):

        base_img = self.base_img
        image_state = self.image_state
        print('img_processor_config: ', self.template_configuration)
        if image_state['Display_Contour']:
            # self.selected_contour_index_list = []
            self.generate_contour()
            self.filter_contour()
            new_img = self.get_contouor_image()

        else:
            new_img = self.base_img
        
            new_img = self.apply_arc(img = new_img)
            new_img = self.apply_straight(img = new_img)

        return new_img
    
    def calculate_arc1(self):
        arc_contours = [self.all_contours[idx] for idx in self.selected_contour_index_list]

        x = []
        y = []
        for contour in arc_contours:
            for point in contour:
                x.append(point[0].tolist()[0])
                y.append(point[0].tolist()[1])
        x_m = np.mean(x)
        y_m = np.mean(y)

        def calc_R(xc, yc):
            """Calculate distances from all points to the center (xc, yc)."""
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
    

    def calculate_straight(self):
        straight_contours = [self.all_contours[idx] for idx in self.selected_contour_index_list]
        best_fit_straight_lines = []

        for contour in straight_contours:
                    [vx, vy, x0, y0] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
                    best_fit_straight_lines.append((float(vx), float(vy), float(x0), float(y0)))        
        print('best_fit_straight_lines: ',best_fit_straight_lines)
        data_array = np.array(best_fit_straight_lines)  # get ag
        (avg_vx, avg_vy, avg_x0, avg_y0) = np.mean(data_array, axis=0)
        print('avg_line1 stats: ', avg_vx, avg_vy, avg_x0, avg_y0)
        return (avg_vx, avg_vy, avg_x0, avg_y0)

    def apply_arc(self, img =None):
        if img is None: 
            img = self.base_img        
        
        if image_state['Display_Arc1']:
            x = self.template_configuration['Arc_1_x']
            y = self.template_configuration['Arc_1_y']
            r = self.template_configuration['Arc_1_r']
            
            cv2.circle(img, (x, y), r ,(0, 0, 255), 2)
        
        if image_state['Display_Arc2']:
            x = self.template_configuration['Arc_2_x']
            y = self.template_configuration['Arc_2_y']
            r = self.template_configuration['Arc_2_r']
            cv2.circle(img, (x, y), r ,(0, 0, 255), 2)
        
        return img

    def apply_straight(self, img = None):
        if img is None: 
            img = self.base_img        

        height, width = img.shape[:2]
        line_length = max(width, height)  # Extend long enough

        if image_state['Display_Line1']:
            x0 = self.template_configuration['Line_1_x0']
            y0 = self.template_configuration['Line_1_y0']
            vx = self.template_configuration['Line_1_vx']
            vy = self.template_configuration['Line_1_vy']
            if 0 not in [int(x0), int(y0), int(vx), int(vy)]:
                x1, y1 = int(x0 - vx * line_length), int(y0 - vy * line_length)
                x2, y2 = int(x0 + vx * line_length), int(y0 + vy * line_length)
                cv2.line(self.image, (x1, y1), (x2, y2), (0, 255, 0), 2)        

        if image_state['Display_Line2']:
            x0 = self.template_configuration['Line_2_x0']
            y0 = self.template_configuration['Line_2_y0']
            vx = self.template_configuration['Line_2_vx']
            vy = self.template_configuration['Line_2_vy']
            if 0 not in [int(x0), int(y0), int(vx), int(vy)]:
                x1, y1 = int(x0 - vx * line_length), int(y0 - vy * line_length)
                x2, y2 = int(x0 + vx * line_length), int(y0 + vy * line_length)
                cv2.line(self.image, (x1, y1), (x2, y2), (0, 255, 0), 2)  
        
        return img