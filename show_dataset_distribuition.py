import sys
import os
import cv2
import argparse
import xml.etree.ElementTree as ET
from data.config import classes
import numpy as np
import json
import yaml
import matplotlib.pyplot as plt

from data.config import classes

def main():
    
    parser = argparse.ArgumentParser(description='Process labeled images to generate files to be used during the training phase')
    parser.add_argument('--in_folder',
                        dest='input_dataset_path',
                        required=True,
                        help='Path to the folder with labeled records')

    args = parser.parse_args()

    dataset_in_path = args.input_dataset_path
    if os.path.isdir(dataset_in_path) == False:
        print("Error: Input path is not a directory")
        exit(1)

    label_freq_distrib = np.zeros(len(classes.sign_labels))

    # get all labeled record
    list_records = os.listdir(dataset_in_path)
    for record in list_records:
        record_path = dataset_in_path + "/" + record

        if os.path.isdir(record_path) == False:
            continue

        # check if folder images and labels exist
        record_images_path = record_path + "/images"
        record_labels_path = record_path + "/labels"
        if (os.path.isdir(record_images_path) and os.path.isdir(record_labels_path)) == False:
            continue

        # read all images of a folder
        all_images_record = os.listdir(record_images_path)
        for image_file in all_images_record:

            image_path = record_images_path + "/" + image_file

            image_filename = image_file.split(".")[0]
            annotation_path = record_labels_path + "/" + image_filename + ".xml"

            image_labels_list = list()
            image_boxes_list = list()

            # read annotation file
            if os.path.exists(annotation_path) == True:
                label_file = ET.parse(annotation_path)
                xml_root = label_file.getroot()

                # for each object of the annotation, increment label counter
                for obj in xml_root.iter('object'):
                    label = obj.find('name').text.lower().strip()

                    if label in classes.sign_labels:
                        class_index = classes.sign_labels.index(label)
                        label_freq_distrib[class_index] += 1

            else:
                continue

            # load image
            image = cv2.imread(image_path)
            #cv2.imshow("image", image)
            #cv2.waitKey(1)

    print()
    print("Dataset frequency distribution")
    for ci, cl in enumerate(classes.sign_labels):
        print("- " + cl + ": " + str(label_freq_distrib[ci]))
    
    print()
    print("Max: " + str(np.max(label_freq_distrib)))
    print()

    fig, ax = plt.subplots()
    y_pos = np.arange(len(classes.sign_labels))
    ax.barh(y_pos, label_freq_distrib, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(classes.sign_labels)
    ax.set_title('Frequency distribution')
    plt.show()
    
if __name__ == "__main__":
    main()