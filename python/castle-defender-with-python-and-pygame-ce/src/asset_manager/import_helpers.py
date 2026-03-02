from os import walk
from os.path import join
from settings import pygame


def import_folder_as_list(*path):
    frames = []

    for folder_path, _, image_names in walk(join(*path)):
        for image_name in sorted(image_names, key=lambda name: int(name.split(".")[0])):
            full_path = join(folder_path, image_name)
            surface = pygame.image.load(full_path).convert_alpha()
            frames.append(surface)

    return frames


def import_folder_as_dict(*path):
    frames_dict = {}

    for folder_path, _, image_names in walk(join(*path)):
        for image_name in image_names:
            full_path = join(folder_path, image_name)
            surface = pygame.image.load(full_path).convert_alpha()
            frames_dict[image_name.split(".")[0]] = surface

    return frames_dict


def import_subfolders_as_dict(*path):
    frames_dict = {}

    for _, subfolders, _ in walk(join(*path)):
        if subfolders:
            for subfolder in subfolders:
                frames_dict[subfolder] = import_folder_as_list(*path, subfolder)

    return frames_dict
