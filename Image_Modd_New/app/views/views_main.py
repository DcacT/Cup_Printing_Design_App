

from .root import Root
from .HomeView import HomeView
from .NewTempView import NewTemplateView
from .ConfigView import ConfigTemplateView
class View:
    def __init__(self):
        self.root = Root()
        self.frames = {}
        # self._add_frame(SignUpView, "signup")
        # self._add_frame(SignInView, "signin")
        self._add_frame(NewTemplateView, "new_template")
        self._add_frame(ConfigTemplateView, "cfg_template")
        self._add_frame(HomeView, "home")

    def _add_frame(self, Frame, name):
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def switch(self, name):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[name]
        frame.reset()
        frame.grid()
        frame.tkraise()
        self.root.update()
        self.root.geometry("")
        
        
        
    def start_mainloop(self):
        self.root.mainloop()