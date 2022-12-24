"""Implements dataset class for semantic segmentation task."""
from os import listdir, system
from os.path import join

import numpy as np

from DatasetItem import DatasetItem


def remove_ext(file_name):
    """Remove the ext from the filename."""
    return file_name.split(".")[0]


def get_file_name(path):
    """Return the filename from the full path."""
    return path.split("/")[-1]


def img2label(path):
    """Return label file path converted from image path."""
    return path.replace("jpg", "png").replace("images", "labels")


def label2img(path):
    """Return image file path converted from label path."""
    return path.replace("png", "jpg").replace("labels", "images")


def split_by_percentage(images, labels, percentages):
    """Split the image and labels into train and validation items.

    Input:
        images, labels
    Output:
        [(train_images, train_labels), (val_images, val_labels)]
    """
    shuffle_order = np.random.permutation(len(images))
    images = np.array(images)[shuffle_order]  # Not smart!
    labels = np.array(labels)[shuffle_order]  # Again!!
    train_images = images[0 : int(len(images) * percentages["train"])]
    train_labels = labels[0 : int(len(images) * percentages["train"])]
    val_images = list(images[int(len(images) * percentages["train"]) :])
    val_labels = list(labels[int(len(images) * percentages["train"]) :])
    return [(train_images, train_labels), (val_images, val_labels)]


class Dataset:
    """Contain dataset object."""

    def __init__(self, label_path=None):
        """Initialize the class."""
        self.label_path = label_path
        self.idx = 0

        self.calc_file_paths()
        return

    def calc_file_paths(self):
        """Calculate the file paths for labels and images.

        Generates the corresponding image and label items objects from the\
            label path.
        """
        fnames = listdir(self.label_path)
        self.label_items = [
            DatasetItem(join(self.label_path, x)) for x in fnames
        ]
        self.image_items = [
            DatasetItem(label2img(join(self.label_path, x))) for x in fnames
        ]
        return

    def copy_images(self, path, filter_properties=None):
        """Copy images to a given path from the dataset.

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
            system(command)
        return

    def set_day_condition(self, date, condition):
        """Set the day condition for the given condition."""
        for i, image_item in enumerate(self.image_items):
            image_item_date = image_item.time.strftime("%y-%m-%d")
            if date == "all" or image_item_date == date:
                image_item.properties["condition"] = condition
                self.label_items[i].properties["condition"] = condition
        return

    def set_place(self, date, condition):
        """Set the place for the given condition."""
        for i, image_item in enumerate(self.image_items):
            image_item_date = image_item.time.strftime("%y-%m-%d")
            if date == "all" or image_item_date == date:
                image_item.properties["place"] = condition
                self.label_items[i].properties["place"] = condition
        return

    def calc_dates(self, calc_type="name"):
        """Calculate the dates of the dataset elements."""
        for i, image_item in enumerate(self.image_items):
            image_item.calc_date(calc_type)
            self.label_items[i].set_time(image_item.time)
        self.sort_by_time()
        return

    def sort_by_date(self):
        """Sort the dataset items by date."""
        self.image_items.sort(key=lambda x: x.time, reverse=True)
        self.label_items.sort(key=lambda x: x.time, reverse=True)
        return

    def index(self, path):
        """Return the index of the image file."""
        for i, image_item in enumerate(self.image_items):
            if path == image_item.path:
                return i
        return -1

    def get_distinct_days(self):
        """Return the number of distinct days in the dataset."""
        return set(
            [image.time.strftime("%y-%m-%d") for image in self.image_items]
        )

    def cutout(self, idx):
        """Remove the labels/images after some index value. (idx as well)."""
        self.label_items = self.label_items[:idx]
        self.image_items = self.image_items[:idx]
        return

    def __len__(self):
        """Return len of the labels."""
        return len(self.label_items)

    def check_filter(self, item_properties, filter_properties):
        """TO-DO: Fill."""
        valid = True

        if not filter_properties:
            return valid

        for filter_key, filter_value in filter_properties.items():
            item_value = type(filter_value)(item_properties[filter_key])
            if filter_key not in item_properties or item_value != filter_value:
                valid = False
                break
        return valid

    def len_with_filter(self, filter_properties=None):
        """Calculate len with the given filter.

        If properties are given then only images which complies with the
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
        """Return image and label path for the given index."""
        image_path = None
        label_path = None

        image_path = self.image_items[int(i)].path
        temp_label_path = img2label(image_path)
        if temp_label_path in self.label_items:
            label_path = temp_label_path
        return image_path, label_path

    def check_labels(self, labels=None):
        """Check the images for the given labels."""
        for i, label_item in enumerate(self.label_items):
            if i % 20 == 0:
                print(str(i) + "/" + str(len(self.label_items)))
            label_item.check_labels(labels)
            self.image_items[i].properties.update(label_item.properties)
        return

    def del_label_img(self):
        """Delete the loaded images of dataset from items."""
        for label_item in self.label_items:
            label_item.del_label_img()

    def exclude_labels_from_labels(self, labels):
        """Remove given labels from the dataset."""
        for label in labels:
            label_wo_ext = remove_ext(label)
            label_items = [
                x for x in self.label_items if get_file_name(x.path) != label
            ]
            image_items = [
                x
                for x in self.image_items
                if remove_ext(get_file_name(x.path)) != label_wo_ext
            ]
            assert len(self.image_items) == len(image_items) + 1
            assert len(label_items) == len(image_items)
            self.image_items = image_items
            self.label_items = label_items
        return

    def exclude_labels_from_date(self, date):
        """Remove given dates from the dataset."""
        image_items = [
            x for x in self.image_items if date != x.properties["date"]
        ]
        label_items = [
            x for x in self.label_items if date != x.properties["date"]
        ]
        assert len(self.image_items) > len(image_items)
        assert len(image_items) == len(label_items)
        self.image_items = image_items
        self.label_items = label_items
        return
