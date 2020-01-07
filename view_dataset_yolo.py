import cv2
import argparse
import os
import random

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert dataset from VOC format to Yolo")
    parser.add_argument("--dataset",
                        dest="dataset",
                        required=True,
                        help="Path to the dataset, or collection of datasets")
    parser.add_argument("--class_names",
                        dest="class_names",
                        required=True,
                        help="File defining label names")

    args = parser.parse_args()

    dataset_path = args.dataset
    if os.path.isdir(dataset_path) == False:
        print("Error: input path is not a folder or it does not exist")
        exit(1)

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

            class_names_dict[class_counter] = file_line
            class_counter += 1

            file_line = f.readline()

    images_folder = os.path.join(os.path.join(dataset_path, "images"))
    labels_folder = os.path.join(os.path.join(dataset_path, "labels"))

    # create a list with all labels
    labels_list = list()
    if os.path.isdir(labels_folder):
        label_files = os.listdir(labels_folder)
        for file in label_files:
            labels_list.append(os.path.join(labels_folder, file))

            continue

    # display images and labels
    while True:

        label = random.choice(labels_list)
        filename = (label.split(".txt")[0]).split("/")[-1]
        image_path = images_folder + "/" + filename + ".png"
        
        image = cv2.imread(image_path)
        
        with open(label, 'r') as label_yolo:
            label_line = label_yolo.readline()
            
            while len(label_line) > 1:
                label_line = label_line.strip()
                label_fields = label_line.split(" ")

                obj_num =       int(label_fields[0])
                obj_x_center =  float(label_fields[1])*image.shape[1]
                obj_y_center =  float(label_fields[2])*image.shape[0]
                obj_weight =    float(label_fields[3])*image.shape[1]
                obj_height =    float(label_fields[4])*image.shape[0]

                obj_class = class_names_dict[obj_num]
                obj_xmin = int(obj_x_center - obj_weight/2.)
                obj_ymin = int(obj_y_center - obj_height/2.)
                obj_xmax = int(obj_x_center + obj_weight/2.)
                obj_ymax = int(obj_y_center + obj_height/2.)

                cv2.rectangle(image,
                              (obj_xmin, obj_ymin),
                              (obj_xmax, obj_ymax),
                              (0,255,0),
                              2)

                cv2.putText(image,
                           obj_class,
                           (int(obj_x_center), int(obj_y_center)),
                           cv2.FONT_HERSHEY_SIMPLEX,
                           0.3,
                           (255, 255, 255),
                           1)

                label_line = label_yolo.readline()

        cv2.imshow("image", image)
        cv2.waitKey(0)
                         
    print(len(labels_list))
    print(labels_list)

# receber um pasta
# ler todas as labels
# mostrar imagens aleatoriamente com bounding box e classes