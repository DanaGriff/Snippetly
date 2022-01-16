import sys
import os
import json
from shutil import copyfile

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
    json_data = ''
    data_path = full_path('', 'data.json')
    if os.path.exists(data_path):
        with open(data_path) as database_file:
            try:
                json_data = json.load(database_file)
            except ValueError:
                database_file.close()
                print('The JSON File is corrupted')
                os.replace(data_path, data_path.replace('data.json', 'data_backup.json'))
                json_data = create_new_db_file()
    else:
       json_data = create_new_db_file()
    
    return json_data

def save_to_db(data):
    data_path = full_path('', 'data.json')
    with open(data_path, 'w') as database_file:
        json.dump(data, database_file)

def get_hotkeys_dict(data):
    hotkeysMap = {}

    for hotkey_i in data["hotkeys"]:
        hotkey = hotkey_i["hotkey"]
        text_to_copy = hotkey_i["text"]

        hotkeysMap[hotkey] = text_to_copy

    return hotkeysMap

def create_new_db_file():
    data_path = full_path('', 'data.json')
    database_file = open(data_path, "x")
    data = json.loads('{"hotkeys": []}')
    save_to_db(data)

    return data