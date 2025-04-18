from tkinter import Frame, Label, Button, Entry

class NewTemplateView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.header = Label(self, text="New Template")
        self.header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.folder_name_entry = Entry(self)
        self.folder_name_entry.grid(row=1, column=0, padx = 10, pady = 10)

        self.image_button = Button(self, text="Select Image File")
        self.image_button.grid(row=2, column=0, columnspan=1, pady=10)
        
        Label(self, text="New File Name:").grid(row=1, column=0, padx=10, pady=10)
        self.image_Entry = Entry(self)
        self.image_Entry.grid(row=1, column=1, padx=10, pady=10)       
        
        self.new_template_button = Button(self, text="Modify Template")
        self.new_template_button.grid(row=3, column=0, padx=10, pady=10)
        
        self.home_button = Button(self, text="home")
        self.home_button.grid(row=4, column=0, padx=10, pady=10)

