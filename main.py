"""Generate train and val txts."""
import copy
import os
import pickle

from Dataset import Dataset, split_by_percentage


def load_labels(labels_path):
    """Load new line seperated labels from txt file."""
    f = open(labels_path, "r")
    lines = [line.rstrip() for line in f]
    return lines


def prepare_ls():
    """Generate ls dataset using coone labels."""
    ls_dataset = Dataset(
        label_path="/media/delivers-26/My Passport/\
                            Delivers.ai/labels/ls_720_1280_3"
    )
    dataset_len = len(ls_dataset)
    print("Dataset label count: " + str(dataset_len))
    ls_dataset.get_modification_times(calc_type="name")
    distinct_days = list(ls_dataset.get_distinct_days())
    distinct_days.sort()
    print(distinct_days)
    ls_dataset.set_day_condition("22-04-12", "rainy")
    ls_dataset.set_day_condition("22-04-18", "rainy")
    ls_dataset.set_day_condition("22-05-17", "sunny")
    ls_dataset.set_day_condition("22-07-27", "sunny")
    ls_dataset.set_day_condition("22-07-28", "sunny")
    ls_dataset.set_day_condition("22-08-05", "sunny")
    ls_dataset.set_day_condition("22-08-12", "sunny")
    ls_dataset.set_day_condition("22-08-13", "sunny")
    ls_dataset.set_day_condition("22-08-14", "sunny")
    ls_dataset.set_day_condition("22-08-15", "sunny")
    ls_dataset.set_day_condition("22-08-16", "sunny")

    ls_dataset.set_place("22-04-12", "ITU")
    ls_dataset.set_place("22-04-18", "ITU")
    ls_dataset.set_place("22-05-17", "Caddebostan")
    ls_dataset.set_place("22-07-27", "Spain?")
    ls_dataset.set_place("22-07-28", "Spain?")
    ls_dataset.set_place("22-08-05", "ITU")
    ls_dataset.set_place("22-08-12", "Spain?")
    ls_dataset.set_place("22-08-13", "Spain?")
    ls_dataset.set_place("22-08-14", "Spain?")
    ls_dataset.set_place("22-08-15", "Spain?")
    ls_dataset.set_place("22-08-16", "Spain?")
    ls_dataset.check_labels(labels=[0, 1, 2, 3])

    """
    properties1 = {'time': '22-04-12'}
    properties2 = {'time': '22-04-18'}
    properties3 = {'time': '22-05-17'}
    count1 = ls_dataset.len_with_filter(properties1)
    count2 = ls_dataset.len_with_filter(properties2)
    print ("Filtered count is: ", count1 + count2)
    ls_dataset.copy_images('/home/delivers-26/Desktop/ls_bycycle', properties)
    """
    return ls_dataset


def prepare_coone():
    """Generate coone dataset using coone labels."""
    coone_dataset = Dataset(
        label_path="/media/delivers-26/My Passport/\
                                Delivers.ai/labels/coone_720_1280_3"
    )
    # coone_dataset.index('/media/delivers-26/My Passport/\
    #       Delivers.ai/labels/coone_720_1280_3/\
    #       0b722f91-a05a-4e26-ac19-fe7a849a8636.jpg')

    coone_dataset.check_labels(labels=[0, 1, 2, 3])
    coone_dataset.get_modification_times(calc_type="modification")
    coone_dataset.set_day_condition("all", "sunny")
    coone_dataset.set_place("all", "ITU")

    """
    print(coone_dataset.len_with_filter(properties))
    coone_dataset.copy_images(path='/home/delivers-26/Desktop/coone_bicycle',
                               filter_properties=properties)
    """
    return coone_dataset


def create_splits(ls_dataset, coone_dataset, split_path):
    """Create train and val splits using dataset objects."""
    label_percentages = {
        "train": 0.8,
        "val": 0.2,
    }

    image_items = copy.deepcopy(coone_dataset.image_items)
    label_items = copy.deepcopy(coone_dataset.label_items)

    image_items.extend(ls_dataset.image_items)
    label_items.extend(ls_dataset.label_items)

    assert len(image_items) == len(label_items)

    train_split, val_split = split_by_percentage(
        image_items, label_items, label_percentages
    )
    train_images, train_labels = train_split
    val_images, val_labels = val_split

    assert len(train_images) == len(train_labels)
    assert len(val_images) == len(val_labels)

    image_prefix = "/media/delivers-26/My Passport/Delivers.ai/images/"
    label_prefix = "/media/delivers-26/My Passport/Delivers.ai/labels/"
    post_fix = "_720_1280_3"
    with open(os.path.join(split_path, "train.txt"), "w") as f:
        for i, train_image in enumerate(train_images):
            image_path = str(train_image.path).replace(image_prefix, "")
            image_path = image_path.replace(post_fix, "")
            label_path = str(train_labels[i].path).replace(label_prefix, "")
            label_path = label_path.replace(post_fix, "")
            image_path_assert = image_path.replace(".jpg", "")
            label_path_assert = label_path.replace(".png", "")
            assert image_path_assert == label_path_assert
            line = image_path + " " + label_path
            f.write(f"{line}")
            if i != len(train_images) - 1:
                f.write("\n")

    with open(os.path.join(split_path, "val.txt"), "w") as f:
        for i, val_image in enumerate(val_images):
            image_path = str(val_image.path).replace(image_prefix, "")
            image_path = image_path.replace(post_fix, "")
            label_path = str(val_labels[i].path).replace(label_prefix, "")
            label_path = label_path.replace(post_fix, "")
            image_path_assert = image_path.replace(".jpg", "")
            label_path_assert = label_path.replace(".png", "")
            assert image_path_assert == label_path_assert
            line = image_path + " " + label_path
            f.write(f"{line}")
            if i != len(val_images) - 1:
                f.write("\n")
    return


if __name__ == "__main__":

    """
    ls_dataset = prepare_ls()
    coone_dataset = prepare_coone()

    with open('dataset_pickles/ls_dataset.pickle', 'wb') as handle:
        pickle.dump(ls_dataset, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('dataset_pickles/coone_dataset.pickle', 'wb') as handle:
        pickle.dump(coone_dataset, handle, protocol=pickle.HIGHEST_PROTOCOL)
    """

    file = open("dataset_pickles/ls_dataset.pickle", "rb")
    ls_dataset = pickle.load(file)
    file.close()

    file = open("dataset_pickles/coone_dataset.pickle", "rb")
    coone_dataset = pickle.load(file)
    file.close()

    loaded_labels1 = load_labels(
        "exceptions/ls_caddebostan_bicycle_exceptions.txt"
    )
    loaded_labels2 = load_labels("exceptions/ls_ITU_bicycle_exceptions.txt")
    ls_dataset.exclude_labels_from_labels(loaded_labels1)
    ls_dataset.exclude_labels_from_labels(loaded_labels2)
    ls_dataset.exclude_labels_from_date("22-05-17")
    ls_dataset.exclude_labels_from_date("22-07-27")
    ls_dataset.exclude_labels_from_date("22-07-28")
    ls_dataset.exclude_labels_from_date("22-08-12")
    ls_dataset.exclude_labels_from_date("22-08-13")
    ls_dataset.exclude_labels_from_date("22-08-14")
    ls_dataset.exclude_labels_from_date("22-08-15")
    ls_dataset.exclude_labels_from_date("22-08-16")

    loaded_labels1 = load_labels("exceptions/coone_ITU_bicycle_exceptions.txt")
    coone_dataset.exclude_labels_from_labels(loaded_labels1)

    create_splits(ls_dataset, coone_dataset, "splits/split2")
