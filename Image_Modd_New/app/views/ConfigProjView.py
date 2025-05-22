from tkinter import Frame, Label, Button, OptionMenu, StringVar

class CfgProjView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_name_var = StringVar(value="Select Project")
        self.project_list = ['1']
        self.left_frame = Frame(self)
        self.left_frame.pack(side='left')
        self.mid_frame = Frame(self)
        self.mid_frame.pack(side='left')
        self.right_frame = Frame(self)
        self.right_frame.pack(side='left')
    
        Label(self.left_frame, text="Edit Project").pack()
        Label(self.left_frame, text="Current Project: ").pack()
        self.project_select_dropdown = OptionMenu(self.left_frame , self.project_name_var, *self.project_list)
        self.project_select_dropdown.pack(padx=5, pady=5)
        
        self.left_btn_dict = {}
        self.populate_left_frame_with_buttons()

    def populate_left_frame_with_buttons(self):
        btn_list = [
            'add_image', 
            'save_project',
            'delete_project',
            'export_project',
            'home' 
        ]
        for btn_text in btn_list:
            print(' '.join(btn_text.split('_')))
            self.left_btn_dict[btn_text] = Button(self.left_frame, text= ' '.join(btn_text.split('_')))
            self.left_btn_dict[btn_text].pack(padx=10, pady=10)
        
    def reset(self):
        pass
        
###
# add image 
# delete project
# save project
# export project
# 
#image actions
# sliders? 
# ###