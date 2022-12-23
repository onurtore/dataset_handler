
import os
import numpy as np
import copy

from DatasetItem import DatasetItem


def img2label(path):
    return path.replace('jpg', 'png').replace('images', 'labels')


def label2img(path):
    return path.replace('png', 'jpg').replace('labels', 'images')



def split_by_percentage(images, labels, percentages):
    """
    Input:
        (images, labels)
    Output:
        [(train_images, train_labels), (val_images, val_labels)]
    """

    shuffle_order = np.random.permutation(len(images))
    images = np.array(images)[shuffle_order] #Not smart!
    labels = np.array(labels)[shuffle_order] #Again!!
    train_images = images[0:int(len(images) * percentages['train'])]
    train_labels = labels[0:int(len(images) * percentages['train'])]
    val_images = list(images[int(len(images) * percentages['train']):])
    val_labels = list(labels[int(len(images) * percentages['train']):])
    return [(train_images, train_labels), (val_images, val_labels)]


class Dataset():

    def __init__(self, label_path = None):
        self.label_path = label_path
        self.idx = 0

        self.get_file_paths()
        return


    def get_file_paths(self):

        fnames = os.listdir(self.label_path)
        self.label_items =\
                [DatasetItem(os.path.join(self.label_path, x)) for x in fnames]
        self.image_items =\
                [DatasetItem(label2img(os.path.join(self.label_path, x))) for x in fnames]
        return


    def copy_images(self, path, filter_properties=None):
        """
        If properties are given then only images which complies with the
        properties will be copied.
        """

        for i, image_item in enumerate(self.image_items):
            image_properties = image_item.properties
            label_properties = self.label_items[i].properties
            image_properties.update(label_properties)
            val = self.check_filter(image_properties, filter_properties)

            if not val:
                continue

            command = 'cp "' + image_item.path + '" ' + path
            try:
                os.system(command)
            except:
                print('Problem with command')

        return


    def set_day_condition(self, date, condition):
        for i, image_item in enumerate(self.image_items):
            image_item_date = image_item.time.strftime("%y-%m-%d")
            if date == 'all' or image_item_date == date:
                image_item.properties["condition"] = condition
                self.label_items[i].properties["condition"] = condition
        return


    def set_place(self, date, condition):
        for i, image_item in enumerate(self.image_items):
            image_item_date = image_item.time.strftime("%y-%m-%d")
            if date == 'all' or image_item_date == date:
                image_item.properties["place"] = condition
                self.label_items[i].properties["place"] = condition
        return



    def get_modification_times(self, calc_type = 'name'):
        for i, image_item in enumerate(self.image_items):
            image_item.get_modification_time(calc_type)
            self.label_items[i].set_time(image_item.time)
        self.sort_by_time()
        return


    def sort_by_time(self):
        self.image_items.sort(key=lambda x: x.time, reverse=True)
        self.label_items.sort(key=lambda x: x.time, reverse=True)
        return


    def index(self, path):
        for i, image_item in enumerate(self.image_items):
            if path == image_item.path:
                return i
        return -1


    def get_distinct_days(self):
        return set([image.time.strftime("%y-%m-%d") for image in self.image_items])


    def cutout(self, idx):
        """
        Remove the labels/images after some index value. (idx removed as well)
        """
        self.label_items = self.label_items[:idx]
        self.image_items = self.image_items[:idx]
        return


    def __len__(self):
        return len(self.label_items)

    def check_filter(self, item_properties, filter_properties):
        valid = True

        if not filter_properties:
            return valid

        for filter_key, filter_value in filter_properties.items():
            if filter_key not in item_properties or\
                type(filter_value)(item_properties[filter_key]) != filter_value:
                valid=False
                break
        return valid


    def len_with_filter(self, filter_properties=None):
        """
        If propertiles are given then only images which complies with the
        properties will be copied.
        """
        if not filter_properties:
            return self.__len__()

        count = 0
        for i, label_item in enumerate(self.label_items):
            label_properties = label_item.properties
            image_properties = self.image_items[i].properties
            image_properties.update(label_properties)
            val = self.check_filter(image_properties, filter_properties)
            if val:
                count += 1
        return count


    def __getitem__(self, i):
        image_path = None
        label_path = None

        image_path = self.image_items[int(i)].path
        temp_label_path = img2label(image_path)
        if temp_label_path in self.label_items:
            label_path = temp_label_path
        return image_path, label_path


    def check_labels(self, labels=None):
        for i, label_item in enumerate(self.label_items):
            if i % 20 == 0:
                print(str(i) + '/' + str(len(self.label_items)))
            label_item.check_labels(labels)
            self.image_items[i].properties.update(label_item.properties)
        return


    def del_label_data(self):
        for label_item in self.label_items:
            label_item.del_label_data()


    def clean_by_size(self, h, w):
        for i in range(len(self.label_items)):
            print('Checked: ' + str(i) + '/' + str(len(self.label_items)))
            label_item = self.label_items[i]
            curr_h, curr_w = label_item.get_size()
            if h != curr_h or w != curr_w:
                self.remove_item_idx(i) #TO-DO: Change to list comphrension
                i -= 1


    def exclude_labels_from_labels(self, labels):
        for label in labels:
            found = False
            for i in range(len(self.label_items)):
                if label == self.label_items[i].path.split('/')[-1]:
                    found = True
                    self.remove_item_idx(i) #TO-DO: Change to list comphrension
                    break
            if not found:
                print("Could not found the label: " + str(label))
                return
        return


    def exclude_labels_from_date(self, date):
        image_items = [x for x in self.image_items if date != x.properties["date"]]
        label_items = [x for x in self.label_items if date != x.properties["date"]]
        assert len(self.image_items) > len(image_items)
        self.image_items = image_items
        self.label_items = label_items
        return