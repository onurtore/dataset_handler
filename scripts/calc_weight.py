import os
import cv2
import numpy as np
from pathlib import Path
from sklearn.utils.class_weight import compute_class_weight

"""
Calculates same value with the compute_class_weight from sklearn however it is better
because does not need to actual labels.
used
"""


DATASET_LABEL_DIR1 = Path('/media/delivers-26/My Passport/Delivers.ai/labels/ls_720_1280_3')
DATASET_LABEL_DIR2 = Path('/media/delivers-26/My Passport/Delivers.ai/labels/coone_720_1280_3')
DATASET_LABELS = [DATASET_LABEL_DIR1, DATASET_LABEL_DIR2]



def calc_total_pixel(dataset_label_dirs):

    dir_list = list()
    for dataset_label_dir in dataset_label_dirs:
        fname = os.listdir(dataset_label_dir)
        fname_abs = [os.path.join(dataset_label_dir, x) for x in fname]
        dir_list.extend(fname_abs)

    total_label = str(len(dir_list))
    pixels_counts = dict()
    labels = [0, 1, 2, 3]
    for i, dir in enumerate(dir_list):
        if i % 100 == 0:
            print(str(i) + '/' + str(total_label))
        img = cv2.imread(os.path.join(dir), cv2.IMREAD_GRAYSCALE)
        for label in labels:
            cnt = len(img[img == label])
            if label not in pixels_counts.keys():
                pixels_counts[label] = cnt
            else:
                pixels_counts[label] += cnt

    return pixels_counts

def calc_class_weights(pixel_counts, log_smooth=False, weight_cutout=None):

    class_weights = dict()
    n_labels = len(pixel_counts.keys())

    total_pixel = 0
    for key in pixel_counts.keys():
        total_pixel += pixel_counts[key]

    for key in pixel_counts.keys():
        weight = total_pixel / (n_labels * pixel_counts[key])

        if log_smooth:
            weight = np.log(weight)


        weight = weight_cutout if weight_cutout and weight > weight_cutout\
                    else weight

        class_weights[key] = weight

    return class_weights



def print_dict(dict):
    for key in class_weights.keys():
        print(str(key) + ': ' + str(class_weights[key]))
    print('Done')


if __name__ == '__main__':
    #pixel_counts = calc_total_pixel(DATASET_LABELS)

    pixel_counts = {
        0: 764794749,
        1: 368303158,
        2: 733219329,
        3: 52453964
    }
    class_weights = calc_class_weights(pixel_counts, log_smooth=False,\
                                       weight_cutout=None)
    print_dict(class_weights)
