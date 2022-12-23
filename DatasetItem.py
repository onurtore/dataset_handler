import os
import time
import datetime
import cv2

class DatasetItem():

    def __init__(self, path = None):
        self.path = path
        self.gg = dict()
        self.image = None
        self.time = None
        self.properties = dict()
        return

    def check_labels(self, labels=None):
        if "labels" not in self.path:
            return -1

        self.image = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        for label in labels:
            label_len = len(self.image[self.image == label])
            if label_len:
                self.properties['label-' + str(label) ] = label_len
        del self.image
        self.image = None
        return

    def get_size(self):
        if not self.image:
            self.image = cv2.imread(self.path)
        return self.image.shape

    def get_time_from_modification(self):
        modified = os.path.getmtime(self.path)
        year, month, day, hour, minute, second = time.localtime(modified)[:-3]
        self.time = datetime.datetime(year, month, day, hour, minute, second)
        self.properties["date"] = self.time.strftime("%y-%m-%d")
        return

    def get_time_from_name(self):
        fname = self.path.split('/')[-1]
        fname = fname.replace('-','_').replace("HQ", '').replace('x', '_').replace('.png', '').replace('.jpg', '')
        fname = fname[fname.index('2022'):]
        dt = [int(x) for x in fname.split('_')]
        self.time = datetime.datetime(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5])
        self.properties["date"] = self.time.strftime("%y-%m-%d")
        return


    def set_time(self, time):
        self.time = time
        self.properties["date"] = self.time.strftime("%y-%m-%d")
        return

    def get_modification_time(self, calc_type="name"):
        if calc_type == "name":
            self.get_time_from_name()
        else:
            self.get_time_from_modification()

    def __getitem__(self, i):
        return self.image_items[int(i)], self.label_items[int(i)]

    def __eq__(self, other):
        other_path  = other
        res = False
        if not isinstance(other,str):
            other_path = other.path
        if other_path == self.path:
            res = True
        return res

    def del_label_data(self):
        del self.image
        self.img = None
        return