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

def get_snippets_dict(data):
    snippetsMap = {}

    for snippet_i in data["snippets"]:
        snippet = snippet_i["snippet"]
        text_to_copy = snippet_i["text"]

        snippetsMap[snippet] = text_to_copy

    return snippetsMap

def create_new_db_file():
    data_path = full_path('', 'data.json')
    open(data_path, "x")
    data = json.loads('{"snippets": []}')
    save_to_db(data)

    return data

def save_snippets_to_db(data, snippetsMap):
    data['snippets'] = []
    for key, value in snippetsMap.items():
        attribute = { 'snippet' : key, 'text' : value}
        data['snippets'].append(attribute)

    save_to_db(data)