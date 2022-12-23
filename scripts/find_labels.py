import os
import cv2
import numpy as np
from pathlib import Path
from sklearn.utils.class_weight import compute_class_weight

"""

"""


DATASET_LABEL_DIR1 = Path('/media/delivers-26/My Passport/Delivers.ai/labels/ls_720_1280_3')
DATASET_LABEL_DIR2 = Path('/media/delivers-26/My Passport/Delivers.ai/labels/coone_720_1280_3')
DATASET_LABELS = [DATASET_LABEL_DIR1, DATASET_LABEL_DIR2]



def find_labels(dataset_label_dirs):

    dir_list = list()
    for dataset_label_dir in dataset_label_dirs:
        fname = os.listdir(dataset_label_dir)
        fname_abs = [os.path.join(dataset_label_dir, x) for x in fname]
        dir_list.extend(fname_abs)

    total_label = str(len(dir_list))
    specific_label = 3
    for i, dir in enumerate(dir_list):
        if i % 100 == 0:
            print(str(i) + '/' + str(total_label))
        img = cv2.imread(os.path.join(dir), cv2.IMREAD_GRAYSCALE)
        cnt = len(img[img == specific_label])
        if cnt > 0:
            image_dir = os.path.join(dir).replace("labels", "images")
            image_dir = image_dir.replace("png", "jpg")
            command = 'cp "' + image_dir + '" /home/delivers-26/Desktop/imgs/'
            os.system(command)
            print(os.path.join(dir))
    return


if __name__ == '__main__':
    find_labels(DATASET_LABELS)

