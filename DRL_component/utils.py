import numpy as np
from PIL import Image
import json

with open("settings.json", "r") as f:
    data = json.load(f)

def set_setting(setting_name:str, value)->None:
    global data
    data[setting_name]=value

def get_setting(setting_name:str):
    return data[setting_name]

def print_all_settings():
    for k in data:
        print(k+":",data[k])

def resize_img(img, to_width, to_height):
    return np.array(Image.fromarray(img).resize((to_width, to_height), Image.Resampling.NEAREST))