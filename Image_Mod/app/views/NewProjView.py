from tkinter import Frame, Label, Button, Entry, StringVar, OptionMenu

class NewProjView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_name_var = StringVar(value = "")
        self.template_name_var = StringVar(value='Select Template')
        self.template_list = [1,2,3,4,5]

        # self.grid_columnconfigure(0, weight=1)
        self.left_frame = Frame(self)
        self.left_frame.pack(side='left')
        
        self.header = Label(self.left_frame, text="New Project")
        self.header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.template_select_frame = Frame(self.left_frame, bg='red')
        self.template_select_frame.grid(row=1, column=0, sticky='w')
        self.template_select_dropdown = OptionMenu(self.template_select_frame , self.template_name_var, *self.template_list)
        self.template_select_dropdown.pack(padx=5, pady=5)
        
  
        self.project_name_frame = Frame(self.left_frame)
        self.project_name_frame.grid(row=2, column=0, sticky='w')

        Label(self.project_name_frame, text="New Project Name:").pack(padx=5, pady=5, side = 'left')
        self.project_name_entry = Entry(self.project_name_frame, textvariable=self.project_name_var)
        self.project_name_entry.pack(padx=5, pady=5, side = 'left')     
        

        self.new_project_button = Button(self.left_frame, text="Create New Project")
        self.new_project_button.grid(row=3, column=0, padx=10, pady=10)
        
        self.home_button = Button(self.left_frame, text="home")
        self.home_button.grid(row=4, column=0, padx=10, pady=10)
        
        self.right_frame = Frame(self)
        self.right_frame.pack(side='left')
        self.img_label = Label(self.right_frame)
        self.img_label.pack()
        
        
    def reset(self):
        
        pass