import tkinter as tk
import sys
import os
import csv
from tkinter import filedialog, messagebox, Scrollbar, Canvas, Entry,StringVar, OptionMenu, BooleanVar
from PIL import Image, ImageTk
import shutil 
from .pages import ConfigureTemplatePage

config_row_header = [
    'folder_name',
    'PX_Min', #Pixel Count 
    'PX_Max', 
    'Horizontal_Limit', #Aspect Ratio
    'Vertical_Limit',
    
    'Line_1_vx',  #line1
    'Line_1_vy',
    'Line_1_x0',
    'Line_1_y0',

    'Line_2_vx', #line2
    'Line_2_vy',
    'Line_2_x0',
    'Line_2_y0',
    
    'Arc_1_x', #arc1
    'Arc_1_y',
    'Arc_1_r',
    
    'Arc_2_x', #arc2
    'Arc_2_y',
    'Arc_2_r',                
]
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

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-View App")
        # self.attributes('-fullscreen', True)  # Fullscreen mode
        # self.configure(borderwidth=2, relief="solid")  # Bordered window

        self.frames = {}

        for F in (
            StartPage, 
            ConfigureTemplatePage, 
            NewTemplatePage, 
            SelectProjectPage, 
            NewProjectPage
            ):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        # Exit fullscreen with ESC
        self.bind("<Escape>", lambda e: self.attributes('-fullscreen', False))

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Welcome to the Start Page", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(self, text="Configure Template", command=lambda: master.show_frame(ConfigureTemplatePage)).pack()
        tk.Button(self, text="New Template", command=lambda: master.show_frame(NewTemplatePage)).pack()
        # tk.Button(self, text="Select Project", command=lambda: master.show_frame(SelectProjectPage)).pack()
        # tk.Button(self, text="New Project", command=lambda: master.show_frame(NewProjectPage)).pack()

#Tempaltes

class NewTemplatePage(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.check_and_generate_config_csv()
        tk.Label(self, text="New Template Page", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=20)
        
        self.configure(borderwidth=2, relief="solid")

        
        # File name entry
        tk.Label(self, text="New File Name:").grid(row=1, column=0, padx=10, pady=10)
        self.folder_name_entry = tk.Entry(self)
        self.folder_name_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Image file prompt
        tk.Button(self, text="Select Image File", command=self.select_image).grid(row=2, column=0, columnspan=1, pady=10)
        self.image_path_label = tk.Label(self, text="No file selected")
        self.image_path_label.grid(row=2, column=1, columnspan=2, pady=10)
        
        # Continue button
        tk.Button(self, text="Continue", command=self.check_inputs).grid(row=3, column=0, columnspan=2, pady=10)
        
        #return button
        tk.Button(self, text="Back to Start", command=lambda: os.execl(sys.executable, sys.executable, *sys.argv)).grid(row=4, column=0, columnspan=2, pady=10)


    def select_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image_path_label.config(text=file_path)
    
    def check_inputs(self):
        folder_name = self.folder_name_entry.get().strip()
        image_path = self.image_path_label.cget("text")
        
        if not folder_name or ' ' in folder_name or folder_name == 'file_name':
            messagebox.showwarning("Warning", "Please enter a valid file name.")
        elif image_path == "No file selected":
            messagebox.showwarning("Warning", "Please select an image file.")
        elif os.path.isdir(os.path.join('Templates',folder_name)):
            messagebox.showwarning("Warning", "Name Exist, Another valid file name please")
        # elif self.check_config_row():
        #     messagebox.showwarning("Warning", "Config Exist But No Folder Error, Contact Steven")
        else:
            self.new_template_generation()

    def check_and_generate_config_csv(self):
        
        config_file = os.path.join('Templates','config.csv')
        if not (os.path.isfile(config_file)):
            with open(config_file, 'w', newline='') as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerow(config_row_header)
        
    def check_config_row(self):
        folder_name = self.folder_name_entry.get().strip()
        config_file = os.path.join('Templates','config.csv')
        with open(config_file) as file:
            spamreader = csv.reader(config_file)
            for row in spamreader:
                if row[0] == folder_name:
                    return True
        
        return False

    def new_template_generation(self):
        
        #get values
        image_path = self.image_path_label.cget("text")
        folder_name = self.folder_name_entry.get().strip()

        #insert initialized config
        config_file = os.path.join('Templates','config.csv')
        with open(config_file, 'a',newline='') as f:
            writer = csv.writer(f)
            new_row = [folder_name] + [-1 for i in config_row_header[1:]]
            writer.writerow(new_row) 

        #new_dir
        folder_name =os.path.join('Templates',folder_name)
        os.makedirs(folder_name)        
        
        #save_image
        new_image_path = os.path.join(folder_name, 'template_image.png')
        img = Image.open(image_path)
        img = img.save(new_image_path)
        
        self.master.show_frame(SelectProjectPage)
        
#Project
class SelectProjectPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Configure Template Page", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(self, text="Back to Start", command=lambda: os.execl(sys.executable, sys.executable, *sys.argv)).pack()


class NewProjectPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="New Project Page", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=20)


#csv_actions

def get_config_csv_values(folder_name = None):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_file_path = os.path.join(dir_path, '../Templates/config.csv')
    rows = []
    with open(config_file_path) as file:
        spamreader = csv.reader(file)
        
        for row in spamreader:
            rows.append(row)
            if row[0] == folder_name:
                return row
            
    if folder_name == None:
        return rows
    return None

def get_template_list():    
    
    return [row[0] for row in get_config_csv_values()[1:]]

def translate_config_obj_to_row(config_obj):
    return [v.get() for (k,v) in config_obj.items()]

def modify_config_data(new_config_obj, delete_row = False):
    rows = get_config_csv_values()
    new_rows = []
    new_row = translate_config_obj_to_row(new_config_obj)
    print(new_row)
    for row in rows:
        if row[0] != new_row[0]:
            new_rows.append(row)
        else:
            if delete_row ==False:
                new_rows.append(new_row)
            else:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                template_dir_path = os.path.join(dir_path, '../Templates', new_row[0])
                if os.path.exists(template_dir_path):
                    shutil.rmtree(template_dir_path) 

    
    write_to_config(new_rows=new_rows)


def write_to_config(new_rows):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_file_path = os.path.join(dir_path, '../Templates/config.csv')
    print(new_rows)
    with open(config_file_path, 'w', newline= '') as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

def read_png(template_folder_name = None, project_folder_name = None, image_name = None):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    if template_folder_name == None and project_folder_name == None: #get default image
        img_path = os.path.join(dir_path, './tools/filler_image.png') if image_name == None else os.path.join(dir_path, './tools/filler_replacement.png')
    elif template_folder_name != None: 
        img_path = os.path.join(dir_path, '../Templates/', template_folder_name, 'template_image.png') 
        return
    elif project_folder_name != None: 
        img_path = os.path.join(dir_path, '../Templates/', template_folder_name, 'template_image.png') # MODDDDDDDDDDDDDDDDDDDDDD

    img = Image.open(img_path)
    return img  

def show_confirmation(on_confirm=None, on_cancel=None, Action = 'Save'):
    # Show a confirmation popup
    response = messagebox.askyesno(f"Confirm {Action}", f"Are you sure you want to {str(Action).lower()}?")
    
    if response:
        if on_confirm:
            on_confirm()
    else:
        if on_cancel:
            on_cancel()
            
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()






