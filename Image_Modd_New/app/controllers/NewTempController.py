from tkinter import filedialog
from tkinter import messagebox
from os.path import isfile
class NewTempController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["new_template"]
        self._bind()

    def _bind(self):
        self.frame.home_button.config(command = lambda: self.view.switch("home"))
        self.frame.image_button.config(command = self.select_image)
        self.frame.new_template_button.config(command = self.new_template)
        pass
    def select_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.frame.image_path_var.set(file_path)

    def new_template(self):
        folder_name = self.frame.folder_name_var.get()
        image_path = self.frame.image_path_var.get()
        #verify folder name 
        verify = self.model.config_sheet.verify(folder_name)
        if not verify:
            messagebox.showerror('Error', "Invalid Template Name! Try Another One")
            return 
        #verify image
        verify = isfile(image_path)
        if not verify:
            messagebox.showerror('Error', "Invalid Image! Try Another One")
            return

        self.model.config_sheet.new_template(folder_name,image_path)
        #success
        messagebox.showinfo('Success', "Template Created! Head over to Template Configuration next to configure via Home please")
