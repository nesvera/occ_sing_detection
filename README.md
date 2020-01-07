REMEMBER:
    - The image used as input for input must be in RGB colorspace
    - The bounding boxes are represented in fractional format ([0,1]) in the train phases
    - The bounding boxes are represented in normal values in the annotation file ([0,width])
    - There is a main folder to keep all the labeled records

How to install:

1. Clone repo

2. Pull submodules (labelImg)

    git submodule update --init --recursive

3. Install requirements

3.1. Install environment

3.2. Install labelImg

    workon pytorch
    sudo apt-get install pyqt5-dev-tools
    pip install -r requirements/requirements-linux-python3.txt
    make qt5py3

How to prepare a dataset:

1. Record some footage and save it as run_day-month-year_hour-minute.avi (mp4,avi)

2. Convert the video to images

    python convert_video_to_images.py --video [VIDEO_PATH] --output [OUTPUT_PATH] --freq [FPS]
    python convert_video_to_images.py --video data/footages/bosch19_04.avi --output data/raw_dataset --freq 10

    This script will create a folder tree like:
    - run_day-month-year_hour-minute
        - images
            - run_day-month-year_hour-minute_1.jpg
            - run_day-month-year_hour-minute_2.jpg
            - run_day-month-year_hour-minute_3.jpg
        - labels

3. Manually, look all images that were converted, and delete images that are:
    - Repeated
    - Bad quality
    - Images without a single object or with objects that far away

    OBS: the remaining images must be labeled, then take care to not leave some bad image here

4. Check the following files to see if all the labels that are going to be used are presented.
    - file config labelimg
    - file que tem a conversao de label pra numero

4. Open labelImg:
    
    python3 labelImg/labelImg.py [IMAGE_PATH] dataset/data/labelimg_classes.txt
    python labelImg/labelImg.py data/raw_dataset/run_04-09-19_20-35/ data/config/occ_traffic.names

5. Configure labelImg:
5.1. Change path to save the labels:
    - Click in "Change Save Dir"
    - Select the "labels" folder inside the folder created by the conversion script

5.2. Change save format:
    - Select "PascalVOC"

6. Label the images
    You must create a new rectangle box, define the bounding box of the object and select the correct label for it

    OBS: the remaining images must be labeled

    Shortcuts/Hotkeys
        - Ctrl + s      = Save
        - w             = Create a rect box
        - d             = Next image
        - a             = Previous image
        - del           = Delete the selected rect box
        - Ctrl++        = Zoom in
        - Ctrl--        = Zoom out

7. Place the record folder that was created inside the main dataset folder

8. Check the frequency distribution of the classes inside de dataset. It is NOT recommended to have a big disparity
   of labeled objects between the classes. 

   Run the script below inside de dataset main folder, where all the labeld records were placed.

   python show_dataset_distribuition.py --in_folder /path/to/main/dataset/folder
   python show_dataset_distribuition.py --in_folder data/raw_dataset/

9. Split label image in N regions
    - Currently split in 3 regions with overlap

    Check parameters in configuration file
    /data/config/preprocessing.yml

    Preprocess:
    python dataset_preprocessing.py --in_folder data/raw_dataset --out_folder ./data/dataset/teste --config data/config/preprocessing.yml --debug 0 --save 1

    It is possible to visualize the output of this process enabling debug and disabling save (--debug 1 --save 0)

How to train:

1. Configure the config file (e.g asdfjakl) with the crop, dimension, number of crops...

2. Run script that will split the dataset, and will create the a dataset to be used for training

3. Configure the config file for training, pointing to the dataset address, ...

How to deploy:

1. aaaaaaaaaaaaaaaa