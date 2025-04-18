from tkinter import filedialog

class NewTempController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["new_template"]
        self._bind()

    def _bind(self):
        self.frame.home_button.config(command = lambda: self.view.switch("home"))
        self.frame.image_button.config(command = self.select_image)
        pass
    def select_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image_Entry.config(text=file_path)