import os 
import sys

def add_extension(file_name, extension):
    return file_name + '.' + extension

folder_path = input('Enter the folder path: ').replace('"', '')
extension = input('Enter the extension: ')


for root, dirs, files in os.walk(folder_path):
    for file in files:
        if not (file.endswith(extension)):
            file_path = os.path.join(root, file)
            os.rename(file_path, add_extension(file_path, extension))
            print(f'{file_path} renamed to {add_extension(file_path, extension)}')
