#!/usr/bin/env python3
import threading
from os import listdir, makedirs, remove
from os.path import isfile, join, splitext, basename, exists
from PIL import Image
from resizeimage import resizeimage, imageexceptions
from termcolor import colored


def divide_in_chunks(ls, n):
    n = max(1, n)
    return (ls[i:i + n] for i in range(0, len(ls), n))


def check_folder_forjpg():
    onlyjpgfiles = [f for f in listdir() if isfile(join(".", f)) and f.endswith(".jpg")]
    return onlyjpgfiles


def check_folder_forpng():
    onlypngfiles = [f for f in listdir() if isfile(join(".", f)) and f.endswith(".png")]
    return onlypngfiles


def retrieve_images():
    return check_folder_forpng(), check_folder_forjpg()


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
                    width, height = image.size
                    if height >= width:
                        cover = resizeimage.resize_height(image, 512)
                    else:
                        cover = resizeimage.resize_width(image, 512)
                    save_files(cover, image_file, image)
                except imageexceptions.ImageSizeError:
                    print(colored(f"Image {image_file} is too small to be resized!", 'red'))


def remove_temp_files(png_trash):
    for elem in png_trash:
        remove(elem)


def multithreaded_resizer(image_list):
    lists = divide_in_chunks(image_list, 3)
    for sublist in lists:
        tn = threading.Thread(target=resize_image, args=(sublist,))
        tn.start()
        tn.join()


if __name__ == '__main__':
    old_pngs, jpgs = retrieve_images()
    if len(jpgs) > 0 or len(old_pngs) > 0:
        print(colored(f"The following images will be converted and resized: {jpgs}", 'yellow'))
        print(colored(f"The following images will be resized only: {old_pngs}", 'yellow'))
        if input(colored("Are you sure you want to continue?", 'green') + " [y,N] ").lower() == 'y':
            convert_to_png(jpgs)
            pngs = check_folder_forpng()
            only_new_pngs = [elem for elem in pngs if elem not in old_pngs]
            multithreaded_resizer(pngs)
            remove_temp_files(only_new_pngs)
            print(colored("Done! You will find all your resized images in the Results folder.", 'green'))
        else:
            print(colored("Operation aborted.", 'yellow'))
    else:
        print(colored("There are no available pictures to convert or resize in this folder.", 'red'))
