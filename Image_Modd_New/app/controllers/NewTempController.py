class NewTempController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["new_template"]
        self._bind()

    def _bind(self):
        self.frame.home_btn.config(command = lambda: self.view.switch("home"))
        pass