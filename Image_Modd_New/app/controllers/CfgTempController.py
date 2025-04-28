from tkinter import Label, Entry, StringVar, messagebox
class CfgTempController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["cfg_template"]
        self.column_titles = self.model.config_sheet.data_column_title
        self.template_selected_dict = {}

        self.refresh_template_selected_dict()
        self.populate_dropdown_options()
        self.populate_middle_frame_labels()

        
        self._bind()

    def _bind(self):
        self.frame.home_button.config(command = lambda: self.view.switch("home"))
        self.frame.delete_template_button.config(command = lambda:self.on_select_delete_template())
        self.frame.save_template_button.config(command = lambda:self.on_save_tempalte())
        

        self.frame.reset = self.populate_dropdown_options
        pass

    def on_save_tempalte(self):
        folder_name = self.frame.template_selected_var.get()
        if folder_name == 'Select Template':
            messagebox.showerror('Error', 'Template not selected')
        
        confirm = messagebox.askokcancel('Save Template Confirmation', f'Are you sure about saving template {folder_name}')
        data = { k:v.get() for k, v in self.template_selected_dict.items()}
        self.model.config_sheet.modify_template(data)

    def on_select_delete_template(self):
        folder_name = self.frame.template_selected_var.get()
        if folder_name == 'Select Template':
            messagebox.showerror('Error', 'Select Template to Delete')

        confirm = messagebox.askokcancel('Delete Template Confirmation', f'Are you sure about deleting template {folder_name}')

        if confirm:
            self.model.config_sheet.delete_template(self.frame.template_selected_var.get())
            
            self.populate_dropdown_options()

        # self.populate_dropdown_options()
        # self.refresh_template_selected_dict()



    
    def populate_dropdown_options(self):
        print('update')
        self.frame.template_list = self.model.config_sheet.data.keys()
        menu = self.frame.template_select_dropdown['menu']
        menu.delete(0, "end")
        
        for option in self.frame.template_list:
            menu.add_command(label=option, command=lambda value=option: self.on_template_selected(value))
        
        self.frame.template_selected_var.set('Select Template')
        
    def on_template_selected(self, val):
        self.frame.template_selected_var.set(val)
        self.refresh_template_selected_dict()
        
    def refresh_template_selected_dict(self):

        folder_name = self.frame.template_selected_var.get()
        data = self.model.config_sheet.data
        
        for key in self.column_titles:
            if key not in self.template_selected_dict.keys():
                self.template_selected_dict[key] = StringVar()
                
            if folder_name == 'Select Template':
                val = -1
            else:
                val = data[folder_name][key] 
                
            self.template_selected_dict[key].set(val)
        
    def populate_middle_frame_labels(self):
        for row_id, key in enumerate(self.template_selected_dict.keys()):
            
            Label(self.frame.scrollable_frame,text=key ).grid(row=row_id, column=0)
            entry = Entry(self.frame.scrollable_frame ,textvariable= self.template_selected_dict[key] )
            entry.grid(row = row_id, column= 1)
            
            self.frame.scrollable_frame_content[key] = entry
            
            
        pass
