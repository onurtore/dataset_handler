"""Contain the image and the label entries of the dataset."""
import datetime
import os
import time

import cv2


class DatasetItem:
    """Contain the image and the label entries of the dataset."""

    def __init__(self, path=None):
        """Init the object."""
        self.path = path
        self.gg = dict()
        self.image = None
        self.time = None
        self.properties = dict()
        return

    def check_labels(self, labels=None):
        """Check the image for the labels."""
        if "labels" not in self.path:
            return -1

        self.image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        for label in labels:
            label_len = len(self.image[self.image == label])
            if label_len:
                self.properties["label-" + str(label)] = label_len
        del self.image
        self.image = None
        return

    def get_size(self):
        """Return the image size."""
        if not self.image:
            self.image = cv2.imread(self.path)
        return self.image.shape

    def calc_date_from_modification(self):
        """Calculate the date from modification."""
        modified = os.path.getmtime(self.path)
        year, month, day, hour, minute, second = time.localtime(modified)[:-3]
        self.time = datetime.datetime(year, month, day, hour, minute, second)
        self.properties["date"] = self.time.strftime("%y-%m-%d")
        return

    def calc_date_from_name(self):
        """Calculate the date from name."""
        fname = self.path.split("/")[-1]
        fname = fname.replace("-", "_")
        fname = fname.replace("HQ", "")
        fname = fname.replace("x", "_")
        fname = fname.replace(".png", "")
        fname = fname.replace(".jpg", "")
        fname = fname[fname.index("2022") :]
        dt = [int(x) for x in fname.split("_")]
        self.time = datetime.datetime(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
        self.properties["date"] = self.time.strftime("%y-%m-%d")
        return

    def set_date(self, time):
        """Set the date of the item."""
        self.time = time
        self.properties["date"] = self.time.strftime("%y-%m-%d")
        return

    def calc_date(self, calc_type="name"):
        """Calculate the date of the item from name or modification."""
        if calc_type == "name":
            self.calc_date_from_name()
        else:
            self.calc_date_from_modification()

    def __eq__(self, other):
        """Check equality of the two item."""
        other_path = other
        res = False
        if not isinstance(other, str):
            other_path = other.path
        if other_path == self.path:
            res = True
        return res

    def del_label_img(self):
        """Delete image from the item."""
        del self.image
        self.img = None
        return
