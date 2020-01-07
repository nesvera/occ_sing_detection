import numpy as np
import csv
import os
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    
    in_folder = "/home/nesvera/Documents/neural_nets/object_detection/occ_sign_detection/data/raw_dataset"
    file_conversion = "/home/nesvera/Documents/neural_nets/object_detection/occ_sign_detection/data/config/cvt_names.txt"

    label_dict = {}

    with open(file_conversion, 'r') as f:        
        line = f.readline()
        while len(line) > 0:
            line = line.strip()
            label_old, label_new = line.split(';')
            label_dict[label_old] = label_new
            line = f.readline()
    f.close()

    # read all folders
    sub_folder = os.listdir(in_folder)

    for i, folder in enumerate(sub_folder):

        label_folder = os.path.join(os.path.join(in_folder, folder, "labels"))

        if os.path.isdir(label_folder):
            label_files = os.listdir(label_folder)

            for j, file in enumerate(label_files):

                print("Folder " + str(i) + "/" + str(len(sub_folder)) + " - File: " + str(j) + "/" + str(len(label_files)))
                
                if file.endswith(".xml"):

                    tree = ET.parse(os.path.join(label_folder, file))
                    raiz = tree.getroot()

                    for obj_label in raiz.findall('object'):
                        obj_name = obj_label.find("name").text
                        
                        obj_label.find("name").text = label_dict[obj_name]

                        #print(obj_name, obj_label.find("name").text)

                    tree.write(os.path.join(label_folder, file))

    # find the labels
    # read xml
    # find labels
    # change it
    # save xml

    # como conferir se os conteudos de duas listas sao iguais pytonicamente