import hashlib
import os
from PIL import Image
from shutil import copy2

def file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def log_output(string, txt_file):
    print(string)
    txt_file.write(string + '\n')

def remove_duplicates(parent_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    index = 0
    count = 0

    for folder in os.listdir(parent_dir):
        folder_path = os.path.join(parent_dir, folder)
        output_folder_path = os.path.join(output_dir, folder)
        
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        hashes = set()
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            try:
                img_hash = file_hash(file_path)
                if img_hash not in hashes:
                    hashes.add(img_hash)
                    copy2(file_path, output_folder_path)
            except IOError:
                print(f'Error processing file: {file_path}')
        index += 1
        count = count + len(hashes)
        log_output(f'Finished processing folder {index}, {folder_path}, there are normal {len(hashes)} images in this folder', txt_file)
    log_output(f'Finished processing all folders, there are total {count} images', txt_file)

parent_directory = './dst/'
output_directory = './dst_unique/'
txt_file = open('./dst_unique.txt', 'w')
remove_duplicates(parent_directory, output_directory)
