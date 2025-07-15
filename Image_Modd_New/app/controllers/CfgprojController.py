from tkinter import filedialog, Label, Entry, StringVar, messagebox, Frame, Entry, Scale, Checkbutton, Button, IntVar, TclError
from functools import partial
from PIL import Image,ImageTk
import cv2
import os
self_path = os.path.dirname(os.path.realpath(__file__))
projects_folder_path = os.path.join(self_path, '../../data/projects')

resize_ratio = 0.5
class CfgProjController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["cfg_project"]
        self.vcmd = self.frame.register(self.only_int)
        
        self.populate_project_list_drop_down()
        self._bind()
        
    def _bind(self):
        self.frame.left_btn_dict['add_image'].config(command = self.add_image)
        self.frame.left_btn_dict['delete_project'].config(command = self.delete_project)
        self.frame.left_btn_dict['home'].config(command=self.go_to_home)
        self.frame.left_btn_dict['save_project'].config(command = self.update_project)
        self.frame.reset_trigger.trace_add("write", partial(self.reset, self.frame.reset_trigger))

        pass
    
    def reset(self, *args):
        self.populate_project_list_drop_down()


    def go_to_home(self):
        self.populate_project_list_drop_down()
        self.view.switch("home")
    
    def update_project(self):
        self.model.project.update_project()
        messagebox.showinfo('Sucess', 'Project Saved! ')      

    def delete_project(self):

        project_name = self.frame.project_name_var.get()
        ok = messagebox.askokcancel("Delete?", f"Are you sure of deleting project {self.frame.project_name_var.get()}")

        if ok: 
            self.model.project.delete_project()
            print('project_deleted')
            messagebox.showinfo('Sucess', 'Project Deleted! ')
            self.go_to_home()
        
    def update_image_table(self):
        #clear
        self.model.project.read_project()  
        print(self.model.project.project_data.keys())
        for widget in self.frame.mid_frame_scrollable_frame.winfo_children():
            print('d')
            widget.destroy()
        
        for id, image_data in self.model.project.project_data.items():
            t_frame = Frame(self.frame.mid_frame_scrollable_frame, bg='red')
            t_frame.pack()
            
            image_id_widget = Label(t_frame, textvariable=image_data['Image_ID'])
            image_id_widget.pack(side='left', ipadx=15)

            
            image_name_widget = Entry(t_frame, textvariable=image_data['Image_Name'])
            image_name_widget.pack(side='left', ipadx=15)

            image_idx_widget = Label(t_frame, textvariable=image_data['Order_Index']) 
            image_idx_widget.pack(side='left', ipadx=15)

            adjust_button = Button(t_frame, text=">>>>>", command=partial(self.on_select_adjust_btn, image_id = image_data['Image_ID'].get()))
            adjust_button.pack(side='left')
            

    def on_select_adjust_btn(self, image_id):
        for widget in self.frame.mid_frame_right.winfo_children():
            widget.destroy()

        if self.frame.selected_image_id.get() != image_id:
            self.frame.selected_image_id.set(image_id)
            
            image_data = next((row for id, row in self.model.project.project_data.items() if id == image_id), None)
            
            image_x_widget = Entry(self.frame.mid_frame_right, textvariable=image_data['x_Percent'], width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            
            image_y_widget = Entry(self.frame.mid_frame_right, textvariable=image_data['y_Percent'], width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            
            image_r_widget = Entry(self.frame.mid_frame_right, textvariable=image_data['Rotation'], width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            
            image_s_widget = Entry(self.frame.mid_frame_right, textvariable=image_data['Scale'], width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            
            order_idx_adjust_frame = Frame(self.frame.mid_frame_right, bg='green')
            t =8
            order_idx_adjust_up_btn = Button(order_idx_adjust_frame, text = f'{" "*t}↑{" "*t}', command=lambda: self.on_select_order_idx_adjust_btn(direction_up=True))
            order_idx_adjust_dn_btn = Button(order_idx_adjust_frame, text = f'{" "*t}↓{" "*t}', command=lambda: self.on_select_order_idx_adjust_btn(direction_up=False))
            
            image_delete_btn = Button(self.frame.mid_frame_right, text = f'Delete Image', command=lambda: self.on_select_delete_image())


            Label(self.frame.mid_frame_right, text=f'image name: ').pack()
            Label(self.frame.mid_frame_right, text=f'{image_data["Image_Name"].get()}').pack()
            
            Label(self.frame.mid_frame_right, text='x%').pack()
            image_x_widget.pack(side='top')
            
            Label(self.frame.mid_frame_right, text='y%').pack()
            image_y_widget.pack(side='top')
            
            Label(self.frame.mid_frame_right, text='rotation%').pack()
            image_r_widget.pack(side='top')
            
            Label(self.frame.mid_frame_right, text='size%').pack()
            image_s_widget.pack(side='top')
            
            Label(self.frame.mid_frame_right, text= 'Order Index').pack()

            order_idx_adjust_frame.pack(side='top')
            order_idx_adjust_up_btn.pack(side='left')
            order_idx_adjust_dn_btn.pack(side='left')
            
            Label(self.frame.mid_frame_right, text=f' ').pack()

            image_delete_btn.pack()
            
        else:
            self.frame.selected_image_id.set('-69420')
            

    def on_select_delete_image(self ):
        image_id = self.frame.selected_image_id.get()
        if messagebox.askokcancel('Delete Image', 'Are you sure about deleting this image?'):
            self.model.project.delete_image(image_id)
            self.update_image_table()


    def on_select_order_idx_adjust_btn(self, direction_up = True):
        
        image_id = self.frame.selected_image_id.get()
        self.model.project.update_order_idx(image_id, direction_up)
        # self.refresh_image()
                
    def refresh_image(self):
        
        # template_image = self.model.project.template_data['template_image']
        template_image = self.model.project.get_display_image()
        
        h, w = template_image.shape[:2]        
        
        img_rgb = cv2.cvtColor(template_image, cv2.COLOR_BGR2RGB)
        img_resize = cv2.resize(img_rgb, (int(w*resize_ratio), int(h*resize_ratio)) )
        img_pil = Image.fromarray(img_resize)
        img_tk = ImageTk.PhotoImage(img_pil)
        
        self.frame.img_label.config(image=img_tk)
        self.frame.img_label.image = img_tk
        pass

    def populate_project_list_drop_down(self):
        menu = self.frame.project_select_dropdown['menu']
        menu.delete(0, "end")
        project_list =  os.listdir(projects_folder_path)
        
        
        for option in project_list:
            menu.add_command(label=option, command=lambda value=option: self.select_project(value))
        
        self.frame.project_name_var.set('Select Project')
    
    def select_project(self, project_name):
        self.frame.project_name_var.set(project_name)
        
        self.model.project.load_project(project_name)
        
        self.update_image_table()
        self.refresh_image()

    def add_image(self):
        if self.frame.project_name_var.get() == "Select Project":
            messagebox.showerror('Error', 'No Project Selected')
        else:
            file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
            if file_path:
                self.model.project.add_image(file_path)
                self.update_image_table()

                messagebox.showinfo('Sucess', 'Image added')
                

    def only_int(self, new_val):
        return new_val == "" or new_val == "-" or new_val.lstrip('-').isdigit()



