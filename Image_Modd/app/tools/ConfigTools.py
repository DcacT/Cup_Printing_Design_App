import os
import csv
from tkinter import messagebox
import shutil


get_tools_dir_path = lambda: os.path.dirname(os.path.realpath(__file__))
get_config_dir_path = lambda: os.path.join(get_tools_dir_path(), '../../Templates')
get_config_file_path = lambda: os.path.join(get_config_dir_path(), 'config.csv')

def get_config_csv_values(folder_name = None):
    rows = []
    with open(get_config_file_path()) as file:
        spamreader = csv.reader(file)
        
        for row in spamreader:
            rows.append(row)
            if row[0] == folder_name:
                return row
            
    if folder_name == None:
        return rows
    return None

def get_template_list():    
    
    return [row[0] for row in get_config_csv_values()[1:]]

def translate_config_obj_to_row(config_obj):
    return [v for (k,v) in config_obj.items()]

def modify_config_data(new_config_obj, delete_row = False):
    rows = get_config_csv_values()
    new_rows = []
    print(new_config_obj)
    new_row = translate_config_obj_to_row(new_config_obj)
    print(new_row, delete_row)
    for row in rows:
        if row[0] != new_row[0]:
            new_rows.append(row)
        else:
            if delete_row ==False:
                new_rows.append(new_row)
            else:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                template_dir_path = os.path.join(dir_path, '../Templates', new_row[0])
                if os.path.exists(template_dir_path):
                    shutil.rmtree(template_dir_path) 

    
    write_to_config(new_rows=new_rows)


def write_to_config(new_rows):
    print(get_config_file_path())
    with open(get_config_file_path(), 'w', newline= '') as f:
        writer = csv.writer(f)
        a = writer.writerows(new_rows)
        print(a)

def show_confirmation(on_confirm=None, on_cancel=None, Action = 'Save'):
    # Show a confirmation popup
    response = messagebox.askyesno(f"Confirm {Action}", f"Are you sure you want to {str(Action).lower()}?")
    
    if response:
        if on_confirm:
            on_confirm()
    else:
        if on_cancel:
            on_cancel()
           