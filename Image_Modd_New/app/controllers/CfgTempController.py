
class CfgTempController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["cfg_template"]
        self.column_title = self.model.config_sheet.data_column_title 

        self._bind()

    def _bind(self):
        print('invoked')
        self.frame.home_button.config(command = lambda: self.view.switch("home"))
        self.populate_dropdown_options()
        # self.frame.image_button.config(command = self.select_image)
        # self.frame.new_template_button.config(command = self.new_template)
        pass
    
    def populate_dropdown_options(self):
        self.frame.template_list = self.model.config_sheet.data.keys()
        menu = self.frame.template_select_dropdown['menu']
        menu.delete(0, "end")
        for option in self.frame.template_list:
            menu.add_command(label=option, command=lambda value=option: self.frame.template_selected_var.set(value))
        self.frame.template_selected_var.set('Select Template')
        
        
    def populate_left_frame_labels(self):
        pass
