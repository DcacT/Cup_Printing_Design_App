import tkinter as tk
import sys
import os
import csv
from tkinter import filedialog, messagebox, Scrollbar, Canvas, Entry,StringVar, OptionMenu, BooleanVar, IntVar
from PIL import Image, ImageTk
import shutil 
from ..tools.TemplateImgTools import TemplateImageProcessor
from ..tools.ConfigTools import * 
from ..tools.TemplateImgTools import TemplateImageProcessor
import tkinter as tk




class ConfigureTemplatePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.selected_template_folder = StringVar(self, value = 'None')
        self.selected_contour_index = IntVar(self, value = '-1')

        self.template_configuration =  self.get_default_template_configuration()
        self.img_processor = TemplateImageProcessor(self.template_configuration)

        self.scrollable_frame = self.load_left_frame()
        self.dropdown = self.load_left_frame_drop_down()
        self.configuration_entries = {}
        self.load_left_frame_configuration_entries()
        self.left_frame_buttons = self.load_left_frame_buttons()
        self.left_frame_contour_selector = self.load_left_frame_contour_selector()
        self.img_frame = self.load_right_frame()
        self.img_label = self.load_right_frame_image()
        self.selected_contour_list_drop_down = self.load_selected_contours_list()
        self.contour_action_buttons = self.load_contour_action_buttons()

    def get_default_template_configuration(self):
        return {
            'folder_name': tk.StringVar(value=''),
            'PX_Min': tk.StringVar(value='-1'),  # Pixel Count
            'PX_Max': tk.StringVar(value='-1'),
            'Horizontal_Limit': tk.StringVar(value='-1'),  # Aspect Ratio
            'Vertical_Limit': tk.StringVar(value='-1'),
            
            'Line_1_vx': tk.StringVar(value='-1'),  # line1
            'Line_1_vy': tk.StringVar(value='-1'),
            'Line_1_x0': tk.StringVar(value='-1'),
            'Line_1_y0': tk.StringVar(value='-1'),

            'Line_2_vx': tk.StringVar(value='-1'),  # line2
            'Line_2_vy': tk.StringVar(value='-1'),
            'Line_2_x0': tk.StringVar(value='-1'),
            'Line_2_y0': tk.StringVar(value='-1'),
            
            'Arc_1_x': tk.StringVar(value='-1'),  # arc1
            'Arc_1_y': tk.StringVar(value='-1'),
            'Arc_1_r': tk.StringVar(value='-1'),
            
            'Arc_2_x': tk.StringVar(value='-1'),  # arc2
            'Arc_2_y': tk.StringVar(value='-1'),
            'Arc_2_r': tk.StringVar(value='-1'),
        }
    def update_img_label(self, new_img = None):

        new_img =self.img_processor.convert_cv2_to_tk(img_cv2= new_img, default=False if new_img is not None else True)
        
        self.img_label.config(image=new_img)
        self.img_label.image = new_img

    def update_selected_contours_list(self): 
        
        new_index = self.img_processor.selected_contour
        if new_index != -1:
            if new_index not in self.img_processor.selected_contour_index_list:
                self.img_processor.selected_contour_index_list.append(new_index)

            else:
                self.img_processor.selected_contour_index_list.remove(new_index)

            self.selected_contour_list_drop_down['menu'].delete(0, 'end')
            options = self.img_processor.selected_contour_index_list
            
            # Add new options
            for option in options:
                self.selected_contour_list_drop_down['menu'].add_command(label=option, command=lambda option = option: self.selected_contour_index.set(option))


    def update_contour_index_label(self):
        print('update')
        current_index = self.img_processor.selected_contour
        total_count = len(self.img_processor.all_contours)
        total_count = total_count if total_count > 0 else '?'
        display_text = f'Contour: {current_index}/{total_count}'

        self.contour_action_buttons['selected_contour_index_label'].config(text = display_text)
        self.contour_action_buttons['selected_contour_index_label'].text = display_text
    
    def load_contour_action_buttons(self):
        selected_contour_index_label = tk.Label(self.scrollable_frame, text= 'Contour: ?/?')
        selected_contour_index_label.grid(row=24, column=1, padx = 10, pady = 5, sticky = 'w')
        tk.Label(self.scrollable_frame, text= 'Actions').grid(row=25, column=1, padx = 10, pady = 5, sticky = 'w')
        
        next_contour_button = tk.Button(self.scrollable_frame, text="Next Contour", command=self.highlight_next_contour)
        next_contour_button.grid(row=26, column=1, pady=10)
        

        prev_contour_button = tk.Button(self.scrollable_frame, text="Prev Contour",command=self.highlight_prev_contour)
        prev_contour_button.grid(row=27, column=1, pady=10)

        select_contour_button = tk.Button(self.scrollable_frame, text="Select Contour",command=self.update_selected_contours_list)
        select_contour_button.grid(row=28, column=1, pady=10)

        return {
            'selected_contour_index_label':selected_contour_index_label,
            'next_contour_button':next_contour_button,
            'prev_contour_button':prev_contour_button
        } 
   
    def load_selected_contours_list(self):
        selected_contour_index_list = self.img_processor.selected_contour_index_list
        
        options = selected_contour_index_list
        
        tk.Label(self.scrollable_frame, text= 'Selected Contours').grid(row=25, column=2, padx = 10, pady = 5, sticky = 'w')
        dropdown = OptionMenu(self.scrollable_frame, self.selected_contour_index, *options if len(options)>0 else['None'])
        dropdown.config(width=15)
        dropdown.grid(row=26, column=2, padx=10, pady=5, sticky="w")        
        
        self.selected_contour_index.trace_add("write", self.process_contour_list_drop_down_select)
        return dropdown
    
    def process_contour_list_drop_down_select(self, *args):
        self.img_processor.selected_contour = self.selected_contour_index.get()
        
        self.update_contour_index_label()
        new_img = self.img_processor.get_dispay_image()
        self.update_img_label(new_img = new_img)


    def get_line1(self): 
        print('get_line1')
        (vx,vy,x0,y0) = self.img_processor.calculate_straight()

        def f(key, val):
            print('k: ', key, ';val: ', val)
            self.template_configuration[key].set(val)

        j = {
            'Line_1_vx':vx,
            'Line_1_vy':vy,
            'Line_1_x0':x0,
            'Line_1_y0':y0,
        }
        for k, v in j.items():
            f(k, v)

        self.img_processor.template_configuration = {k:v.get() for k, v in self.template_configuration} 
        self.update_img_label()
        return 
    
    # def get_Arc2(self):

    def load_right_frame_image(self):
        # only when init that we load lebron
        img_tk = self.img_processor.convert_cv2_to_tk(default=True)
        img_label = tk.Label(self.img_frame, image=img_tk)
        img_label.image = img_tk
        img_label.grid(row=0, column=0, sticky='nsew')
        return img_label

    def load_right_frame(self):
        right_frame = tk.Frame(self)
        right_frame.grid(row = 0, column=1, sticky='nsew')
        return right_frame
    
    # def convert_image_path_to_tk(self, image_path):
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(image)
        return image_tk
    
    def load_left_frame_contour_selector(self):
        total_contour_count = self.img_processor.all_contours
        selected_idx = self.img_processor.all_contours
        # tk.Label(self.scrollable_frame, text='Contour: ').grid(row = 25, column=0)
        # tk.Label(self.scrollable_frame, text = '-1').grid(row=25, column=1)
        # tk.Label(self.scrollable_frame, text = '/35').grid(row=25, column=2)

        # tk.Button(self.scrollable_frame, text="Prev Contour", 
        #           command=lambda: self.delete_template()).grid(row=26, column=0)
        # tk.Button(self.scrollable_frame, text="Select Contour", 
        #           command=lambda: self.delete_template()).grid(row=26, column=1)
        # tk.Button(self.scrollable_frame, text="Next Contour", 
        #           command=lambda: self.delete_template()).grid(row=26, column=2)        
        
        # tk.Label(self.scrollable_frame, text='Selected Contours: ').grid(row = 27)



    # def load_left_frame_sub_buttons(self):

    #     if self.img_processor.image_state['Display_Contour']:
    #         self.left_frame_buttons['select_arc_1_button'].grid_forget()
    #         self.left_frame_buttons['select_arc_2_button'].grid_forget()
    #         self.left_frame_buttons['select_line_1_button'].grid_forget()
    #         self.left_frame_buttons['select_line_2_button'].grid_forget()
    #     else:
    #         self.left_frame_buttons['select_arc_1_button'].grid(row=25, column=0, pady=10)
    #         self.left_frame_buttons['select_arc_2_button'].grid(row=26, column=0, pady=10)
    #         self.left_frame_buttons['select_line_1_button'].grid(row=27, column=0, pady=10)
    #         self.left_frame_buttons['select_line_2_button'].grid(row=28, column=0, pady=10)


    def load_left_frame_buttons(self):
        save_config_button = tk.Button(self.scrollable_frame, text="Save Config", 
                  command=lambda: show_confirmation(on_confirm=lambda: 
                                                    self.save_config()))
        save_config_button.grid(row=21, column=0, pady=10)
        
        show_contour_button = tk.Button(self.scrollable_frame, 
                  text="Hide Contour" if self.img_processor.image_state['Display_Contour'] else "Show Contour",
                  command = self.process_show_contour
                  )
        show_contour_button.grid(row=22, column=0, pady=10)
        
        delete_config_button = tk.Button(self.scrollable_frame, text="Delete Config", 
                  command=lambda: self.delete_template()).grid(row=21, column=1, pady=10)
        print_config_button = tk.Button(self.scrollable_frame, text="Print Config", 
                  command=lambda: print(len(self.img_processor.all_contours))).grid(row=22, column=1, pady=10)
        
        tk.Label(self.scrollable_frame, text='Actions: ').grid(row = 24, column=0)

        select_arc_1_button = tk.Button(self.scrollable_frame, text="Select Top Arc", 
                  command=lambda: self.get_line1())
        select_arc_1_button.grid(row=25, column=0, pady=10)
        select_arc_2_button = tk.Button(self.scrollable_frame, text="Select Bottom Arc", 
                  command=lambda: print('self.config', self.get_line1()))
        select_arc_2_button.grid(row=26, column=0, pady=10)
        select_line_1_button = tk.Button(self.scrollable_frame, text="Select Left Line", 
                  command=lambda: print('self.config', self.get_line1()))
        select_line_1_button.grid(row=27, column=0, pady=10)
        select_line_2_button = tk.Button(self.scrollable_frame, text="Select Right Line", 
                  command=lambda: print('self.config', self.get_line1()))
        select_line_2_button.grid(row=28, column=0, pady=10)


        
        return {
            'save_config_button': save_config_button,
            'show_contour_button': show_contour_button,
            'delete_config_button': delete_config_button,
            'print_config_button': print_config_button,
            'select_arc_1_button':select_arc_1_button,
            'select_arc_2_button':select_arc_2_button,
            'select_line_1_button':select_line_1_button,
            'select_line_2_button':select_line_2_button,
        }
    
    def load_left_frame_configuration_entries(self):
        if self.configuration_entries!= {}:
            for o, widget in self.configuration_entries.items():
                widget.destroy()

        def w(p):
            print("Validating:", repr(p))  # Use repr() to see empty strings
            try:
                isfloat = isinstance(float(p), float)
            except ValueError:
                isfloat = False
                
            return isfloat or p == '' or p == "-" or p[-1] == '.' or p == '-1'

        
        vcmd = self.register(w)     #validation
        for i, (key, value) in enumerate(
            {k:v for k, v in self.template_configuration.items() if k!= 'folder_name'}.items()):
            
            tk.Label(self.scrollable_frame, text=key).grid(row=i+1, column=0, padx = 10, pady = 5, sticky ='w')
            entry = Entry(self.scrollable_frame, validate='all', validatecommand=(vcmd, '%P'))
            entry.grid(row=i+1, column=1, padx=1, pady=5)
            entry.insert(0, str(value.get()))
            # self.configuration_entries[key] = entry.get()
        return 
    
    def load_left_frame_drop_down(self):
        options = get_template_list()
        tk.Label(self.scrollable_frame, text= 'Folder_Name').grid(row=0, column=0, padx = 10, pady = 5, sticky = 'w')
        dropdown = OptionMenu(self.scrollable_frame, self.selected_template_folder, *options if len(options)>0 else['Empty List Error'])
        dropdown.config(width=15)
        dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.selected_template_folder.trace_add("write", self.on_dropdown_select)
        return dropdown
    
    def load_left_frame(self):
        # Left frame scroll bar configuration
        left_frame = tk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights to allow resizing
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        canvas = Canvas(left_frame, bg = 'red')
        scrollbar = Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Update scroll region when the frame resizes
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Add the scrollable frame to the canvas
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))

        # Use grid layout with proper sticky values
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky="ns")

        return scrollable_frame


    def tk_configuration(self):
        #layout
        self.configure(borderwidth=2, relief="solid")

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)
    
    def on_dropdown_select(self, *args):
        selected_template_folder = self.selected_template_folder.get()
        new_config_key = get_config_csv_values(folder_name='folder_name')
        new_config_val = get_config_csv_values(folder_name=selected_template_folder)
        for k in range(len(new_config_key)):
            key = new_config_key[k]
            val = new_config_val[k]
            self.template_configuration[key].set(val)  
        self.load_left_frame_configuration_entries()

        self.img_processor.load_template(template_configuration={k:v.get() for k, v in self.template_configuration.items()})
        self.update_img_label()
    
    def save_config(self):
        self.get_template_configuration()
        template_configuration = {k:v.get() for k, v in self.template_configuration.items()}
        print('t: ',template_configuration)
        template_configuration = {'folder_name': self.selected_template_folder.get(), **template_configuration}
        show_confirmation(on_confirm=lambda:modify_config_data(template_configuration))
        
    def highlight_next_contour(self):
        if self.selected_contour_index.get() < len(self.img_processor.all_contours)-5:
            self.selected_contour_index.set(self.selected_contour_index.get()+5)
        print('get: ',self.selected_contour_index.get())    
        print(self.selected_contour_index.get())
    
    def highlight_prev_contour(self):
        if self.selected_contour_index.get() >-1:
            self.selected_contour_index.set(self.selected_contour_index.get() -1)
        print(self.selected_contour_index.get())

    
    def process_show_contour(self):
        #handle image
        self.img_processor.update_template_configuration(self.get_template_configuration())
        show_contour_state = self.img_processor.update_image_state('Display_Contour')['Display_Contour']
        new_img = self.img_processor.get_dispay_image()
        self.update_img_label(new_img = new_img)
        
        #hanle button
        self.left_frame_buttons['show_contour_button'].config(text = 'Hide Contour' if show_contour_state else 'Show Contour')
        self.left_frame_buttons['show_contour_button'].text = 'Hide Contour' if show_contour_state else 'Show Contour'
        # new_img = self.img_processor.get_display_image()
        
        self.contour_action_buttons['selected_contour_index_label'].config(text = '')
        self.update_contour_index_label()
        return
    
    def get_template_configuration(self, with_folder_name = True):
        self.template_configuration = {'folder_name': self.selected_template_folder.get(),**{k:v for (k,v) in self.configuration_entries.items()}}
        return self.template_configuration
    
    def load_template(self):

        return 
