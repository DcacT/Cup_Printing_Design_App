from tkinter import filedialog, Label, Entry, StringVar, messagebox, Frame, Entry, Scale, Checkbutton, Button, IntVar

class CfgProjController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["cfg_project"]
        self.project_data = []
        self.populate_project_list_drop_down()
        self._bind()
        
    def _bind(self):
        self.frame.left_btn_dict['add_image'].config(command = self.add_image)
        pass

        
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

            iamge_show_widget = Checkbutton(t_frame, variable=image_data[2], command=self.refresh_image)
            iamge_show_widget.pack(side='left', ipadx=15)
            
            
            image_x_widget = Scale(t_frame, from_=0, to=100, orient="horizontal", command=lambda val: image_data[3].set(val),length=30)
            image_y_widget = Scale(t_frame, from_=0, to=100, orient="horizontal", command=lambda val: image_data[4].set(val),length=30)
            image_r_widget = Scale(t_frame, from_=0, to=100, orient="horizontal", command=lambda val: image_data[5].set(val),length=30)
            image_s_widget = Scale(t_frame, from_=0, to=100, orient="horizontal", command=lambda val: image_data[6].set(val),length=30)

            image_x_widget.set(image_data[3].get())
            image_y_widget.set(image_data[4].get())
            image_r_widget.set(image_data[5].get())
            image_s_widget.set(image_data[6].get())
            
            image_x_widget.pack(side='left', ipadx=40)
            image_y_widget.pack(side='left', ipadx=40)
            image_r_widget.pack(side='left', ipadx=40)
            image_s_widget.pack(side='left', ipadx=40)
            
            
           
            image_idx_widget = Entry(t_frame, textvariable=image_data[7])
            image_idx_widget.pack(side='left', ipadx=30)
            


                
    def refresh_image(self):
        pass

            

    def populate_project_list_drop_down(self):
        self.frame.project_list = self.model.project_manager.project_list
        menu = self.frame.project_select_dropdown['menu']
        menu.delete(0, "end")
        
        for option in self.frame.project_list:
            menu.add_command(label=option, command=lambda value=option: self.select_project(value))
        
        self.frame.project_name_var.set('Select Project')
        
    def select_project(self, project_name):
        self.frame.project_name_var.set(project_name)
        data = self.model.project_manager.get_project_data(project_name)
        data = [
            [
                row[0], 
                StringVar( value=row[1]), 
                IntVar( value=row[3]),
                IntVar( value=row[4]),
                IntVar( value=row[5]),
                IntVar( value=row[6]),
                IntVar( value=row[7]),
                IntVar( value=row[8]),
            ] 
            for row in data]
        
        self.project_data = data
        self.update_image_table()


        
    def add_image(self):
        if self.frame.project_name_var.get() == "Select Project":
            messagebox.showerror('Error', 'No Project Selected')
        else:
            file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
            if file_path:
                self.model.project_manager.new_img(self.frame.project_name_var.get(), file_path)
                messagebox.showinfo('Sucess', 'Image added')