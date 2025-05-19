from ..sql.sql_helper import sql
import os 
from PIL import Image
import re

class TemplateManager:
    def __init__(self):
        self.column_titles = []
        self.templates = {}
        self.refresh()
        
    def refresh(self):
        self.column_titles = self.get_column_title()
        self.templates = self.get_all_tempaltes()
        
    def get_all_tempaltes(self):
        msg = """
        SELECT * FROM templates
        """
        res = sql(msg)
        data = {}
        for row in res:
            data[row[0]] = {} 
            for idx, val in enumerate(row):
                data[row[0]][self.column_titles[idx]] = val
        print(data)
        return data
            
    def get_column_title(self):
        msg = """
        PRAGMA table_info(templates);

        """
        res = sql(msg)
        return [row[1] for row in res]
        
    def new_template(self, folder_name, image_path):
        #sql
        msg = f"""
        INSERT INTO templates VALUES({','.join([f"'{folder_name}'"] + ['-1'] * (len(self.column_titles) - 1))})
        """
        res = sql(msg)
        #dir
        self_path = os.path.dirname(os.path.realpath(__file__))
        folder_name =os.path.join( self_path,'../../data/templates/',folder_name)
        os.makedirs(folder_name, exist_ok=True)    
        #img
        new_image_path = os.path.join(folder_name, 'template_image.png')
        img = Image.open(image_path)
        img = img.save(new_image_path)
        self.refresh()

    def update_template(self, val):
        
        if isinstance(val, dict):
            val = list(val.values())
        print(val)
        folder_name = val[0]
        msg = f"""
        UPDATE templates
        SET {','.join(map(lambda idx: self.column_titles[idx + 1] + ' = ' + str(val[idx + 1]), range(len(self.column_titles)- 1)))}
        WHERE folder_name = '{folder_name}'
        """
        sql(msg)
        self.refresh()

    def delete_template(self, val):
        if isinstance(val, dict):
            val = val.values
        if isinstance(val, list):
            folder_name = val[0]
        folder_name = val
        #sql
        msg = f"""
        DELETE FROM templates WHERE folder_name = '{folder_name}'
        """
        sql(msg)
        #img
        self_path = os.path.dirname(os.path.realpath(__file__))
        image_path =os.path.join( self_path,'../../data/templates/',folder_name, 'template_image.png')
        os.remove(image_path)
        folder_path =os.path.join( self_path,'../../data/templates/',folder_name)
        os.rmdir(folder_path)        
        self.refresh()

        
    def verify(self, folder_name):
        banned_words = ['folder_name', '']    
        if folder_name in banned_words:
            return False
        if not is_valid_windows_directory_name(folder_name):
            return False
        msg = f"""
        SELECT * FROM templates WHERE folder_name = '{folder_name}'
        """
        res = sql(msg)
        print('len:',len(res))
        if len(res) != 0: 
            return False
        return True
        
    def test(self):

        self.new_template('8oz_standard',r'C:\Users\steve\Documents\Projects\Cup_Printing\Cup_Printing_Design_App\Image_Modd\Templates\8oz_standard\template_image.png')
        self.update_template(['8oz_standard',99,50,0.5,2,0.33704125455447603,0.941439858504704,76.46071216038295,633.0955418178013,-1,-1,-1,-1,-1,-1,-1,799,2597,1703])
        pass

def is_valid_windows_directory_name(name: str) -> bool:
    if not name or len(name) > 255:
        return False

    # Check for invalid characters
    if re.search(r'[<>:"/\\|?*]', name):
        return False

    # Reserved names (case-insensitive)
    reserved = {
        "CON", "PRN", "AUX", "NUL",
        *["COM" + str(i) for i in range(1, 10)],
        *["LPT" + str(i) for i in range(1, 10)]
    }
    name_upper = name.upper().split('.')[0]  # Remove extension if any
    if name_upper in reserved:
        return False

    # No trailing space or period
    if name[-1] in {' ', '.'}:
        return False

    return True