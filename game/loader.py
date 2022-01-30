import pathlib
import pygame
import sys
from pathlib import Path


def get_list_of_images(path_to_folder, scale=1):
    """
    returns list of images loaded by pygame
    """
    path = Path(path_to_folder)
    img_list = []
    for img in path.iterdir():
        if img.is_file():
            if img.suffix == '.png' or img.suffix == '.jpg' or img.suffix == '.jpg':
                loaded_image = pygame.image.load(img)
                loaded_image = pygame.transform.scale(loaded_image, (int(loaded_image.get_width() * scale), int(loaded_image.get_height() * scale))).convert_alpha()
                img_list.append(loaded_image)
        
    return img_list


def get_folders(path):
    """
    returns a list with folder names in directory specified by path
    """
    path = Path(path)
    directories = []
    for dir in path.iterdir():
        if dir.is_dir():
            directories.append(dir)

    return directories


def scrapp_images(path, scale=1):
    """
    to get ready to use animation actions, scrapp folder "player" with folder tree as below:
          player/Idle/images
                /Run/images
                /Jump/images
                /Death/images

    then you will get dictionary with key: "idle" and value: list of images
    """
    path = Path(path)
    tree = {}
    for dir in path.iterdir():
        image_list = []
        if dir.is_dir():
            image_list += get_list_of_images(dir, scale=scale)

        tree[dir.name.lower()] = image_list

    return tree


def load_tiles(path, scale=1):
    path = Path(path)
    tiles = []
    for dir in path.iterdir():
        if dir.is_file():
            if dir.suffix == '.png' or dir.suffix == '.jpg' or dir.suffix == '.jpg':
                loaded_image = pygame.image.load(dir)
                loaded_image = pygame.transform.scale(loaded_image, (int(loaded_image.get_width() * scale), int(loaded_image.get_height() * scale))).convert_alpha()
                tiles.append(loaded_image)

    return tiles


def get_animations_from_sprite_sheet(path_to_spritesheet: str, actions_dict: dict, scale=1, start_point=(0, 0), left_marigin=0, right_marigin=0, top_marigin=0, bottom_marigin=0, frame_width=0, frame_height=0):
    """
    path_to_spritesheet - 'path to image with sprite sheet',
    actions_dict - {'animation_name':num_of_frames_in_animation},
    frame_width - width of rectangle created from this sprite sheet's frame,
    frame_height - height of rectangle created from this sprite sheet's frame, 
    start_point - modify this to for example set character in the center of rectangle,
    marigin - offset to the left/right/top/bottom of the spritesheet's images,
    returns: dict of structure "animation name": [list, of, images]
    """
    spritesheet = pygame.image.load(Path(path_to_spritesheet)).convert_alpha()
    max_frames_in_row = max(actions_dict.values())
    # print('max frames in row:', max_frames_in_row)
    num_of_animations = len(actions_dict)
    # print('num_of_animations:', num_of_animations)
    # print('sprite sheet width:', spritesheet.get_width())
    # print('sprite sheet height:', spritesheet.get_height())
    if frame_width == 0:
        frame_width = (spritesheet.get_width() - left_marigin - right_marigin) // max_frames_in_row
    if frame_height == 0:
        frame_height = (spritesheet.get_height() - top_marigin - bottom_marigin) // num_of_animations
    cutting_frame_width = (spritesheet.get_width() - left_marigin - right_marigin) // max_frames_in_row
    cutting_frame_height = (spritesheet.get_height() - top_marigin - bottom_marigin) // num_of_animations
    frames_x_offset = (spritesheet.get_width() - left_marigin - right_marigin) // max_frames_in_row - frame_width
    frames_y_offset = (spritesheet.get_height() - top_marigin - bottom_marigin) // num_of_animations - frame_height
    # print("frame_width", frame_width, "\nframe_height", frame_height)
    dict_of_animation_lists = {}
    row_index = 0
    for animation_name, num_of_frames in actions_dict.items():
        # create list of images
        one_animation_list = []
        for frame_num in range(num_of_frames):
            img = pygame.Surface((frame_width, frame_height), flags=pygame.SRCALPHA)
            # blit(source, xy_of_destination_in_img, (fragment))
            img.blit(spritesheet, 
                    start_point, 
                    (left_marigin + frame_num * (frame_width + frames_x_offset),
                    top_marigin + row_index * (frame_height + frames_y_offset),
                    (cutting_frame_width),
                    (cutting_frame_height)))
            
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))).convert_alpha()
            one_animation_list.append(img)
        
        dict_of_animation_lists[animation_name] = one_animation_list

        row_index += 1

    # x_check_sum = left_marigin + right_marigin + max_frames_in_row * frame_width
    # y_check_sum = top_marigin + bottom_marigin + num_of_animations * frame_height

    return dict_of_animation_lists




if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[1] == 'images':
            print(get_list_of_images(sys.argv[2]))
        elif sys.argv[1] == 'folders': 
            print(get_folders(sys.argv[2]))
        elif sys.argv[1] == 'scrapp':   
            print(scrapp_images(sys.argv[2]))

    else:
        print('as an argument provide method and path to folder with images')