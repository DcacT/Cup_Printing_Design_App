from ..sql.sql_helper import sql
from tkinter import messagebox
import os 
import re
import shutil 
import cv2
from .project import Project
self_path = os.path.dirname(os.path.realpath(__file__))

projects_folder_path = os.path.join(self_path, '../../data/projects')

class Project_Manager:
    def __init__(self):
        self.project_list = []
        self.project = Project()
        self.refresh()
        pass
    
    def refresh(self):
        self.project_list = os.listdir(projects_folder_path)

    def create_Project(self, project_name, template_name):
        if self.verify(project_name):
            self.project.create_project(project_name, template_name)
            self.refresh()
        else:
            messagebox.showerror('ERROR', 'invalid project name')
    
    def delete_project(self, project_name):
        self.project.delete_project(project_name)
    
    def verify(self, project_name):
        banned_words = ['Project_Name', '']    
        if project_name in banned_words:
            return False
        if not is_valid_windows_directory_name(project_name):
            return False
        if project_name in self.project_list:
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

