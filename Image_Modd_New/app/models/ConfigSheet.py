import csv
import os


class ConfigSheet:
    def __init__(self):
        self.sheet_path = self.get_sheet_path()
        self.data_rows = []
        self.data_rows = self.read_rows()
        pass
    
    def get_sheet_path(self):
        self_path = os.path.dirname(os.path.realpath(__file__))
        
        return os.path.join(self_path, '../../data/templates/config.csv')

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
                
        if folder_name == None:
            return rows
        return None
    
    def write_rows(self, update_row = None, delete = False):
        
        with open(self.sheet_path, 'w', newline= '') as f:
            writer = csv.writer(f)
            if update_row == None:
                new_rows = self.data_rows
            else:
                new_rows = []
                for row in self.data_rows:
                    if update_row[0] == row[0]:
                        row = update_row  
                        update_row = None
                    if not delete:
                        new_rows.append(row)

                if update_row is not None and not delete:
                    new_rows.append(update_row)

            writer.writerows(new_rows)

    def get_template_list(self):
        return [row[0] for row in self.data_rows[1:]]


if __name__ == "__main__":
    c = ConfigSheet()
    print(c.data_rows)