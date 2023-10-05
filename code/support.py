#### IMPORTS
from os import walk
from pygame.image import load as loadImage

from settings import *
from save_load_manager import SaveLoadSystem

def import_images_from_folder(path):
    surface_list = []

    for _folder_name, _sub_folders, file_names in walk(path):
        for file_name in file_names:
            full_path = path + '/' + file_name
            image_surface = loadImage(full_path).convert_alpha()
            surface_list.append(image_surface)
    
    return surface_list

def import_images_from_folder_as_dict(path):
    surface_list = {}

    for _folder_name, _sub_folders, file_names in walk(path):
        for file_name in file_names:
            full_path = path + '/' + file_name
            image_surface = loadImage(full_path).convert_alpha()
            surface_list[file_name.split('.')[0]] = image_surface # Get only file name as dictionary key without the file extension
    
    return surface_list

def import_levels(folder_name):
    saved_levels = {}
    node_positions = OVERWORLD_NODE_POSITIONS
    
    for _folder_name, _sub_folders, file_names in walk(folder_name):
        for index, file_name in enumerate(file_names):
            ## Save/Load Manager
            saveloadmanager = SaveLoadSystem(SAVE_FILE_EXTENSION, SAVE_FOLDER_NAME)
            loaded_level = saveloadmanager.load_data(file_name.split('.')[0])
            saved_levels[file_name.split('.')[0]] = {
                'data': loaded_level,
                'node_position': node_positions[index],
                'node_graphics': f'graphics/overworld/{index}',
                'unlock': index+1
            }
    
    return saved_levels