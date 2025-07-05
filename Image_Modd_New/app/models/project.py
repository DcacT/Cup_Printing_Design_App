from ..sql.sql_helper import sql
import os 
import re
import shutil 
import cv2
from tkinter import StringVar, IntVar
self_path = os.path.dirname(os.path.realpath(__file__))

projects_folder_path = os.path.join(self_path, '../../data/projects')


class Project:
    def __init__(self, project_name):
        self.project_name = None
        self.project_data = {}
        self.template_data = {}
        
        self.project_path = self.get_project_path(project_name)
        self.db_path = self.get_project_db_path(project_name)
        
        self.refresh()            
        
        
    # def refresh(self):
    #     if self.project_name != None:

    def create_project(self, project_name, template_name):

        os.makedirs(self.project_path)
        
        msg = f'''
        CREATE TABLE project (
            Image_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Image_Name TEXT,
            Image_Path TEXT,
            Show FLOAT DEFAULT 0,
            x_Percent FLOAT DEFAULT 50,
            y_Percent FLOAT DEFAULT 50,
            Rotation FLOAT DEFAULT 0,
            Scale FLOAT DEFAULT 50,
            Order_Index INTEGER
        );
        CREATE TABLE settings (
            Project_Name TEXT PRIMARY KEY,
            Template_Name TEXT
        );
        INSERT INTO settings (Project_Name, Template_Name)
        VALUES ('{project_name}', '{template_name}');
        '''
        sql(msg, db_path = self.db_path)
        
        
    def read_project(self):
        msg = 'SELECT template_name FROM settings'
        template_name = sql(msg, db_path = self.db_path)[0][0]
        template_image = cv2.imread(
            os.path.join(self.project_path, f'../../templates/template_{template_name}.png', ),
            cv2.IMREAD_UNCHANGED )
        
        msg = f'SELECT * FROM templates WHERE template_name = {template_name}'
        template_data = sql(msg)
        
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
            'Arc_2_r': template_data[18]
        }
        
        msg = f'SELECT * FROM project'
        project_data = sql(msg, db_path = self.db_path)
        
        for row in project_data:
            image_data = list(row)
            self.project_data[row[0]] = {
                'Image_ID': IntVar(value=row[0]),
                'Image_Name': StringVar(value=row[1]),
                'Image_Path': StringVar(value=row[2]),
                'Show': IntVar(value=row[3]),
                'x_Percent': IntVar(value=row[4]),
                'y_Percent': IntVar(value=row[5]),
                'Rotation': IntVar(value=row[6]),
                'Scale': IntVar(value=row[7]),
                'Order_Index': IntVar(value=row[8]),
            }
                    
        pass
    
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
                WHERE Image_ID = {Image_ID.get()};
            """
            msg += n_msg
        t = sql(msg, db_path = self.db_path)
        pass
    
    def delete_project(self):
        
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
    
    
### UTIL
    def get_project_path(self, project_name):
        return os.path.join(projects_folder_path, project_name)
        
    def get_project_db_path(self, project_name):
        os.path.join(self.get_project_path(project_name), f'{project_name}.db')

