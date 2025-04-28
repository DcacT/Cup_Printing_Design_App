from tkinter import Frame, Label, Button, Entry, StringVar

class NewTemplateView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.folder_name_var = StringVar()
        self.image_path_var = StringVar()

        # self.grid_columnconfigure(0, weight=1)

        self.header = Label(self, text="New Template")
        self.header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.folder_name_entry = Entry(self, textvariable=self.folder_name_var)
        self.folder_name_entry.grid(row=1, column=1, padx = 10, pady = 10)

        self.image_button = Button(self, text="Select Image File")
        self.image_button.grid(row=2, column=0, pady=10)
        
        Label(self, text="New File Name:").grid(row=1, column=0, padx=10, pady=10)
        self.image_Entry = Entry(self, textvariable=self.image_path_var)
        self.image_Entry.grid(row=2, column=1, padx=10, pady=10)       
        
        self.new_template_button = Button(self, text="Create New Template")
        self.new_template_button.grid(row=3, column=0, padx=10, pady=10)
        
        self.home_button = Button(self, text="home")
        self.home_button.grid(row=4, column=0, padx=10, pady=10)

    def reset(self):
        pass