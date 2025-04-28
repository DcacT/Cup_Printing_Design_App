import csv
import os
import re
from PIL import Image

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

class ConfigSheet:
    def __init__(self):
        self.sheet_path = self.get_sheet_path()
        self.data_rows = self.read_rows()
        self.data_column_title = self.get_data_column_title()
        self.data = self.get_data_from_rows()
        pass
    
    def get_sheet_path(self):
        self_path = os.path.dirname(os.path.realpath(__file__))
        
        return os.path.join(self_path, '../../data/templates/config.csv')

    
    def get_data_column_title(self):
        return self.data_rows[0]

    def get_data_from_rows(self):

        data = {}
        print('self.data_rows', self.data_rows)
        for row in self.data_rows[1:]:
            data[row[0]] = {}
            for idx, val in enumerate(row):
                data[row[0]][self.data_column_title[idx]] = val
        print(data)
        return data
    
    def read_rows(self, folder_name = None):
        '''
        if folder_name not None: return row with corresponding folder_name , unless
        if folder_name not None but not found: return None
        if folder_name is None: return everything
        '''

        rows = []
        with open(self.sheet_path) as file:
            spamreader = csv.reader(file)
            
            for row in spamreader:
                rows.append(row)
                if row[0] == folder_name:
                    return row
                
        print('rows:', rows)
        if folder_name == None:
            return rows
        return None
    
    def write_rows(self, update_row = None, delete = False, new = False):
        print('write')
        with open(self.sheet_path, 'w', newline= '') as f:
            writer = csv.writer(f)
            if update_row == None:
                new_rows = self.data_rows
            else:
                new_rows = [self.data_rows[0]] if not new else [self.data_rows[0], update_row]

                for row in self.data_rows[1:]:

                    if row[0] == update_row[0]:                            
                        row = update_row
                        if not delete:
                            new_rows.append(row)
                    else:
                        new_rows.append(row)
                        
            writer.writerows(new_rows)
            
        self.data_rows = self.read_rows()
        self.data = self.get_data_from_rows()

    def new_template(self, folder_name:str , image_path:str):
        #update_sheet
        new_row = [folder_name]
        for i in self.data_column_title[1:]:
            new_row.append(-1)
        self.write_rows(update_row=new_row, new=True)


        #new_dir
        p = os.path.dirname(self.sheet_path)
        folder_name =os.path.join(p,folder_name)
        os.makedirs(folder_name)        
        
        #save_image
        new_image_path = os.path.join(folder_name, 'template_image.png')
        img = Image.open(image_path)
        img = img.save(new_image_path)
        
    def modify_template(self, data):
        print('modify : ', data.values())
        self.write_rows(update_row= [i for i in data.values()])

    def delete_template(self, folder_name):
        print('delete ', folder_name)
        self.write_rows(update_row= [folder_name], delete=True)
        self_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(self_path, '../../data/templates/', folder_name,'template_image.png' )
        os.remove(path)
        path = os.path.join(self_path, '../../data/templates/', folder_name)
        os.rmdir(path)

        
        
        pass

    def verify(self, folder_name):
        
        if folder_name in self.data :
            return False
        banned_words = ['folder_name', '']    
        if folder_name in banned_words:
            return False
        if not is_valid_windows_directory_name(folder_name):
            return False
        return True 

#for debug only
if __name__ == "__main__":
    c = ConfigSheet()
