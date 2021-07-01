# -*- coding: utf-8 -*-
import os
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#yamlファイルに定義されている運動の名前listを作成する関数
def read_exercise_name_list():
    file_path = os.path.join(BASE_DIR, 'exercise_info.yaml')
    with open(file_path, 'rb') as f:#yamlファイルを開く
        config = yaml.safe_load(f)
    
    name_list = []
    for dict_key in config:
        name_list.append(config[dict_key]['name'])
    return name_list

#yamlファイルをそのまま返す関数
def read_exercise_name():
    file_path = os.path.join(BASE_DIR, 'exercise_info.yaml')
    with open(file_path, 'rb') as f:#yamlファイルを開く
        config = yaml.safe_load(f)
    return config#yamlの中身をそのまま返す