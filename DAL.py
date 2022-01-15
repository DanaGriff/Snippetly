import sys
import os
import json

def full_path(sub_folder, file_name):
    if getattr(sys, 'frozen', False):  # running in a bundle
        if len(sub_folder) > 0:
            dir_path = os.path.join(os.path.dirname(sys.executable), sub_folder)
        else:
            dir_path = os.path.dirname(sys.executable)
        return os.path.join(dir_path, file_name)
    else:  # running live
        if len(sub_folder) > 0: 
            dir_path = os.path.join(os.path.dirname(__file__), sub_folder)
        else:
            dir_path = os.path.dirname(__file__)
        return os.path.join(dir_path, file_name)

def retrieve_db():
    with open(full_path('', 'data.json')) as database_file:
        try:
            json_data = json.load(database_file)
            return json_data
        except ValueError:
            print('The JSON File is missing or corrupted')
            sys.exit()

def save_to_db(data):
    with open(full_path('', 'data.json'), 'w') as database_file:
        json.dump(data, database_file)       