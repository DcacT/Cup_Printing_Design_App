from ..sql.sql_helper import sql
import os 
import re

self_path = os.path.dirname(os.path.realpath(__file__))

projects_folder_path = os.path.join(self_path, '../../data/projects')

class ProjectManager:
    def __init__(self):
        self.project_list = []
        self.projects = {}
        self.templates = {}
        self.refresh()

    def refresh(self):
        self.projects = os.listdir(projects_folder_path)
        
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
        Image_Name TEXT PRIMARY KEY,
        x_Percent FLOAT,
        y_Percent FLOAT,
        Rotation FLOAT,
        Scale FLOAT,
        Order_Index FLOAT
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
    

    def update_project(self, project_params):
        pass
    def new_img(self, project_name, image_path):
        pass
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

