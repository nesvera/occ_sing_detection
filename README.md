REMEMBER:
    - The image used as input must be in RGB colorspace
    - Darknet uses bounding boxes in fractional format ([0,1]) 
    - The annotations from labelImg must be converted to YOLO format
    - There is a main dataset folder that contains sub-folders with images and annotation of each recorded video

How to install:

1. Clone repo

2. Pull submodules (labelImg)

    git submodule update --init --recursive

3. Install requirements

3.1. Install environment

    https://virtualenvwrapper.readthedocs.io/en/latest/

3.2. Install labelImg

    workon pytorch
    sudo apt-get install pyqt5-dev-tools
    pip install -r requirements/requirements-linux-python3.txt
    make qt5py3

How to prepare a dataset:

0. Check if the ".names" file contains the names of all classes that should be detected. This file relates the 
name of the class to the number used during the training and test phase.
    - occ_sign_detection/data/config/yolov3-occ_traffic_sign.names

1. Record some video

2. Convert the video to images. This script receives the path from a video, and saves the images at a certain
frame rate. It will create a folder with the name passed as output path.

    python convert_video_to_images.py --video [VIDEO_PATH] --output [OUTPUT_PATH] --freq [FPS]
    python convert_video_to_images.py --video data/footages/bosch19_04.avi --output data/raw_dataset --freq 10


    This script creates a FOLDER ("video_set_folder") inside the OUTPUT_PATH:
    - footage_set_folder
        - images
            - run_day-month-year_hour-minute_1.jpg
            - run_day-month-year_hour-minute_2.jpg
            - run_day-month-year_hour-minute_3.jpg
        - labels

3. Open labelImg with the video_set_folder and classes_names:
    
    python3 labelImg/labelImg.py [IMAGE_PATH] [CLASSES_NAMES_PATH]
    python labelImg/labelImg.py data/raw_dataset/run_04-09-19_20-35/ data/config/yolov3-occ_traffic_sign.names

4. Configure labelImg:
4.1. Change the path to save the labels:
    - Click in "Change Save Dir"
    - Select the "labels" folder inside the video_set_folder

4.2. Change save format:
    - Select "PascalVOC"

5. Label images
    You must create a new rectangle box, define the bounding box of the object and select the correct label for it

    Shortcuts/Hotkeys
        - Ctrl + s      = Save
        - w             = Create a rect box
        - d             = Next image
        - a             = Previous image
        - del           = Delete the selected rect box
        - Ctrl++        = Zoom in
        - Ctrl--        = Zoom out

6. Place the video_set_folder folder inside the main dataset folder

8. Check the frequency distribution of the classes inside de dataset. It is NOT recommended to have a big disparity
   of labeled objects between the classes. 

   Run the script below inside de dataset main folder, where all the labeld records were placed.

   python show_dataset_distribuition.py --in_folder /path/to/main/dataset/folder
   python show_dataset_distribuition.py --in_folder data/raw_dataset/

9. Convert dataset from VOC format to YOLO format.
    VOC format has more information about the label, then it is better to keep the original labels in this format

    python convert_voc_to_yolo.py --dataset data/raw_dataset --out_folder data/dataset_yolo_format --class_names data/config/yolov3-occ_traffic_sign.names

10. It is possible to visualize the dataset (just to check)

    python view_dataset_yolo.py --dataset data/dataset_yolo_format/ --class_names data/config/yolov3-occ_traffic_sign.names 

11. Copy dataset to the computer that is going to be used to train.
    
    scp -r <dataset_folder> <computer_user>@<ip>:<path_to_folder>

12. Copy also the script to split the dataset

    scp split_dataset_yolo.py feaf-seat-1@141.41.32.122:/home/feaf-seat-1/Documents/nesvera/darknet

13. This script MUST be executed in the computer that is going to be used to train.
    This must be done in this way, once that darknet uses training files with full path for the images

    python split_dataset_yolo.py --dataset <dataset_folder> --train_per <percentage_of_images_train>
    python split_dataset_yolo.py --dataset ./occ_sign_yolo_dataset/ --train_perc 0.9


Download darknet:

How to train YOLOV3 from zero:

1. Download Yolo base weights (classifier)

    cd darknet
    wget https://pjreddie.com/media/files/darknet53.conv.74

2. Modify .data file

    cp cfg/voc.data yolov3_occ_traffic_sign.data
    nano yolov3_occ_traffic_sign.data
  
    classes= n
    last filters = [4 + 1 + n]*3
    train  = <path-to-train-dataset>
    valid  = <path-to-validation-dataset>
    names = data/occ_traffic_sign.names
    backup = backup

3. Copy the .cfg from tiny-yolo. Change batch size and subdivisions for training.
   Change number of classes and filters. The .cfg file must be placed inside the cfg/ folder

    cp cfg/yolov3-tiny.cfg cfg/yolov3-occ-traffic-sign.cfg

    nano cfg/yolov3-occ-traffic-sign.cfg

    # Testing
    #batch=1
    #subdivisions=1
    # Training
    batch=64
    subdivisions=4

    in lines 135 and 177, classes = n_classes
    in lines 127 and 171, filters = [4 + 1 + n_classes]*3
    
4. Start training. The weights are going to be saved inside "backup" folder
    
    ./darknet detector train <path to .data file> <path to .cfg file> <path to base weights>
    ./darknet detector train yolov3_occ_traffic_sign.data cfg/yolov3-occ-traffic-sign.cfg weights/darknet53.conv.74 

5. Continue training from a backup

    ./darknet detector train <path to .data file> <path to .cfg file> <path to trained weight>
    ./darknet detector train yolov3-occ_traffic_sign.data cfg/yolov3-occ-traffic-sign.cfg backup/yolov3-occ-traffic-sign.backup 
