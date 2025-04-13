# =======================================================================================
# util modules imported into fPhenix 2025 : Wheel Of Fortune
# Import functions
# =======================================================================================

import pygame
from setup.settings import *

from csv import reader
import re

from os import walk
from os.path import join
from pathlib import Path

# -----------------------------------------------------------------------------------
# Simply return a pygame (converted+alpha) surface from the image at fpath
def import_image(fpath, keepalpha= True):
    if keepalpha:
        return pygame.image.load(fpath).convert_alpha()
    else:
        return pygame.image.load(fpath).convert()
    #endif

# -----------------------------------------------------------------------------------
# Returns a list of surfaces from the files containes in the fpath directory
#
# Exemple: the ./assets/graphics/spin folder has the files 0.png, ... 3.png
#      particle_anims = import_folder(join('assets', 'graphics', 'spin'))
# will get a list of the 4 corresponding surfaces
def import_folder(fpath):
    surface_list = []

    for __folder_name, __sub_folders, img_files in walk(fpath):
        for image in img_files:
            full_image_name = join(fpath, image)
            image_surface = import_image(full_image_name)
            surface_list.append(image_surface)
        #endfor
    #endfor

    return surface_list

# -----------------------------------------------------------------------------------
# Returns a dictionary of key:value pairs with for each image file in the fpath directory:
#   * key: the base name of the image file;
#   * value: the surface for that image file.
#
# Exemple: the ./assets/graphics/terrain folder has the files: top.png, bottom.png, center.png
#      land_tiles = import_folder_dict(join('assets', 'graphics', 'terrain'))
# will get the collection: {'top': <Surface for top.png>, 'bottom": <Surface for bottom.png>, 'center': <Surface for center.png>}
def import_folder_dict(fpath):
    surface_dict = {}

    for __folder_name, __sub_folders, img_files in walk(fpath):
        for image in img_files:
            full_image_name = join(fpath, image)
            image_surface = import_image(full_image_name)
            basename = Path(image).stem  # or key = image.split('.')[0]  # remove the '.png'
            surface_dict[basename] = image_surface
        #endfor
    #endfor
    
    return surface_dict

# -----------------------------------------------------------------------------------
# Reads a cvs file and Returns a list of datadescribed in the cvs file.
#
# Exemple: terrain.csv is a csv file
#    import_csv_layout(CWD, 'terrain')
# would return a list of rows, each row being a list of (string) values corresponding
# to the database data
def import_csv_database(fpath, db):
    data = []
    path = join(fpath, 'dB', db + '.csv')
    with open(path) as csv_datafile:
        cvsdata = reader(csv_datafile, delimiter= ',')
        for row in cvsdata:
            category, puzzle = row
            if category == '' or puzzle == '':
                continue
            #endif
            puzzle_text = puzzle.upper()
            puzzle_text = re.sub('\s*;\s*', ', ', puzzle_text)
            puzzle_text = re.sub('\s*:\s*', ': ', puzzle_text) 
            data.append(list((category, puzzle_text)))
        #endfor
    #endwith open

    return data

# -----------------------------------------------------------------------------------
def import_avatars(fpath):
    avatars_path = join(fpath, 'assets', 'avatars')
    return import_folder_dict(avatars_path)

# -----------------------------------------------------------------------------------
def import_img(fpath, img):
    img_path = join(fpath, 'assets', 'images', img)
    return import_image(img_path)

# # -----------------------------------------------------------------------------------
# def import_audio(self, fpath):
#     audio_path = join(fpath, 'assets', 'audio')
#     audio = {
#         'music': {'sound': pygame.mixer.Sound(join(audio_path, 'Opening Theme from 2007.mp3')), 'volume': 0.2 * MUSIC_VOLUME}
#     }
#     for sound in audio.keys():
#         audio[sound]['sound'].set_volume(audio[sound]['volume'])
#     #endfor
    
#     return audio