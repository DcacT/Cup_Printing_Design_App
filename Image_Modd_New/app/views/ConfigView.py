from tkinter import OptionMenu, Frame, Label, Button, Scrollbar, Canvas, Listbox, END, StringVar

class ConfigTemplateView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_selected_var = StringVar(value='Select Template')
        self.template_list = [1,2,3,4,5]
        
        self.drop_down_frame = Frame(self, bg='red')
        self.drop_down_frame.grid(row=0, column=0, sticky='w')
        self.template_select_dropdown = OptionMenu(self.drop_down_frame , self.template_selected_var, *self.template_list)
        self.template_select_dropdown.pack( side='left',padx=5, pady=5, anchor='w')
        
        
        self.left_frame = Frame(self, bg = 'blue')
        self.left_frame.grid(row=1, column=0)
        self.scrollable_frame = self.load_scrollable_frame()
        self.scrollable_frame_content = {}

        
        self.right_frame = Frame(self)
        self.right_frame.grid(row = 1, column=1)
        self.img_label = Label(self.right_frame)
        self.img_label.grid(row=1, column=1)
        
        self.home_button = Button(self, text="Home")
        self.home_button.grid(row = 2, column = 0)
        pass        
    
        
    def load_scrollable_frame (self):
        canvas = Canvas(self.left_frame)
        canvas.pack(side='left', fill='both', expand=True)
        
        scrollbar = Scrollbar(self.left_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        scrollable_frame = Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        return scrollable_frame