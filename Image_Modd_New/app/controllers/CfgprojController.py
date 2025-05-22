from tkinter import filedialog, Label, Entry, StringVar, messagebox
class CfgProjController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["cfg_project"]
        
        self.populate_project_list_drop_down()
        self._bind()
    def _bind(self):
        self.frame.left_btn_dict['add_image'].config(command = self.add_image)
        pass
    
    def populate_project_list_drop_down(self):
        self.frame.project_list = self.model.project_manager.project_list
        menu = self.frame.project_select_dropdown['menu']
        menu.delete(0, "end")
        
        for option in self.frame.project_list:
            menu.add_command(label=option, command=lambda value=option: self.frame.project_name_var.set(value))
        
        self.frame.project_name_var.set('Select Project')

    def add_image(self):
        if self.frame.project_name_var.get() == "Select Project":
            messagebox.showerror('Error', 'No Project Selected')
        else:
            file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
            if file_path:
                self.model.project_manager.new_img(self.frame.project_name_var.get(), file_path)
                messagebox.showinfo('Sucess', 'Image added')