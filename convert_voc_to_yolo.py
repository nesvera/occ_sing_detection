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
    parser.add_argument("--out_folder",
                        dest="out_folder",
                        required=True,
                        help="Path to a new folder that will receive the converted dataset")
    parser.add_argument("--class_names",
                        dest="class_names",
                        required=True,
                        help="File defining label names")

    args = parser.parse_args()

    dataset_path = args.dataset
    if os.path.isdir(dataset_path) == False:
        print("Error: input path is not a folder or it does not exist")
        exit(1)

    out_folder_path = args.out_folder
    if os.path.exists(out_folder_path) == True:
        print("Error: output folder already exists, type another name for output folder")
        exit(1)

    out_images_folder_path = out_folder_path + "/images"
    out_labels_folder_path = out_folder_path + "/labels"
    os.mkdir(out_folder_path)
    os.mkdir(out_images_folder_path)
    os.mkdir(out_labels_folder_path)

    class_names_path = args.class_names
    if os.path.exists(class_names_path) == False:
        print("Error: class names file does not exist")
        exit(1)

    # read class names and create a dictionary with numbers for each label
    class_names_dict = {}
    with open(class_names_path) as f:

        class_counter = 0
        file_line = f.readline()
        while len(file_line) > 1:
            file_line = file_line.strip()

            class_names_dict[file_line] = class_counter
            class_counter += 1

            file_line = f.readline()

    # open each record folder inside the main directory; find and convert labels; and copy just images that contains a label file
    sub_folder = os.listdir(dataset_path)
    for sub_folder_ind, folder in enumerate(sub_folder):
        
        if os.path.isdir(os.path.join(dataset_path, folder)) == True:

            images_folder = os.path.join(os.path.join(dataset_path, folder, "images"))
            labels_folder = os.path.join(os.path.join(dataset_path, folder, "labels"))

            # just save image if there are labes for it
            save_image = False

            if os.path.isdir(labels_folder):
                
                label_files = os.listdir(labels_folder)
                for label_files_ind, file in enumerate(label_files):

                    print("Folder " + str(sub_folder_ind) + "/" + str(len(sub_folder)) + 
                          " - File: " + str(label_files_ind) + "/" + str(len(label_files)))
                    
                    # read VOC format file
                    if file.endswith(".xml"):

                        filename = file.split(".xml")[0]
                        in_image_path = images_folder + "/" + filename + ".png"

                        out_image_path = out_images_folder_path + "/" + filename + ".png"
                        out_label_path = out_labels_folder_path + "/" + filename + ".txt"

                        if os.path.exists(in_image_path) == False:
                            print("Error: Image does not exist")
                            print("Image: " + in_image_path)
                            print("Label: " + os.path.join(labels_folder, file))
                            print()
                            continue

                        # copy image to new folder
                        im = cv2.imread(in_image_path)
                        if(im.shape[0] == 0 or im.shape[1] == 0 or im is None):
                            print("Error: Image size is Null")
                            continue

                        # read label and convert to yolo's
                        tree = ET.parse(os.path.join(labels_folder, file))
                        raiz = tree.getroot()

                        image_width = float(raiz.find('size/width').text)
                        image_height = float(raiz.find('size/height').text)

                        yolo_label_txt = ""

                        # for each object in the image
                        for obj_class in raiz.findall('object'):
                            obj_name = obj_class.find("name").text
                            obj_name = obj_name.strip()

                            # check if label are in the list
                            if(obj_name in class_names_dict.keys()) == True:

                                obj_number = class_names_dict[obj_name]
                                obj_xmin = int(obj_class.find("bndbox/xmin").text)
                                obj_ymin = int(obj_class.find("bndbox/ymin").text)
                                obj_xmax = int(obj_class.find("bndbox/xmax").text)
                                obj_ymax = int(obj_class.find("bndbox/ymax").text)

                                obj_x_center =  ((obj_xmax + obj_xmin)/(2.*image_width))
                                obj_y_center =  ((obj_ymax + obj_ymin)/(2.*image_height))
                                obj_width =     ((obj_xmax - obj_xmin)/image_width)
                                obj_height =    ((obj_ymax - obj_ymin)/image_height)

                                obj_label = str(obj_number) + " " +\
                                            str(obj_x_center) + " " +\
                                            str(obj_y_center) + " " +\
                                            str(obj_width) + " " +\
                                            str(obj_height) + "\n"

                                #yolo_label_file.write(obj_label)
                                yolo_label_txt += obj_label

                                save_image = True

                        if save_image == True:

                            # create a new label file
                            with open(out_label_path, 'w') as yolo_label_file:
                                yolo_label_file.write(yolo_label_txt)

                            cv2.imwrite(out_image_path, im)
                            #cv2.imshow('image', im)
                            #cv2.waitKey(0)

                            save_image = False
                                
            else:
                print("Error: labels folder does not exist inside: " + os.path.join(dataset_path, folder))
                exit(1)

    # find the labels
    # read xml
    # find labels
    # change it
    # save xml

    # como conferir se os conteudos de duas listas sao iguais pytonicamente