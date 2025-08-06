from tkinter import IntVar, OptionMenu, Frame, Label, Button, Scrollbar, Canvas, Listbox, END, StringVar,Checkbutton

class ConfigTemplateView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_selected_var = StringVar(value='Select Template')
        self.template_list = [1,2,3,4,5]
        
        self.drop_down_frame = Frame(self, bg='red')
        self.drop_down_frame.grid(row=0, column=0, sticky='w')
        self.template_select_dropdown = OptionMenu(self.drop_down_frame , self.template_selected_var, *self.template_list)
        self.template_select_dropdown.pack(padx=5, pady=5)
        
        self.left_frame = Frame(self)
        self.left_frame.grid(row=1, column=0)
        self.delete_template_button = Button(self.left_frame, text='delete template')
        self.delete_template_button.grid(row=0, column=0, columnspan=2)
        self.save_template_button = Button(self.left_frame, text='save template')
        self.save_template_button.grid(row=0, column=2,columnspan=2)
        self.update_image_button = Button(self.left_frame, text='update image')
        self.update_image_button.grid(row=1, column=2, columnspan=2)
        
        
        self.display_contour_status = IntVar()
        self.display_contour_checkbox = Checkbutton(self.left_frame, text="contour", variable=self.display_contour_status, onvalue=1, offvalue=0)
        self.display_contour_checkbox.grid(row=2, column=0,columnspan=2)
        
        self.display_border_status = IntVar()
        self.display_border_checkbox = Checkbutton(self.left_frame, text="borders", variable=self.display_border_status, onvalue=1, offvalue=0)
        self.display_border_checkbox.grid(row=2, column=2,columnspan=2)
        
        
        self.contour_list = [-1]
        self.selected_contour_id = IntVar(value=-1)
        self.contour_select_dropdown = OptionMenu(self.left_frame, self.selected_contour_id,*self.contour_list)
        self.contour_select_dropdown.grid(row=3, column=0, sticky = 'w')
        
        self.total_contour_count_var = StringVar(value='/-1')
        self.total_contour_count_label = Label(self.left_frame, textvariable=self.total_contour_count_var)
        self.total_contour_count_label.grid(row=3, column=1)

        self.action_list = [
            'Left Border',
            'Right Border',
            'Top Border',
            'Bottom Border',
        ]
        self.selected_action = StringVar(value='No Action Selected')
        self.action_select_drop_down = OptionMenu(self.left_frame, self.selected_action, *self.action_list)
        self.action_select_drop_down.grid(row=3, column=2, columnspan=2, sticky="ew")
        
        self.prev_prev_contour_button = Button(self.left_frame, text='<<')
        self.prev_prev_contour_button.grid(row=4, column=0,sticky="ew")
        self.prev_contour_button = Button(self.left_frame, text='<')
        self.prev_contour_button.grid(row=4, column=1,sticky="ew")
        self.next_contour_button = Button(self.left_frame, text='>')
        self.next_contour_button.grid(row=4, column=2,sticky="ew")
        self.next_next_contour_button = Button(self.left_frame, text='>>')
        self.next_next_contour_button.grid(row=4, column=3, sticky="ew")


        self.select_contour_button = Button(self.left_frame, text='De/Select Contour')
        self.select_contour_button.grid(row=5, column=0, columnspan=4 ,sticky="ew")
        
        self.generate_border_button = Button(self.left_frame, text='Generate Border')
        self.generate_border_button.grid(row=6, column=0, columnspan=4 ,sticky="ew")


        
        
        
        self.middle_frame = Frame(self, bg = 'blue')
        self.middle_frame.grid(row=1, column=1, sticky='nsew')
        self.scrollable_frame = self.load_scrollable_frame()
        self.scrollable_frame_content = {}

        
        self.right_frame = Frame(self)
        self.right_frame.grid(row = 1, column=2, sticky='nsew')
        self.img_label = Label(self.right_frame)
        self.img_label.pack()
        
        self.home_button = Button(self, text="Home")
        self.home_button.grid(row = 2, column = 0)
        pass        
    
        
    def load_scrollable_frame (self):
        canvas = Canvas(self.middle_frame)
        canvas.pack(side='left', fill='both', expand=True)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        scrollbar = Scrollbar(self.middle_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        scrollable_frame = Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        return scrollable_frame
    
    def reset(self):

        pass