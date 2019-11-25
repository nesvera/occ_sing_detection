import sys
import os
import cv2
import argparse
import xml.etree.ElementTree as ET
from data.config import classes
import numpy as np
import json
import yaml

def main():
    
    parser = argparse.ArgumentParser(description='Process labeled images to generate files to be used during the training phase')
    parser.add_argument('--in_folder',
                        dest='input_dataset_path',
                        required=True,
                        help='Path to the folder with labeled records')
    parser.add_argument('--out_folder',
                        dest='output_path',
                        required=True,
                        help='Path to the folder that will receive traning files')
    parser.add_argument('--config',
                        dest='config_file',
                        required=True,
                        help='Configuration file with dimensions from original images and the output images')
    parser.add_argument('--debug',
                        dest='debug',
                        required=False,
                        default=False,
                        type=int,
                        help='Debug mode enables image visualization')
    parser.add_argument('--save',
                        dest='save',
                        required=False,
                        default=True,
                        type=int,
                        help='Dont save the images and annotation')

    args = parser.parse_args()

    debug_ = bool(args.debug)
    save_ = bool(args.save)

    config_path = args.config_file
    if os.path.exists(config_path) == False:
        print("Error: Config file does not exist")
        exit(1)

    config = None
    with open(config_path, 'r') as cf:
        config = yaml.safe_load(cf)

    dataset_in_path = args.input_dataset_path
    if os.path.isdir(dataset_in_path) == False:
        print("Error: Input path is not a directory")
        exit(1)

    dataset_out_path = args.output_path
    if os.path.exists(dataset_out_path) == True:
        print("Error: Output path already exists")
        exit(1)

    if save_ == True:
        os.mkdir(dataset_out_path)

    input_vertical_center = int(config['SPLIT']['INPUT']['HORIZON'])
    in_roi_height =         int(config['SPLIT']['INPUT']['ROI_HEIGHT'])
    in_roi_width =          int(config['SPLIT']['INPUT']['ROI_WIDTH'])
    out_width =             int(config['SPLIT']['OUTPUT']['WIDTH'])
    out_height =            int(config['SPLIT']['OUTPUT']['HEIGHT'])
    num_slices =            int(config['SPLIT']['INPUT']['NUM_SPLITS'])
    split_roi_width =       int(config['SPLIT']['INPUT']['SPLIT_ROI_WIDTH'])
    intersection_overlap =  float(config['SPLIT']['INPUT']['INTERSEC_OVERLAP'])

    roi_height_low = input_vertical_center - int(in_roi_height/2)
    roi_height_up = input_vertical_center + int(in_roi_height/2)

    if (roi_height_low <= 0) or (roi_height_up <= 0):
        print("Error: ROI dimensions must be positive")
        exit(1)

    all_annotation_list = list()

    dataset_annotation_path = dataset_out_path + "/complete_annotation.json"
    train_annotation_path = dataset_out_path + "/train_annotation.json"
    test_annotation_path = dataset_out_path + "/test_annotation.json"

    # get all labeled record
    list_records = os.listdir(dataset_in_path)
    for record_i, record in enumerate(list_records):
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
        for image_file_i, image_file in enumerate(all_images_record):

            print("Record [{0}/{1}] - Image[{2}/{3}]".format(record_i+1,
                                                             len(list_records),
                                                             image_file_i+1,
                                                             len(all_images_record)))

            image_path = record_images_path + "/" + image_file

            image_filename = image_file.split(".")[0]
            annotation_path = record_labels_path + "/" + image_filename + ".xml"

            image_labels_list = list()
            image_boxes_list = list()

            # read annotation file
            if os.path.exists(annotation_path) == True:
                label_file = ET.parse(annotation_path)
                xml_root = label_file.getroot()

                for obj in xml_root.iter('object'):

                    label = obj.find('name').text.lower().strip()
                    image_labels_list.append(label)

                    bb = obj.find('bndbox')
                    # labelImg saves bb between [1, image_size]
                    xmin = int(bb.find('xmin').text) -1
                    ymin = int(bb.find('ymin').text) -1
                    xmax = int(bb.find('xmax').text) -1
                    ymax = int(bb.find('ymax').text) -1
                    image_boxes_list.append([xmin, ymin, xmax, ymax])

            else:
                print("Warning: Annotation was not found, the image will be removed")
                os.remove(image_path)
                continue

            # load image
            image = cv2.imread(image_path)
            
            split_size = int(image.shape[1]/num_slices)        # image_width/num_slicess
            
            for split in range(num_slices):

                if split == 0:
                    split_xmin = 0
                    split_ymin = roi_height_low
                    split_xmax = split_roi_width
                    split_ymax = roi_height_up

                    split_image = image[split_ymin:split_ymax, split_xmin:split_xmax].copy()
                    split_image = cv2.resize(split_image, (out_width, out_height))

                    # check for each object if its inside the split with certain overlap
                    split_boxes, split_labels = find_obj_split(image_boxes_list, image_labels_list,
                                                               [split_xmin, split_ymin, split_xmax, split_ymax],
                                                               intersection_overlap,
                                                               split_roi_width, in_roi_height)

                    # if there are any annotation inside the split, save
                    if len(split_boxes) > 0:
                        split_image_path = os.path.abspath(dataset_out_path + "/" + image_filename + "@" + str(split) + ".png")
                        
                        if debug_ == True:
                            for bb in split_boxes:
                                cv2.rectangle(split_image, 
                                              (int(bb[0]*out_width), int(bb[1]*out_height)), 
                                              (int(bb[2]*out_width), int(bb[3]*out_height)), 
                                              (0,255,0), 1)
                            cv2.imshow(str(split), split_image)
                        
                        if save_ == True: 
                            cv2.imwrite(split_image_path, split_image)    

                        split_annotation = {'image': split_image_path,
                                            'boxes': split_boxes,
                                            'labels': split_labels}

                        all_annotation_list.append(split_annotation)

                        # save split imaga, add image and annotation to a file


                elif split ==  (num_slices-1):
                    split_xmin = image.shape[1] -split_roi_width
                    split_ymin = roi_height_low
                    split_xmax = image.shape[1]
                    split_ymax = roi_height_up
                    
                    split_image = image[split_ymin:split_ymax, split_xmin:split_xmax].copy()
                    split_image = cv2.resize(split_image, (out_width, out_height))

                    # check for each object if its inside the split with certain overlap
                    split_boxes, split_labels = find_obj_split(image_boxes_list, image_labels_list,
                                                               [split_xmin, split_ymin, split_xmax, split_ymax],
                                                               intersection_overlap,
                                                               split_roi_width, in_roi_height)

                    # if there are any annotation inside the split, save
                    if len(split_boxes) > 0:
                        split_image_path = os.path.abspath(dataset_out_path + "/" + image_filename + "@" + str(split) + ".png")
                        
                        if debug_ == True:
                            for bb in split_boxes:
                                cv2.rectangle(split_image, 
                                              (int(bb[0]*out_width), int(bb[1]*out_height)), 
                                              (int(bb[2]*out_width), int(bb[3]*out_height)), 
                                              (0,255,0), 1)
                            cv2.imshow(str(split), split_image)
                        
                        if save_ == True: 
                            cv2.imwrite(split_image_path, split_image)   

                        split_annotation = {'image': split_image_path,
                                            'boxes': split_boxes,
                                            'labels': split_labels}

                        all_annotation_list.append(split_annotation)

                        # save split imaga, add image and annotation to a file
                    

                else:
                    split_center = int((2*split+1)*split_size/2.)

                    split_xmin = split_center -int(split_roi_width/2)
                    split_ymin = roi_height_low
                    split_xmax = split_center +int(split_roi_width/2)
                    split_ymax = roi_height_up

                    split_image = image[split_ymin:split_ymax, split_xmin:split_xmax].copy()
                    split_image = cv2.resize(split_image, (out_width, out_height))

                    # check for each object if its inside the split with certain overlap
                    split_boxes, split_labels = find_obj_split(image_boxes_list, image_labels_list,
                                                               [split_xmin, split_ymin, split_xmax, split_ymax],
                                                               intersection_overlap,
                                                               split_roi_width, in_roi_height)

                    # if there are any annotation inside the split, save
                    if len(split_boxes) > 0:
                        split_image_path = os.path.abspath(dataset_out_path + "/" + image_filename + "@" + str(split) + ".png")
                        
                        if debug_ == True:
                            for bb in split_boxes:
                                cv2.rectangle(split_image, 
                                              (int(bb[0]*out_width), int(bb[1]*out_height)), 
                                              (int(bb[2]*out_width), int(bb[3]*out_height)), 
                                              (0,255,0), 1)
                            cv2.imshow(str(split), split_image)
                        
                        if save_ == True: 
                            cv2.imwrite(split_image_path, split_image)   

                        split_annotation = {'image': split_image_path,
                                            'boxes': split_boxes,
                                            'labels': split_labels}

                        all_annotation_list.append(split_annotation)

                        # save split imaga, add image and annotation to a file

            if debug_ == True:
                cv2.line(image, (0, input_vertical_center), (image.shape[1], input_vertical_center), (0,255,0), 3)
                cv2.rectangle(image, (0, roi_height_low), (image.shape[1], roi_height_up), (255,0,0), 3)
                cv2.imshow('image', image)
                if cv2.waitKey(0) == ord('s'):
                    with open(dataset_annotation_path, 'w') as f:
                        json.dump(all_annotation_list, f)

    print()
    print("Saving annotation file")

    # save annotation file
    if save_ == True:
        with open(dataset_annotation_path, 'w') as f:
            json.dump(all_annotation_list, f)

