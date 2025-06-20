from tkinter import Frame, Label, Button, OptionMenu, StringVar, Canvas, Scrollbar, Menubutton, RAISED, Menu

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
        
        
        self.mid_frame_table_title_frame = Frame(self.mid_frame)
        self.mid_frame_table_title_frame.pack()
        table_title = ['ID', 'Name', 'Show', 'X%', 'Y%', 'Rot%', 'Scale%', 'Order_Index']
        table_title_width = [30,30,30,28,28,28,28,28]
        for i in range(len(table_title)):
            title = table_title[i]
            width = table_title_width[i]
            Label(self.mid_frame_table_title_frame, text=title).pack(side='left', ipadx=width)
        
        self.mid_frame_scrollable_frame_container_frame = Frame(self.mid_frame)
        self.mid_frame_scrollable_frame_container_frame.pack(fill='both', expand=True)
        self.mid_frame_scrollable_frame = self.load_scrollable_frame()

    
    def load_scrollable_frame (self):
        canvas = Canvas(self.mid_frame_scrollable_frame_container_frame)
        canvas.pack(side='left', fill='both', expand=True)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        scrollbar = Scrollbar(self.mid_frame_scrollable_frame_container_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        scrollable_frame = Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        return scrollable_frame

    def populate_left_frame_with_buttons(self):
        btn_list = [
            'add_image', 
            'save_project',
            'delete_project',
            'export_project',
            'home' 
        ]
        for btn_text in btn_list:
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
