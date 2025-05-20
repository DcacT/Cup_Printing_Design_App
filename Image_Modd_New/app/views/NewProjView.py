from tkinter import Frame, Label, Button, Entry, StringVar, OptionMenu

class NewProjView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_name_var = StringVar(value = "")
        self.template_name_var = StringVar(value='Select Template')
        self.template_list = [1,2,3,4,5]

        # self.grid_columnconfigure(0, weight=1)

        self.header = Label(self, text="New Project")
        self.header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.template_select_frame = Frame(self, bg='red')
        self.template_select_frame.grid(row=1, column=0, sticky='w')
        self.template_select_dropdown = OptionMenu(self.template_select_frame , self.template_name_var, *self.template_list)
        self.template_select_dropdown.pack(padx=5, pady=5)
        
  
        self.project_name_frame = Frame(self)
        self.project_name_frame.grid(row=2, column=0, sticky='w')

        Label(self.project_name_frame, text="New Project Name:").pack(padx=5, pady=5, side = 'left')
        self.project_name_entry = Entry(self.project_name_frame, textvariable=self.project_name_var)
        self.project_name_entry.pack(padx=5, pady=5, side = 'left')     
        

        self.new_template_button = Button(self, text="Create New Template")
        self.new_template_button.grid(row=3, column=0, padx=10, pady=10)
        
        self.home_button = Button(self, text="home")
        self.home_button.grid(row=4, column=0, padx=10, pady=10)

    def reset(self):
        pass