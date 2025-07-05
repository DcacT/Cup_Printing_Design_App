from tkinter import filedialog, Label, Entry, StringVar, messagebox, Frame, Entry, Scale, Checkbutton, Button, IntVar, TclError
from functools import partial
from PIL import Image,ImageTk
import cv2
resize_ratio = 0.5
class CfgProjController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["cfg_project"]
        self.vcmd = self.frame.register(self.only_int)

        self.project_data = []
        self.template_data = {}
        self.populate_project_list_drop_down()
        self._bind()
        
    def _bind(self):
        self.frame.left_btn_dict['add_image'].config(command = self.add_image)
        self.frame.left_btn_dict['delete_project'].config(command = self.delete_project)
        self.frame.left_btn_dict['home'].config(command=self.go_to_home)
        self.frame.left_btn_dict['save_project'].config(command = self.update_project)
        pass


    # def layer_display_image(self):
    #     for image in self.project_data:
    #         if []

    def go_to_home(self):
        self.populate_project_list_drop_down()
        self.view.switch("home")
    
    def update_project(self):
        project_name = self.frame.project_name_var.get()

        project_data = [
            [row[0], row[1].get(), row[2].get(), row[3].get(), row[4].get(), row[5].get(), row[6].get()]
            for row in self.project_data]

        res = self.model.project_manager.update_project(project_name, project_data)
        messagebox.showinfo('Sucess', 'Project Saved! ')


            
            
            

    def delete_project(self):

        project_name = self.frame.project_name_var.get()
        ok = messagebox.askokcancel("Delete?", f"Are you sure of deleting project {project_name}")

        if ok: 
            self.model.project_manager.delete_project(project_name)
            print('project_deleted')
            messagebox.showinfo('Sucess', 'Project Deleted! ')
            self.go_to_home()
        
    def update_image_table(self):
        #clear
        for widget in self.frame.mid_frame_scrollable_frame.winfo_children():
            widget.destroy()
        #replenish
        # table_title = ['ID', 'Name', 'Show', 'X%', 'Y%', 'Rot%', 'Scale%', 'Order_Index']
        # table_title_width = [30,30,30,30,30,30,30,30]
        for image_data in self.project_data:
            t_frame = Frame(self.frame.mid_frame_scrollable_frame, bg='red')
            t_frame.pack()
            
            image_id_widget = Label(t_frame, text=image_data[0])
            image_id_widget.pack(side='left', ipadx=15)

            
            image_name_widget = Entry(t_frame, textvariable=image_data[1])
            image_name_widget.pack(side='left', ipadx=15)

            image_idx_widget = Entry(t_frame, textvariable=image_data[2],width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            image_idx_widget.pack(side='left')

            adjust_button = Button(t_frame, text=">>>>>", command=lambda: self.on_select_adjust_btn(image_data[0]))
            adjust_button.pack(side='left')

            # image_x_widget = Entry(t_frame, textvariable=image_data[3], width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            # image_y_widget = Entry(t_frame, textvariable=image_data[4], width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            # image_r_widget = Entry(t_frame, textvariable=image_data[5], width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            # image_s_widget = Entry(t_frame, textvariable=image_data[6], width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            
            # image_x_widget.pack(side='left')
            # image_y_widget.pack(side='left')
            # image_r_widget.pack(side='left')
            # image_s_widget.pack(side='left')
            
            
    def on_select_adjust_btn(self, image_id):
        for widget in self.frame.mid_frame_right.winfo_children():
            widget.destroy()

        if self.frame.selected_image_id.get() != image_id:
            self.frame.selected_image_id.set(image_id)
            image_data = next((row for row in self.project_data if row[0] == image_id), None)
            image_x_widget = Entry(self.frame.mid_frame_right, textvariable=image_data[3], width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            
            image_y_widget = Entry(self.frame.mid_frame_right, textvariable=image_data[4], width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            
            image_r_widget = Entry(self.frame.mid_frame_right, textvariable=image_data[5], width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            
            image_s_widget = Entry(self.frame.mid_frame_right, textvariable=image_data[6], width=15, validate='key', validatecommand= (self.vcmd, '%P'))
            
            Label(self.frame.mid_frame_right, text=f'image name: ').pack()
            Label(self.frame.mid_frame_right, text=f'{image_data[1].get()}').pack()
            Label(self.frame.mid_frame_right, text='x%').pack()
            image_x_widget.pack(side='top')
            Label(self.frame.mid_frame_right, text='y%').pack()

            image_y_widget.pack(side='top')
            Label(self.frame.mid_frame_right, text='rotation%').pack()

            image_r_widget.pack(side='top')
            Label(self.frame.mid_frame_right, text='size%').pack()
            image_s_widget.pack(side='top')
            
        else:
            self.frame.selected_image_id.set('-69420')

    
                
    def refresh_image(self):
        
        template_image = self.template_data[-1]
        h, w = template_image.shape[:2]
        
        img_rgb = cv2.cvtColor(template_image, cv2.COLOR_BGR2RGB)
        img_resize = cv2.resize(img_rgb, (int(w*resize_ratio), int(h*resize_ratio)) )
        img_pil = Image.fromarray(img_resize)
        img_tk = ImageTk.PhotoImage(img_pil)
        
        self.frame.img_label.config(image=img_tk)
        self.frame.img_label.image = img_tk
        pass

            

    def populate_project_list_drop_down(self):
        self.frame.project_list = self.model.project_manager.project_list
        menu = self.frame.project_select_dropdown['menu']
        menu.delete(0, "end")
        
        for option in self.frame.project_list:
            menu.add_command(label=option, command=lambda value=option: self.select_project(value))
        
        self.frame.project_name_var.set('Select Project')
    
    def load_image_from_path(self, path = '', is_template = False):
        project_name = self.frame.project_name_var.get()

        if is_template:
            
            pass
        else:
            pass
    def select_project(self, project_name):
        self.frame.project_name_var.set(project_name)
        data = self.model.project_manager.get_project_data(project_name)
        self.project_data = [
            [
                row[0], 
                StringVar( value=row[1]), 
                IntVar( value=int(row[3])),
                IntVar( value=int(row[4])),
                IntVar( value=int(row[5])),
                IntVar( value=int(row[6])),
                IntVar( value=int(row[7])),
            ] 
            for row in data['project_data']]
        self.template_data = data['template_data']
        for row_id, row in enumerate(self.project_data):
            for i in [3,4,5,6]:
                row[i].trace_add("write", partial(self.validate_range_input,row[i]))
                
            row[2].trace_add("write", lambda *args: self.validate_order_input(row[2], row_id, True))
            
        self.update_image_table()
        # self.model.project_manager.get_project_data(project_name)
        self.refresh_image()


    def validate_order_input(self, check_var, row_id, origin, *args):
        
        try:
            value = check_var.get()
            project_data_len = sum(row[2] != -1 for row in self.project_data)
            
            if isinstance(value, int) or value == '-':
                if not (-1 <= value <= project_data_len):
                    check_var.set(project_data_len if value > project_data_len else -1)
                
        except TclError:
            print('tclerror')
            pass  # In case of non-integer input  
        
    def validate_range_input(self, check_var,*args):
        
        try:
            value = check_var.get()
            if isinstance(value, int) or value == '-' or value == '':
                if not (-1 <= value <= 100):
                    check_var.set(100 if value > 100 else -1)
            else: 
                print('false')
                check_var.set('-1')
        except TclError:
            pass  # In case of non-integer input  
              
 
    
    
    def add_image(self):
        if self.frame.project_name_var.get() == "Select Project":
            messagebox.showerror('Error', 'No Project Selected')
        else:
            file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
            if file_path:
                self.model.project_manager.new_img(self.frame.project_name_var.get(), file_path)
                messagebox.showinfo('Sucess', 'Image added')

    def only_int(self, new_val):
        return new_val == "" or new_val == "-" or new_val.lstrip('-').isdigit()



