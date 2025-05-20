from ..sql.sql_helper import sql
import os 
# from PIL import Image
# import re

self_path = os.path.dirname(os.path.realpath(__file__))

projects_folder_path = os.path.join(self_path, '../../data/projects')

class ProjectManager:
    def __init__(self):
        self.projects = {}
        self.templates = {}
        self.refresh()

    def refresh(self):
        self.projects = os.listdir(projects_folder_path)
        
    def get_project_path(self, project_name):
        os.path.join(projects_folder_path, project_name)

    def new_project(self, project_name, template_name):
        
        project_path = self.get_project_path(project_name)
        os.makedirs(project_path)
        
        db_path = os.path.join(projects_folder_path, project_name)
        with open(db_path, 'w') as db:
            pass
        
        msg = 'create_db'
        sql()
    
    def update_project(self, project_params):
        pass
    def new_img(self, project_name, image_path):
        pass
    def delete_project(self, project_name):
        pass

t = ProjectManager()
