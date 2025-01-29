"""Configuration options and functions for interacting with the configuration file are contained within this module."""

import sys
import os
from getpass import getuser
from typing import Tuple, List
from .pyqt import Qt
from .widget import DefaultDialog

SAVE_DIR = os.path.expanduser('~')
USER = getuser() 
IMAGE_DIR = None
GROUP_NAMES = ['None','1','2','3','4','5','6','7','8','9']
CATEGORY_NAMES = ['None','1','2','3','4','5']
GROUP_MAX = ['None','None','None','None','None','None','None','None','None']
RANDOMIZE_ORDER = True

MARK_KEYBINDS = {1: {Qt.MouseButton.LeftButton,Qt.Key.Key_1}, 
            2: {Qt.Key.Key_2}, 
            3: {Qt.Key.Key_3}, 
            4: {Qt.Key.Key_4}, 
            5: {Qt.Key.Key_5}, 
            6: {Qt.Key.Key_6}, 
            7: {Qt.Key.Key_7}, 
            8: {Qt.Key.Key_8}, 
            9: {Qt.Key.Key_9}}
        

def path():
    return os.path.join(SAVE_DIR,f'{USER}_config.txt')
    
def read() -> Tuple[str,List[str],List[str],List[str],List[int]]:
    """
    Reads in each line from imgmarker.cfg. If there is no configuration file,
    a default configuration file will be created using the required text
    format.

    Returns
    ----------
    image_dir: str
        Directory containing desired image files.

    group_names: list[str]
        A list of containing labels for each mark button.

    category_names: list[str]
        A list containing labels for each image category.

    group_max: list[int]
        A list containing the maximum allowed number of marks for each group.
    """

    # If the config doesn't exist, create one
    if not os.path.exists(path()):
        with open(path(),'w') as config:
            image_dir = None
            group_names = ['None','1','2','3','4','5','6','7','8','9']
            category_names = ['None','1','2','3','4','5']
            group_max = ['None','None','None','None','None','None','None','None','None']
            randomize_order = True

            config.write(f'image_dir = {image_dir}\n')
            config.write(f"groups = {','.join(group_names)}\n")
            config.write(f"categories = {','.join(category_names)}\n")
            config.write(f"group_max = {','.join(group_max)}\n")
            config.write(f'randomize_order = {randomize_order}')  

    else:
        for l in open(path()):
            var, val = [i.strip() for i in l.replace('\n','').split('=')]

            if var == 'image_dir':
                if val == './': image_dir = os.getcwd()
                else: image_dir = val
                image_dir =  os.path.join(image_dir,'')

            if var == 'groups':
                group_names = []
                group_names_temp = val.split(',')
                for group_name in group_names_temp:
                    group_names.append(group_name.strip())
                group_names.insert(0, 'None')

            if var == 'categories':
                category_names = []
                category_names_temp = val.split(',')
                for category_name in category_names_temp:
                    category_names.append(category_name.strip())
                category_names.insert(0, 'None')
            
            if var == 'group_max':
                group_max = []
                group_max_temp = val.split(',')
                for group_max_val in group_max_temp:
                    group_max.append(group_max_val.strip())

            if var == 'randomize_order':
                randomize_order = val == 'True'

    return image_dir, group_names, category_names, group_max, randomize_order

def open_save() -> str:
    dialog = DefaultDialog()
    dialog.setWindowTitle("Open save directory")
    dialog.exec()
    if dialog.closed: sys.exit()

    save_dir = dialog.selectedFiles()[0]
    return save_dir

def open_ims() -> str:
    dialog = DefaultDialog(SAVE_DIR)
    dialog.setWindowTitle("Open image directory")
    dialog.exec()
    if dialog.closed: sys.exit()

    image_dir = dialog.selectedFiles()[0]
    return image_dir

def update() -> None:
    """Updates any of the config variables with the corresponding parameter."""
    
    with open(path(),'w') as config:
        config.write(f'image_dir = {IMAGE_DIR}\n')
        config.write(f"groups = {','.join(GROUP_NAMES[1:])}\n")
        config.write(f"categories = {','.join(CATEGORY_NAMES[1:])}\n")
        config.write(f"group_max = {','.join(GROUP_MAX)}\n")
        config.write(f'randomize_order = {RANDOMIZE_ORDER}')