#!/usr/bin/env python3
from os import listdir
from os.path import isfile, join, splitext, basename
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


def resize_image(images_list):
    for image_file in images_list:
        with open(image_file, 'r+b') as f:
            with Image.open(f) as image:
                try:
                    cover = resizeimage.resize_height(image, 512)
                    cover.save(splitext(basename(image_file))[0] + '.png', image.format)
                except imageexceptions.ImageSizeError:
                    print(colored(f"Image {image_file} is too small to be converted!", 'red'))


if __name__ == '__main__':
    jpgs = check_folder_forjpg()
    print(f"The following images will be converted and resized: {jpgs}")
    if input(colored("Are you sure you want to continue?", 'green') + " [y,N] ").lower() == 'y':
        convert_to_png(jpgs)
        pngs = check_folder_forpng()
        resize_image(pngs)
    else:
        print(colored("Operation aborted.", 'yellow'))
