REMEMBER:
    - The image used as input for input must be in RGB colorspace
    - The bounding boxes are represented in fractional format ([0,1]) in the train phases
    - The bounding boxes are represented in normal values in the annotation file ([0,width])

How to install:

How to install application to label dataset:

    - Update the git repo inside this repo
    - Follow the installation steps presented by the repository

How to prepare a dataset:

1. Record some footage and save it as run_day-month-year_hour-minute.avi (mp4,avi)

2. Convert the video to images

    python utils/video_to_images.py -i [VIDEO_PATH] -o [OUTPUT_PATH] -f [FPS]
    python utils/video_to_images.py -i dataset/footages/training03.avi -o dataset/raw_dataset/ -f 10

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
    python labelImg/labelImg.py dataset/raw_dataset/run_04-09-19_20-35/ dataset/config/labelimg_classes.txt

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

How to train:

1. Configure the config file (e.g asdfjakl) with the crop, dimension, number of crops...

2. Run script that will split the dataset, and will create the a dataset to be used for training

3. Configure the config file for training, pointing to the dataset address, ...

How to deploy:

1. aaaaaaaaaaaaaaaa