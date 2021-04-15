#!/usr/bin/env python3
from os import listdir, makedirs, remove
from os.path import isfile, join, splitext, basename, exists
from PIL import Image
from resizeimage import resizeimage, imageexceptions
from termcolor import colored


def check_folder_forjpg():
    onlyjpgfiles = [f for f in listdir() if isfile(join(".", f)) and f.endswith(".jpg")]
    return onlyjpgfiles


def check_folder_forpng():
    onlypngfiles = [f for f in listdir() if isfile(join(".", f)) and f.endswith(".png")]
    return onlypngfiles


def convert_to_png(jpg_list):
    for image in jpg_list:
        conv = Image.open(image)
        conv.save(splitext(basename(image))[0] + '.png')


def save_files(cover, image_path, image):
    directory = "Results"
    if not exists(directory):
        makedirs(directory)
    cover.save(directory + '/' + splitext(basename(image_path))[0] + '.png', image.format)


def resize_image(images_list):
    for image_file in images_list:
        with open(image_file, 'r+b') as f:
            with Image.open(f) as image:
                try:
                    cover = resizeimage.resize_height(image, 512)
                    save_files(cover, image_file, image)
                except imageexceptions.ImageSizeError:
                    print(colored(f"Image {image_file} is too small to be resized!", 'red'))


def remove_temp_files(png_trash):
    for elem in png_trash:
        remove(elem)


if __name__ == '__main__':
    jpgs = check_folder_forjpg()
    old_pngs = check_folder_forpng()
    if len(jpgs) > 0 or len(old_pngs) > 0:
        print(f"The following images will be converted and resized: {jpgs}")
        print(f"The following images will be resized only: {old_pngs}")
        if input(colored("Are you sure you want to continue?", 'green') + " [y,N] ").lower() == 'y':
            convert_to_png(jpgs)
            pngs = check_folder_forpng()
            only_new_pngs = [elem for elem in pngs if elem not in old_pngs]
            resize_image(pngs)
            remove_temp_files(only_new_pngs)
            print(colored("Done! You will find all your resized images in the Results folder.", 'green'))
        else:
            print(colored("Operation aborted.", 'yellow'))
    else:
        print(colored("There are no available pictures to convert or resize in this folder.", 'red'))
