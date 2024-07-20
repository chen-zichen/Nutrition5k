'''
    Description: For the interaction mode, we collect the images, 
        this file is used to rename the images based on the modification time.
'''

import os
from shutil import move
from datetime import datetime
import re

reference_folder_path = 'refer/'
folder_to_rename_path = 'seg_images/'

# extract the numerical part of the filename
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else None

# sort the reference images based on their numberical part
reference_images = os.listdir(reference_folder_path)
reference_images.sort(key=lambda x: extract_number(x))

# sort the images to rename based on their modification time
images_to_rename = os.listdir(folder_to_rename_path)
images_to_rename.sort(key=lambda x: os.path.getmtime(os.path.join(folder_to_rename_path, x)))

if len(reference_images) != len(images_to_rename):
    print("The number of images in both folders does not match. Please check the folders.")
else:
    # Rename the images
    for i, image_name in enumerate(images_to_rename):
        # Extract the extension of images in folder to rename
        extension = os.path.splitext(image_name)[1]
        # Construct the new name based on the reference image's name
        new_name = reference_images[i]
        # Ensure the new name keeps its original extension if different
        if not new_name.endswith(extension):
            new_name += extension
        # Define the source and destination paths
        src_path = os.path.join(folder_to_rename_path, image_name)
        dst_path = os.path.join(folder_to_rename_path, new_name)
        # Rename (move) the file
        move(src_path, dst_path)
        print(f'Renamed {image_name} to {new_name}')

print("Renaming complete.")
