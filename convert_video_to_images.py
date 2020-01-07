import sys
import os
import cv2
import argparse

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Convert videos in a sequence of images')
    parser.add_argument('--video',
                        dest='input_video_path',
                        required=True,
                        help='Path to the folder with recorded videos')
    parser.add_argument('--output',
                        dest='output_folder',
                        required=True,
                        help='Path to the folder that will receive folders with images')
    parser.add_argument('--freq',
                        dest='output_fps',
                        required=False,
                        default=10,
                        help='FPS value to save the images')

    args = parser.parse_args()

    input_video_path = args.input_video_path
    if os.path.exists(input_video_path) == False:
        print('Error: video not found!')
        exit(1)

    video_name = input_video_path.split("/")[-1]
    video_name = video_name.split(".")[0]
    
    dataset_output_path = args.output_folder
    if os.path.isdir(dataset_output_path) == False:
        print('Error: output path is not a directory, or not exist!')
        exit(1)

    dataset_output_path = dataset_output_path + "/" + video_name
    if os.path.isdir(dataset_output_path) == True:
        print('Error: a folder already exist with this name, remove the old folder to continue')
        exit(1)

    image_output_path = dataset_output_path + "/images"
    label_path = dataset_output_path + "/labels"
    
    os.mkdir(dataset_output_path)
    os.mkdir(image_output_path) 
    os.mkdir(label_path)

    fps_output = float(args.output_fps)
    if fps_output <= 0:
        print('Error: fps output value must be positive!')

    video = cv2.VideoCapture(input_video_path)
    fps_input = video.get(cv2.CAP_PROP_FPS)
    
    fps_dif = int(fps_input/fps_output)

    frame_counter = 0
    while True:

        ret, frame = video.read()
        if ret == False:
            break

        if frame_counter % fps_dif == 0:
            
            image_filename = image_output_path + "/" + video_name + "_" + str(frame_counter) + ".png"
            cv2.imwrite(image_filename, frame)

        cv2.imshow("Video", frame)
        cv2.waitKey(1)

        frame_counter += 1