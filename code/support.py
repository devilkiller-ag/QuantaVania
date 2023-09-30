#### IMPORTS
import pygame
from os import walk
from pygame.image import load as loadImage

def import_images_from_folder(path):
    surface_list = []

    for _folder_name, _sub_folders, file_names in walk(path):
        for file_name in file_names:
            full_path = path + '/' + file_name
            image_surface = loadImage(full_path)
            surface_list.append(image_surface)
    
    return surface_list

def import_images_from_folder_as_dict(path):
    surface_list = {}

    for _folder_name, _sub_folders, file_names in walk(path):
        for file_name in file_names:
            full_path = path + '/' + file_name
            image_surface = loadImage(full_path)
            surface_list[file_name.split('.')[0]] = image_surface # Get only file name as dictionary key without the file extension
    
    return surface_list