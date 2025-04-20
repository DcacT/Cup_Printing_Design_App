from .ConfigSheet import ConfigSheet
default_tempalte = {
    'folder_name':'',
    'PX_Min':-1, #Pixel Count 
    'PX_Max':-1, 
    'Horizontal_Limit':-1, #Aspect Ratio
    'Vertical_Limit':-1,
    
    'Line_1_vx':-1,  #line1
    'Line_1_vy':-1,
    'Line_1_x0':-1,
    'Line_1_y0':-1,

    'Line_2_vx':-1, #line2
    'Line_2_vy':-1,
    'Line_2_x0':-1,
    'Line_2_y0':-1,
    
    'Arc_1_x':-1, #arc1
    'Arc_1_y':-1,
    'Arc_1_r':-1,
    
    'Arc_2_x':-1, #arc2
    'Arc_2_y':-1,
    'Arc_2_r':-1,                
}

class Template:
    def __init__(self, data_row):
        



        pass