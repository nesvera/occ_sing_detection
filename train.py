import torch

import cv2

from utils import datasets
from data.config import classes

def main():

    data_folder = "/home/nesvera/Documents/neural_nets/object_detection/occ_sign_detection/data/dataset/teste/"
    train_dataset = datasets.SignDataset(data_folder,
                                         classes.label_map,
                                         dims=(224,224))

    train_loader = torch.utils.data.DataLoader(train_dataset,
                                               batch_size=2,
                                               shuffle=False,
                                               num_workers=4,
                                               collate_fn=train_dataset.collate_fn,
                                               pin_memory=True)

    for key in classes.label_map.keys():
        print(key, classes.label_map[key])

    for i, (images, boxes, labels) in enumerate(train_loader):

        images = images.numpy()[0]
        images = images.transpose(1,2,0)

        print("-----")
        print(boxes)
        print(labels)

        height = images.shape[0]
        widht = images.shape[1]

        boxes = boxes[0][0]
        print(boxes)

        images =cv2.rectangle(images, 
                      (int(boxes[0]*widht), int(boxes[1]*height)), 
                      (int(boxes[2]*widht), int(boxes[3]*height)), 
                      (0,255,0), 3)

        cv2.imshow("image", images)
        cv2.waitKey(0)


if __name__ == "__main__":
    main()