def intersection_area(box_1, box_2):
    lower_bound = np.maximum(box_1[:2], box_2[:2])
    upper_bound = np.minimum(box_1[2:], box_2[2:])

    dif = np.maximum(upper_bound - lower_bound, 0)

    return dif[0]*dif[1]

def find_obj_split(boxes, labels, split, intersection_overlap, in_width, in_height):

    boxes_list = list()
    labels_list = list()

    for box_i, box in enumerate(boxes):
        box_area = (box[2]-box[0])*(box[3]-box[1])
        intersec_area = intersection_area([split[0], split[1], split[2], split[3]], box)
        
        if intersec_area > intersection_overlap*box_area:
            box_xmin = (box[0] - split[0])/in_width
            box_ymin = (box[1] - split[1])/in_height
            box_xmax = min((box[2] - split[0]), split[2])/in_width
            box_ymax = min((box[3] - split[1]), split[3])/in_height

            box_xmin = max(box_xmin, 0)
            box_ymin = max(box_ymin, 0)
            box_xmax = min(box_xmax, 1)
            box_ymax = min(box_ymax, 1)
            
            boxes_list.append([box_xmin, box_ymin, box_xmax, box_ymax])
            labels_list.append(labels[box_i])

    return boxes_list, labels_list

            
if __name__ == "__main__":
    main()