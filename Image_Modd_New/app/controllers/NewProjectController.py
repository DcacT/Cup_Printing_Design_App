from tkinter import filedialog, messagebox
from os.path import isfile

class NewProjController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["new_project"]
        self._bind()

    def _bind(self):
        self.frame.home_button.config(command = lambda: self.view.switch("home"))
        pass
