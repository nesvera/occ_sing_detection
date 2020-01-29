import numpy as np
import csv
import os
import xml.etree.ElementTree as ET
import argparse
import cv2

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Convert dataset from VOC format to Yolo")
    parser.add_argument("--dataset",
                        dest="dataset",
                        required=True,
                        help="Path to the dataset, or collection of datasets")
    parser.add_argument("--train_perc",
                        dest="train_perc",
                        required=True,
                        help="Percentage for the training part (0.->1.)")

    args = parser.parse_args()

    dataset_path = args.dataset
    if os.path.isdir(dataset_path) == False:
        print("Error: input path is not a folder or it does not exist")
        exit(1)

    train_perc = float(args.train_perc)
    if(train_perc < 0 or train_perc > 1):
        print("Error: training size should be between 0 and 1")
        exit(1)

    images_folder = os.path.abspath(os.path.join(dataset_path, "images"))
    labels_folder = os.path.abspath(os.path.join(dataset_path, "labels"))

    out_train_file = os.path.join(dataset_path, "train.txt")
    out_valid_file = os.path.join(dataset_path, "valid.txt")

    # read and sort images filenames
    image_files = os.listdir(images_folder)
    image_files.sort()

    train_qnt = int(len(image_files)*train_perc)
    train_set = image_files[0:train_qnt]
    valid_set = image_files[train_qnt:]

    with open(out_train_file, 'w') as f:
        for file in train_set:
            file = images_folder + "/" + file + "\n"
            f.write(file)

    with open(out_valid_file, 'w') as f:
        for file in valid_set:
            file = images_folder + "/" + file + "\n"
            f.write(file)



