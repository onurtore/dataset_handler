import os
import cv2
from pathlib import Path

dataset_folder = Path('/media/delivers-26/My Passport/Delivers.ai/images/ls')
dataset_folder_parent = dataset_folder.parent.absolute()

img_dims = dict()
dir_list = os.listdir(dataset_folder)

for i, dir in enumerate(dir_list):
    if i % 10 == 0:
        print(str(i) + '/' + str(len(dir_list)))
    img = cv2.imread(os.path.join(dataset_folder, dir))
    img_shape_str = str(img.shape).replace(' ', '')
    img_shape_str = img_shape_str.replace('(', '')
    img_shape_str = img_shape_str.replace(')', '')
    img_shape_str = img_shape_str.replace(' ', '')
    img_shape_str = img_shape_str.replace(',', '_')
    if  img_shape_str not in img_dims.keys():
        img_dims[img_shape_str] = img_shape_str
        basename = os.path.basename(dataset_folder)
        new_path = os.path.join(dataset_folder_parent, basename + '_' + img_shape_str)
        if not os.path.exists(new_path):
            os.mkdir(new_path)
    command = 'mv "'  + str(os.path.join(dataset_folder, dir))+ '" "' + new_path + '"'
    os.system(command)