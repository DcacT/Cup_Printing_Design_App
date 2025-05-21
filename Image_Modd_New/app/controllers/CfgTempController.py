from tkinter import Label, Entry, StringVar, messagebox
class CfgTempController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["cfg_template"]
        self.column_titles = self.model.template_manager.column_titles
        self.template_selected_dict = {}

        self.refresh_template_selected_dict()
        self.populate_dropdown_options()
        self.populate_middle_frame_labels()

        
        self._bind()

    def _bind(self):
        self.frame.home_button.config(command=lambda: self.view.switch("home"))

        self.frame.delete_template_button.config(command=self.on_select_delete_template)
        self.frame.save_template_button.config(command=self.on_save_tempalte)
        self.frame.display_contour_checkbox.config(command=self.on_display_contour_checkbox)
        self.frame.update_image_button.config(command=self.on_select_update_image)

        self.frame.select_contour_button.config(command=self.on_contour_selected)
        self.frame.prev_prev_contour_button.config(command=lambda: self.on_next_or_prev_selected(go_next=False, count=5))
        self.frame.prev_contour_button.config(command=lambda: self.on_next_or_prev_selected(go_next=False, count=1))
        self.frame.next_contour_button.config(command=lambda: self.on_next_or_prev_selected(go_next=True, count=1))
        self.frame.next_next_contour_button.config(command=lambda: self.on_next_or_prev_selected(go_next=True, count=5))

        self.frame.display_border_checkbox.config(command=self.on_display_contour_checkbox)
        self.frame.generate_border_button.config(command=self.generate_border)

        self.frame.reset = self.populate_dropdown_options
        pass
    
    def refresh_template_selected_dict(self):

            folder_name = self.frame.template_selected_var.get()
            templates = self.model.template_manager.templates
            
            for key in self.column_titles:
                if key not in self.template_selected_dict.keys():
                    self.template_selected_dict[key] = StringVar()
                    
                if folder_name == 'Select Template':
                    val = -1
                else:
                    val = templates[folder_name][key] 
                    
                self.template_selected_dict[key].set(val)
                
    def generate_border(self):
        selected_border = self.frame.selected_action.get()
        if selected_border == 'No Action Selected':
            messagebox.showerror('Error','No Action Selected')
        else:
            contour_list = self.frame.contour_list[:-1] #omit -1
            if len(contour_list) <= 0:
                messagebox.showerror('Error','No Contour Selected')
            else:
                result = self.model.image_processor.generate_border(selected_border,contour_list)
                location = selected_border.split(' ')[0] 
                
                if location == 'Left':
                    self.template_selected_dict['Line_1_vx'].set(result[0]) 
                    self.template_selected_dict['Line_1_vy'].set(result[1]) 
                    self.template_selected_dict['Line_1_x0'].set(result[2]) 
                    self.template_selected_dict['Line_1_y0'].set(result[3]) 
                elif location == 'Right':
                    self.template_selected_dict['Line_2_vx'].set(result[0]) 
                    self.template_selected_dict['Line_2_vy'].set(result[1]) 
                    self.template_selected_dict['Line_2_x0'].set(result[2]) 
                    self.template_selected_dict['Line_2_y0'].set(result[3]) 
                elif location == 'Top':
                    self.template_selected_dict['Arc_1_x'].set(result[0]) 
                    self.template_selected_dict['Arc_1_y'].set(result[1]) 
                    self.template_selected_dict['Arc_1_r'].set(result[2]) 
                elif location == 'Bottom':
                    self.template_selected_dict['Arc_2_x'].set(result[0]) 
                    self.template_selected_dict['Arc_2_y'].set(result[1]) 
                    self.template_selected_dict['Arc_2_r'].set(result[2]) 
        
    def on_contour_selected(self):
        selected_contour_id = self.frame.selected_contour_id.get()
        menu = self.frame.contour_select_dropdown['menu']
        menu.delete(0, "end")
    
        if selected_contour_id != -1:
            try:
                idx = self.frame.contour_list.index(selected_contour_id)
                del self.frame.contour_list[idx]
            except ValueError:
                self.frame.contour_list = [selected_contour_id]+ self.frame.contour_list    

                    
        for option in self.frame.contour_list:
            menu.add_command(label=option, command=lambda value=option: self.on_contour_drop_down_selected(value))
        
    def on_contour_drop_down_selected(self, val):
        self.frame.selected_contour_id.set(val)
        self.refresh_img_label()
        
    def populate_dropdown_options(self):
        self.frame.template_list = self.model.template_manager.templates.keys()
        menu = self.frame.template_select_dropdown['menu']
        menu.delete(0, "end")
        
        for option in self.frame.template_list:
            menu.add_command(label=option, command=lambda value=option: self.on_template_selected(value))
        
        self.frame.template_selected_var.set('Select Template')
    
    def on_next_or_prev_selected(self, go_next = True, count = 1):
        selected_contour_id = self.frame.selected_contour_id.get()
        step = count if go_next else count * -1
        out_of_range = selected_contour_id + step < -1 or selected_contour_id + step >= len(self.model.image_processor.all_contours)
        result_contour_id = selected_contour_id + step if not out_of_range else selected_contour_id
        self.frame.selected_contour_id.set(result_contour_id)
        self.refresh_img_label()

    
    def on_select_update_image(self):
        data = { k:v.get() for k, v in self.template_selected_dict.items()}
        self.model.image_processor.load_template(template_data = data)
        len_of_all_contours = len(self.model.image_processor.all_contours)
        self.frame.total_contour_count_var.set(f'/0 - {len_of_all_contours -1}')
        self.on_display_contour_checkbox()

        
    def on_display_contour_checkbox(self):
        self.refresh_img_label()
          
    def on_save_tempalte(self):
        folder_name = self.frame.template_selected_var.get()
        if folder_name == 'Select Template':
            messagebox.showerror('Error', 'Template not selected')
        
        confirm = messagebox.askokcancel('Save Template Confirmation', f'Are you sure about saving template {folder_name}')
        
        if confirm:
            data = { k:v.get() for k, v in self.template_selected_dict.items()}
            self.model.template_manager.update_template(data)

    def on_select_delete_template(self):
        folder_name = self.frame.template_selected_var.get()
        if folder_name == 'Select Template':
            messagebox.showerror('Error', 'Select Template to Delete')

        confirm = messagebox.askokcancel('Delete Template Confirmation', f'Are you sure about deleting template {folder_name}')

        if confirm:
            self.model.template_manager.delete_template(self.frame.template_selected_var.get())
            
            self.populate_dropdown_options()

        # self.populate_dropdown_options()
        # self.refresh_template_selected_dict()
        
    def on_template_selected(self, val):
        self.frame.template_selected_var.set(val)
        self.refresh_template_selected_dict()
        self.model.image_processor.load_template(template_name = val)
        len_of_all_contours = len(self.model.image_processor.all_contours)
        self.frame.total_contour_count_var.set(f'/0 - {len_of_all_contours -1}')
        self.load_image()
        
        

        
    def populate_middle_frame_labels(self):
        for row_id, key in enumerate(self.template_selected_dict.keys()):
            
            Label(self.frame.scrollable_frame,text=key ).grid(row=row_id, column=0)
            entry = Entry(self.frame.scrollable_frame ,textvariable= self.template_selected_dict[key] )
            entry.grid(row = row_id, column= 1)
            
            self.frame.scrollable_frame_content[key] = entry
            
            
        pass

    def load_image(self):
        img_tk = self.model.image_processor.get_display_image()
        self.frame.img_label.config(image=img_tk)
        self.frame.img_label.image = img_tk
    
    
    def refresh_img_label(self):
        
        self.model.image_processor.display_contours(
            target_contour= self.frame.selected_contour_id.get(), 
            highlight_contour_list = self.frame.contour_list[:-1], #omit -1
            display = self.frame.display_contour_status.get())
        self.model.image_processor.display_border(
            display = self.frame.display_border_status.get())
        self.load_image()
