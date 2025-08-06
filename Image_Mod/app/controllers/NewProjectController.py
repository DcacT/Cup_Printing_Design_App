from tkinter import filedialog, messagebox, StringVar
from os.path import isfile
import cv2
from PIL import Image, ImageTk
import re
import os 
resize_ratio = 0.5
self_path = os.path.dirname(os.path.realpath(__file__))
projects_folder_path = os.path.join(self_path, '../../data/projects')

class NewProjController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["new_project"]
        
        self.load_template_select_dropdown()
        self._bind()

    def _bind(self):
        self.frame.home_button.config(command = lambda: self.view.switch("home"))
        self.frame.new_project_button.config(command = self.on_select_new_project)

        pass
    
    def get_project_name(self):
        
        return self.frame.project_name_var.get()
    
    def load_template_select_dropdown(self):
        self.frame.template_list = self.model.template_manager.templates.keys()
        menu = self.frame.template_select_dropdown['menu']
        menu.delete(0, "end")
        print(self.frame.template_list)
        for option in self.frame.template_list:
            print(option)
            menu.add_command(label=option, command=lambda value=option: self.on_template_selected(value))
        
        self.frame.template_name_var.set('Select Template')
    
    def on_template_selected(self, template_name):
        self.frame.template_name_var.set(template_name)
        img_path = os.path.join(self.model.template_manager.template_folder_path, f'template_{template_name}.png')

        template_img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        h, w = template_img.shape[:2]
        img_rgb = cv2.cvtColor(template_img, cv2.COLOR_BGR2RGB)
        img_resize = cv2.resize(img_rgb, (int(w*resize_ratio), int(h*resize_ratio)) )
        img_pil = Image.fromarray(img_resize)
        img_tk = ImageTk.PhotoImage(img_pil)
        
        self.frame.img_label.config(image=img_tk)
        self.frame.img_label.image = img_tk
        
        
    def on_select_new_project(self):
        new_project_name = self.frame.project_name_var.get()
        template_name = self.frame.template_name_var.get()
        #verify project name.
        print(template_name)
        if template_name == 'Select Template':
            messagebox.showerror('Error', "Please Select a template first")
            return        

        if not verify(new_project_name):
            messagebox.showerror('Error', "Invalid Project Name! Try Another One")
            return        
         
        if self.model.project.create_project(new_project_name, template_name):
            messagebox.showinfo('Success', "Project Created! Head over to Project Configuration next to configure via Home please")
    
    
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


# #items
# template_select_dropdown
# project_name_entry
# new_project_button
# home_button
# img_label

