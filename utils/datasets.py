import torch
from torch.utils.data import Dataset
import torchvision.transforms.functional as FT

import os
import json
import cv2
import numpy as np
from PIL import Image
import random

class SignDataset(Dataset):
    """
    A PyTorch Dataset class to be used in a PyTorch DataLoader to create batches.

    """

    def __init__(self, data_folder, label_map, dims=(224,224), split=None):
        """
        Parameters
        ----------
        data_folder : str
            Path to the dataset folder
        label_map : dict
            List with all the labels
        dims : tuple
            Tuple with width and height of the image
        split: str
            Select each set to load
            None = all images of the dataset
            train = train set
            test = test set
        """

        complete_annotation_file_path = data_folder + "/complete_annotation.json"
        train_annotation_file_path = data_folder + "/train_annotation.json"
        test_annotation_file_path = data_folder + "/test_annotation.json"

        self.split = split

        self.annotation = None
        if split is None:
            with open(complete_annotation_file_path, 'r') as f:
                self.annotation = json.load(f)

        else:
            self.split = split.lower()

        self.label_map = label_map

        self.dims = dims

        self.mean = [0.259, 0.288, 0.305]
        self.std =  [0.282, 0.292, 0.299]

        #self.mean, self.std = self.find_mean_std()

    def __getitem__(self, i):
        """
        Override the function of torch.Dataset

        Parameters
        ----------
        i : int
            Index
        """

        # Get annotation
        image_path = self.annotation[i]['image']
        boxes = self.annotation[i]['boxes']
        labels = self.annotation[i]['labels']

        # label text to number
        label_map = list()
        for label in labels:
            label_map.append(self.label_map[label])

        boxes = torch.FloatTensor(boxes)
        labels = torch.LongTensor(label_map)

        # read and transform image and convert to RGB
        #image = cv2.imread(image_path)
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image = Image.open(image_path)
        image = self.photometric_distort(image)
        
        # apply transformation
        image = FT.to_tensor(image)
        image = FT.normalize(image, mean=self.mean, std=self.std)

        '''
        if split == train
            - add noise
            - crop maybe
            - 
        '''

        return image, boxes, labels

    def __len__(self):
        return len(self.annotation)

    def collate_fn(self, batch):
        """
        Since each image may have a different number of objects, we need a collate function (to be passed to the DataLoader).

        This describes how to combine these tensors of different sizes. We use lists.

        Note: this need not be defined in this Class, can be standalone.

        Parameters
        ----------
        batch : list
            an iterable of N sets from __getitem__()

        Return:
            a tensor of images, lists of varying-size tensors of bounding boxes, labels
        """

        all_images = list()
        all_boxes = list()
        all_labels = list()

        for image, boxes, labels in batch:
            all_images.append(image)
            all_boxes.append(boxes)
            all_labels.append(labels)

        all_images = torch.stack(all_images, dim=0)

        return all_images, all_boxes, all_labels

    def find_mean_std(self):

        b_ch_list = list()
        g_ch_list = list()
        r_ch_list = list()

        for i in range(len(self.annotation)):
            image_path = self.annotation[i]['image']
            image = cv2.imread(image_path)

            b_ch_list.append(image[:,:,0])
            g_ch_list.append(image[:,:,1])
            r_ch_list.append(image[:,:,2])

        b_ch = np.array(b_ch_list)
        g_ch = np.array(g_ch_list)
        r_ch = np.array(r_ch_list)
        
        mean = [np.mean(b_ch)/255., np.mean(g_ch)/255., np.mean(r_ch)/255.]
        std = [np.std(b_ch)/255., np.std(g_ch)/255., np.std(r_ch)/255.]

        return mean, std

    def photometric_distort(self, image):
        """
        Distort brightness, contrast, saturation, and hue, each with a 50% chance, in random order.

        :param image: image, a PIL Image
        :return: distorted image
        """
        new_image = image

        distortions = [FT.adjust_brightness,
                    FT.adjust_contrast,
                    FT.adjust_saturation,
                    FT.adjust_hue]

        random.shuffle(distortions)

        for d in distortions:
            if random.random() < 0.5:
                if d.__name__ is 'adjust_hue':
                    # Caffe repo uses a 'hue_delta' of 18 - we divide by 255 because PyTorch needs a normalized value
                    adjust_factor = random.uniform(-18 / 255., 18 / 255.)
                else:
                    # Caffe repo uses 'lower' and 'upper' values of 0.5 and 1.5 for brightness, contrast, and saturation
                    adjust_factor = random.uniform(0.5, 1.5)

                # Apply this distortion
                new_image = d(new_image, adjust_factor)

        return new_image
        