from ..sql.sql_helper import sql
import os 
import re
from shutil import copy2
self_path = os.path.dirname(os.path.realpath(__file__))

projects_folder_path = os.path.join(self_path, '../../data/projects')

class ProjectManager:
    def __init__(self):
        self.project_list = []
        self.templates = {}
        self.refresh()

    def refresh(self):
        self.project_list = os.listdir(projects_folder_path)

    def get_project_path(self, project_name):
        return os.path.join(projects_folder_path, project_name)

    def new_project(self, project_name, template_name):
        
        project_path = self.get_project_path(project_name)
        os.makedirs(project_path)
        
        db_path = os.path.join(project_path, f'{project_name}.db')
        with open(db_path, 'w') as db:
            pass
        print('db_path: ', db_path)
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
        sql(msg, db_path = db_path)
    
    def verify(self, project_name):
        banned_words = ['Project_Name', '']    
        if project_name in banned_words:
            return False
        if not is_valid_windows_directory_name(project_name):
            return False
        project_list = os.listdir(projects_folder_path)
        if project_name in project_list:
            return False
        return True
    

    def update_project(self, project_name, project_params):
        
        project_path = self.get_project_path(project_name)
        db_path = os.path.join(project_path, f'{project_name}.db')
    
        msg = f"""
            UPDATE project
            SET
                Image_Name = {project_params['Image_Name']},
                Image_Path = {project_params['Image_Path']},
                Show = {project_params['Show']},
                x_Percent = {project_params['x_Percent']},
                y_Percent = {project_params['y_Percent']},
                Rotation = {project_params['Rotation']},
                Scale = {project_params['Scale']},
                Order_Index = {project_params['Order_Index']}
            WHERE Image_ID = {project_params['Image_ID']};
            """
        sql(msg, db_path = db_path)
        pass
    
    def new_img(self, project_name, image_path):
        
        project_path = self.get_project_path(project_name)
        db_path = os.path.join(project_path, f'{project_name}.db')
        
        msg = """
            SELECT COUNT(*) FROM project
        """
        idx = sql(msg, db_path = db_path)[0][0] + 1


        msg = f"""
            INSERT INTO project (
                Image_Name, Image_Path, Show, x_Percent, y_Percent, Rotation, Scale, Order_Index
            )
            VALUES (
                'DEFAULT_IMAGE_NAME',
                'image_{idx}',
                0, 50, 50, 0, 50,-1
            );
        """
        sql(msg, db_path = db_path)
        new_image_path = os.path.join(project_path, f'image_{idx}.png')
        copy2 (image_path, new_image_path)
    
    def get_project_data(self, project_name):
        project_path = self.get_project_path(project_name)
        db_path = os.path.join(project_path, f'{project_name}.db')
        msg = f"""
            SELECT * FROM project;
            """
        data = sql(msg, db_path = db_path)
        data = [list(row) for row in data]
        data = sorted(data, key=lambda row: row[7])
        print('project_data: ',data)

        return data
        
    def delete_project(self, project_name):
        pass
    


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

