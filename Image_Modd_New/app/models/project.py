from ..sql.sql_helper import sql
import os 
import re
import shutil 
import cv2
from functools import partial
from tkinter import StringVar, IntVar, TclError, messagebox
import numpy as np
import math 

self_path = os.path.dirname(os.path.realpath(__file__))
projects_folder_path = os.path.join(self_path, '../../data/projects')
resize_ratio = 0.1

class Project:
    def __init__(self, project_name = None):
        self.project_name = None
        self.project_data = {}
        self.template_data = {}
        self.template_grid_data = {}
        
    def load_project(self, project_name):
        self.project_name = project_name
        self.project_path = self.get_project_path(self.project_name)
        self.db_path = self.get_project_db_path(self.project_name)
        self.display_image = None
        self.read_project()  

            
    def create_project(self, project_name, template_name):
        
        if verify(project_name):
            self.project_name = project_name
            self.project_path = self.get_project_path(self.project_name)
            self.db_path = self.get_project_db_path(self.project_name)
            
            os.makedirs(self.project_path)
            msg = f'''
            CREATE TABLE project (
                Image_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Image_Name TEXT,
                Image_Path TEXT,
                Order_Index INTEGER DEFAULT -1,
                x_Percent FLOAT DEFAULT 50,
                y_Percent FLOAT DEFAULT 50,
                Rotation FLOAT DEFAULT 0,
                Scale FLOAT DEFAULT 50
            );
            CREATE TABLE settings (
                Project_Name TEXT PRIMARY KEY,
                Template_Name TEXT
            );
            INSERT INTO settings (Project_Name, Template_Name)
            VALUES ('{project_name}', '{template_name}');
            '''
            sql(msg, db_path = self.db_path)
            return True
        else: 
            messagebox.showerror('ERROR', 'invalid project name')
            return False
        
    def read_project(self):
        self.project_data = {}
        self.template_data = {}
        self.template_grid_data = {}
        
        msg = 'SELECT template_name FROM settings'
        template_name = sql(msg, db_path = self.db_path)[0][0]
        template_image = read_image(os.path.join(self.project_path, f'../../templates/template_{template_name}.png'))
        
        msg = f'SELECT * FROM templates WHERE template_name = "{template_name}"'
        template_data = sql(msg)
        template_data = list(template_data[0])
        self.template_data = {
            'template_image': template_image,
            'template_name': template_data[0],
            'PX_min': template_data[1],
            'PX_max': template_data[2],
            'Horizontal_Limit': template_data[3],
            'Vertical_Limit': template_data[4],
            'Line_1_vx': template_data[5],
            'Line_1_vy': template_data[6],
            'Line_1_x0': template_data[7],
            'Line_1_y0': template_data[8],
            'Line_2_vx': template_data[9],
            'Line_2_vy': template_data[10],
            'Line_2_x0': template_data[11],
            'Line_2_y0': template_data[12],
            'Arc_1_x': template_data[13],
            'Arc_1_y': template_data[14],
            'Arc_1_r': template_data[15],
            'Arc_2_x': template_data[16],
            'Arc_2_y': template_data[17],
            'Arc_2_r': template_data[18],
            'template_image_center': get_image_center(template_image)
        }
        self.calc_template_grid_data()
        msg = f'SELECT * FROM project'
        
        project_data = sql(msg, db_path = self.db_path)
        
        for row in project_data:
            img = self.read_project_image(row[2])
            self.project_data[row[0]] = {
                'Image_ID': IntVar(value=row[0]),
                'Image_Name': StringVar(value=row[1]),
                'Image_Path': StringVar(value=row[2]),
                'Order_Index': IntVar(value=row[3]),
                'x_Percent': IntVar(value=row[4]),
                'y_Percent': IntVar(value=row[5]),
                'Rotation': IntVar(value=row[6]),
                'Scale': IntVar(value=row[7]),
                'Image':img,
                'Image_Center': get_image_center(img)
            }
            self.project_data[row[0]]['x_Percent'].trace_add("write", partial(self.validate_range_input, self.project_data[row[0]]['x_Percent']))
            self.project_data[row[0]]['y_Percent'].trace_add("write", partial(self.validate_range_input, self.project_data[row[0]]['y_Percent']))
            self.project_data[row[0]]['Rotation'].trace_add("write", partial(self.validate_range_input, self.project_data[row[0]]['Rotation']))
            self.project_data[row[0]]['Scale'].trace_add("write", partial(self.validate_range_input, self.project_data[row[0]]['Scale']))
        
        pass
    
    def read_project_image(self, path):
        return read_image(os.path.join(self.project_path, f'{path}.png'))

            
    def update_project(self):
        
        msg = ''
        for Image_ID, data in self.project_data.items():
            n_msg = f"""
                UPDATE project
                SET
                    Image_Name = '{data['Image_Name'].get()}',
                    Order_Index = '{data['Order_Index'].get()}',
                    x_Percent = '{data['x_Percent'].get()}',
                    y_Percent = '{data['y_Percent'].get()}',
                    Rotation = '{data['Rotation'].get()}',
                    Scale = '{data['Scale'].get()}'
                WHERE Image_ID = {Image_ID};
            """
            msg += n_msg
        t = sql(msg, db_path = self.db_path)
        self.read_project()
        pass
    
    def delete_project(self):
        if messagebox.askokcancel('DELETE PROJECT', f'Are you sure to delete project \n {self.project_name}'):
            for filename in os.listdir(self.project_path):
                file_path = os.path.join(self.project_path, filename)
                try:
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    else:
                        os.remove(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
            os.rmdir(self.project_path)
            

            self.project_name = None
            self.project_data = {}
            self.template_data = {}
            
            self.project_path = ''
            self.db_path = ''
        pass
    
    def add_image(self, image_path):
        msg = """
            SELECT COUNT(*) FROM project
        """
        idx = sql(msg, db_path = self.db_path)[0][0] + 1  
        msg = f"""
            INSERT INTO project (
                Image_Name, Image_Path, Order_Index, x_Percent, y_Percent, Rotation, Scale 
            )
            VALUES (
                'DEFAULT_IMAGE_NAME',
                'image_{idx}',
                -1, 50, 50, 0, 50
            );
        """
        sql(msg, db_path = self.db_path)
        new_image_path = os.path.join(self.project_path, f'image_{idx}.png')
        shutil.copy2 (image_path, new_image_path)
        self.read_project()  

        pass
    
    def delete_image(self, image_id):
        #delete sql
        msg = f'DELETE FROM project WHERE Image_ID = {image_id};'
        sql(msg, self.db_path)

        #delete file
        path = self.project_data[image_id]['Image_Path'].get()
        os.remove(os.path.join(self.project_path, f'{path}.png'))
        
        self.read_project()  

        #update_project
        
        
    def get_display_image(self, selected_image_id = None):
        #order_idx
        #for loop
        #get position
        #perform transformation
        
        #layer atop
        #resize
        
        template_image = self.template_data['template_image']
        display_image = template_image
        
        stacking_id = [[id, data['Order_Index'].get()] for id, data in self.project_data.items() if data['Order_Index'].get() != -1]
        sorted_stacking_id = sorted(stacking_id, key=lambda row: row[1])
        
        stack_image = template_image
        
        for id, _ in sorted_stacking_id:
            new_img = self.project_data[id]['Image']
            self.stack_image(stack_image, new_img)
            
        stack_image = self.draw_reference_line(stack_image, selected_image_id)
        
        return stack_image
        
    def stack_image(self, base_image, top_image):
        # diff_x = top_image_center[0] - base_image_center[0]
        # diff_y = top_image_center[1] - base_image_center[1]
        h, w = top_image.shape[:2]        

        top_image_resize = cv2.resize(top_image, (int(w*resize_ratio), int(h*resize_ratio)) )
        
        top_image_height, top_image_width = top_image_resize.shape[:2]
        
        rgb = top_image_resize[:, :, :3].astype(np.uint16)
        alpha = top_image_resize[:, :, 3].astype(np.uint16)
        
        x = 0
        y = 0
        roi = base_image[y:y+top_image_height, x:x+top_image_width].astype(np.uint16)
        
        for channel in range(3): #rbg
            roi[:,:,channel] = (rgb[:, :, channel] * alpha + roi[:, :, channel] * (255 - alpha)) // 255
            
        base_image[y:y+top_image_height, x:x+top_image_width] = roi.astype(np.uint8)
        # base_image[0:top_image_height, 0:top_image_width] = top_image_resize

        return base_image
    
    def draw_reference_line(self, base_image, image_id):
            
        if self.check_tempalte_complete:
            #draw template_arcs
            reference_line_color = (127, 255, 0)
            cv2.circle(base_image, 
                        (int(self.template_data['Arc_1_x']), int(self.template_data['Arc_1_y'])), 
                        int(self.template_data['Arc_1_r']), reference_line_color, 2)
            
            cv2.circle(base_image, 
                        (int(self.template_data['Arc_2_x']), int(self.template_data['Arc_2_y'])), 
                        int(self.template_data['Arc_2_r']) ,reference_line_color, 2)

            #draw template_sides
            height, width = base_image.shape[:2]
            line_length = max(width, height)
            x0 = float(self.template_data['Line_1_x0'])
            y0 = float(self.template_data['Line_1_y0'])
            vx = float(self.template_data['Line_1_vx'])
            vy = float(self.template_data['Line_1_vy'])
            
            line_x1, line_y1 = int(x0 - vx * line_length), int(y0 - vy * line_length)
            line_x2, line_y2 = int(x0 + vx * line_length), int(y0 + vy * line_length)
            
            cv2.line(base_image, (line_x1, line_y1), (line_x2, line_y2), reference_line_color, 2)  
        
            x0 = float(self.template_data['Line_2_x0'])
            y0 = float(self.template_data['Line_2_y0'])
            vx = float(self.template_data['Line_2_vx'])
            vy = float(self.template_data['Line_2_vy'])
            line_x1, line_y1 = int(x0 - vx * line_length), int(y0 - vy * line_length)
            line_x2, line_y2 = int(x0 + vx * line_length), int(y0 + vy * line_length)
            cv2.line(base_image, (line_x1, line_y1), (line_x2, line_y2), reference_line_color, 2) 
             
            if image_id is not -1:
                #draw_image_percent_line
                
                cross_line_color = (255, 20, 147)                
                x_percent = self.project_data[image_id]['x_Percent'].get()
                line_x1 = self.template_grid_data['line_x1']
                line_y1 = self.template_grid_data['line_y1']
                
                diff = self.template_grid_data['diff']
                angle_base = self.template_grid_data['angle_base']
                angle_delta = angle_base + diff * (x_percent/100)

                line_length = line_y1
                line_x2 = int(line_x1 - line_length * math.cos(angle_delta))
                line_y2 = int(line_y1 + line_length * math.sin(angle_delta))  
                
                
                print('x: ', x_percent)
                print("angle (degrees):", math.degrees(angle_delta))
                angle1 = math.atan2(float(self.template_data['Line_1_vx']), float(self.template_data['Line_1_vy']))
                angle2 = math.atan2(float(self.template_data['Line_2_vx']), float(self.template_data['Line_2_vy']))
                
                print("angle1 (degrees):", math.degrees(angle1))
                print("angle2 (degrees):", math.degrees(angle2))
                print('line_x1: ', line_x1)
                print('line_y1: ', line_y1)
                print('line_x2: ', line_x2)
                print('line_y2: ', line_y2)
                print('shape_of_img: ', base_image.shape[:2])

                cv2.line(base_image, (int(line_x1), int(line_y1)), (int(line_x2), int(line_y2)), cross_line_color, 2) 

                #y_percent
                r = int(self.template_data['Arc_2_r']) + ((int(self.template_data['Arc_1_r']) - int(self.template_data['Arc_2_r'])) *( self.project_data[image_id]['y_Percent'].get()/100))
                cv2.circle(base_image, 
                           (self.template_grid_data['arc_x']//2, self.template_grid_data['arc_y']//2), 
                           int(r),
                           cross_line_color, 2)
            
        
        return base_image
    
    def translate_percent_to_coord(self, image_id):
        x_percent = self.project_data[image_id]['x_Percent'].get()
        line_x1 = self.template_grid_data['line_x1']
        line_y1 = self.template_grid_data['line_y1']
        
        diff = self.template_grid_data['diff']
        angle_base = self.template_grid_data['angle_base']
        angle_delta = angle_base + diff * (x_percent/100)

        line_x2 = int(line_x1 + line_y1 * math.cos(angle_delta))
        line_y2 = int(line_y1 - line_y1 * math.sin(angle_delta)) 
        
        arc_x = self.template_grid_data['arc_x']
        arc_y = self.template_grid_data['arc_y']
        arc_r = int(self.template_data['Arc_2_r']) + ((int(self.template_data['Arc_1_r']) - int(self.template_data['Arc_2_r'])) *( self.project_data[image_id]['y_Percent'].get()/100))

        dx = line_x2 - line_x1
        dy = line_y2 - line_y1

        a = dx**2 + dy**2
        b = 2 * (line_x1 * dx + line_y1 * dy)
        c = line_x1**2 + line_y1**2 - arc_r**2

        # Guaranteed: discriminant > 0
        discriminant = b**2 - 4 * a * c
        sqrt_disc = np.sqrt(discriminant)

        t1 = (-b + sqrt_disc) / (2 * a)
        t2 = (-b - sqrt_disc) / (2 * a)

        # Convert back to original coordinates
        ix1 = line_x1 + t1 * dx + arc_x
        iy1 = line_y1 + t1 * dy + arc_y
        ix2 = line_x1 + t2 * dx + arc_x
        iy2 = line_y1 + t2 * dy + arc_y

        
        return (ix1, iy1) if iy1 >= iy2 else (ix2, iy2)
        
        
    def calc_template_grid_data(self):
        
        line_x1 = (self.template_data['Arc_1_x'] + self.template_data['Arc_2_x'])//2
        line_y1 = (self.template_data['Arc_1_y'] + self.template_data['Arc_2_y'])//2

        angle1 = math.atan2(float(self.template_data['Line_1_vx']), float(self.template_data['Line_1_vy']))
        angle2 = math.atan2(float(self.template_data['Line_2_vx']), float(self.template_data['Line_2_vy']))
        diff = (angle1 - angle2 + math.pi) % (2 * math.pi) - math.pi
        
        arc_x = int(self.template_data['Arc_1_x']) + int(self.template_data['Arc_2_x']) 
        arc_y = int(self.template_data['Arc_2_y']) + int(self.template_data['Arc_2_y'])
        
        self.template_grid_data = {
            'line_x1': line_x1,
            'line_y1': line_y1,
            'angle_base': angle2,
            'diff': diff,
            'arc_x': arc_x,
            'arc_y': arc_y,
        }
        
        pass


    
    def update_order_idx(self, image_id, direction_up):
    

        current_idx = self.project_data[image_id]['Order_Index'].get()  
        ###
        #  direction up
        #  condition 2(append) : order_index == -1 -> order_index is now 0, and everything in showlist goes one up. 
        #  condition 1(invalid): order_index == (len_of_show_list-1) -> invalid input, nothing happens
        #  condition 3(replace): order_index != -1 and smaller than len_of_show_list-> exchange order_index between image_id and image_id with order_index+1
        # 
        # direction down
        # condition_1(invalid): order_index == -1 -> nothing happens, cannot go lower
        # condition 2(pop)    : order_index == 0 -> order_index = -1, everything in showlist goes 1 lower
        # condition 3(replace): order_index above 0 and not -1 -> exchange order_index between image_id and image_id with order_index-1
        # 
        # ###
        if direction_up:
            len_of_proj_data = len([1 for v in self.project_data.values()])
            len_of_no_show_list = len([1 for v in self.project_data.values() if v['Order_Index'].get() == -1])
            len_of_show_list = len_of_proj_data - len_of_no_show_list


            if current_idx >= (len_of_show_list - 1) and current_idx != -1:
                pass
            
            elif current_idx == -1:

                self.project_data[image_id]['Order_Index'].set(0)
                
                for key, val in self.project_data.items():
                    idx = self.project_data[key]['Order_Index'].get()
                    if key != image_id and idx !=-1:
                        self.project_data[key]['Order_Index'].set(idx+1)
                        
            else:

                target_id= next((k for k, v in self.project_data.items() if v['Order_Index'].get() == current_idx + 1), None)
                self.project_data[target_id]['Order_Index'].set(current_idx)
                self.project_data[image_id]['Order_Index'].set(current_idx + 1)

        else: # !direction_dn
            
            if current_idx == -1:
                pass
            
            elif current_idx == 0:
                self.project_data[image_id]['Order_Index'].set(-1)
                
                for key, val in self.project_data.items():
                    idx = self.project_data[key]['Order_Index'].get()
                    if key != image_id and idx !=-1:
                        t = self.project_data[key]['Order_Index'].get()
                        self.project_data[key]['Order_Index'].set(t-1)
                        
            else:

                target_id= next((k for k, v in self.project_data.items() if v['Order_Index'].get() == current_idx - 1), None)
                self.project_data[target_id]['Order_Index'].set(current_idx)
                self.project_data[image_id]['Order_Index'].set(current_idx - 1)
                

        return

### UTIL
    def get_project_path(self, project_name):
        return os.path.join(projects_folder_path, project_name)
        
    def get_project_db_path(self, project_name):        
        return os.path.join(self.get_project_path(project_name), f'{project_name}.db')

    def validate_range_input(self, check_var,*args):
        
        try:
            value = check_var.get()
            if isinstance(value, int) or value == '-' or value == '':
                if not (-1 <= value <= 100):
                    check_var.set(100 if value > 100 else -1)
            else: 
                check_var.set('-1')
        except TclError:
            pass  # In case of non-integer input  
        
    def check_tempalte_complete(self):
        return False if -1 in [
            self.template_data['Line_1_vx'],
            self.template_data['Line_1_vy'],
            self.template_data['Line_1_x0'],
            self.template_data['Line_1_y0'],
            
            self.template_data['Line_2_vx'],
            self.template_data['Line_2_vy'],
            self.template_data['Line_2_x0'],
            self.template_data['Line_2_y0'],
            
            self.template_data['Arc_1_x'],
            self.template_data['Arc_1_y'],
            self.template_data['Arc_1_r'],
            
            self.template_data['Arc_2_x'],
            self.template_data['Arc_2_y'],
            self.template_data['Arc_2_r'],
        ] else True
        
def verify(project_name):
    banned_words = ['Project_Name', '']    
    if project_name in banned_words:
        return False
    if not is_valid_windows_directory_name(project_name):
        return False
    project_list = os.listdir(projects_folder_path)
    if project_name in project_list:
        return False
    return True

def is_valid_windows_directory_name(name: str) -> bool:
    if not name or len(name) > 255:
        return False

    # Check for invalid characters
    if re.search(r'[<>:"/\\|?*]', name):
        return False

    # Reserved names (case-insensitive)
    reserved = {
        "CON", "PRN", "AUX", "NUL",
        *["COM" + str(i) for i in range(1, 10)],
        *["LPT" + str(i) for i in range(1, 10)]
    }
    name_upper = name.upper().split('.')[0]  # Remove extension if any
    if name_upper in reserved:
        return False

    # No trailing space or period
    if name[-1] in {' ', '.'}:
        return False

    return True

def read_image(path):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if image.shape[2] == 3:
        alpha = np.ones(image.shape[:2], dtype=image.dtype) * 255  # Fully opaque
        image_with_alpha = cv2.merge((*cv2.split(image), alpha))
    else:
        image_with_alpha = image
        
    return image_with_alpha

def get_image_center(img):
    height, width = img.shape[:2]
    center_x = width // 2
    center_y = height // 2
    return (center_x, center_y)