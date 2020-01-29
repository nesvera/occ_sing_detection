import cv2
import numpy
import math

lline_xa = 0
lline_ya = 358
lline_xb = 249
lline_yb = 263

rline_xa = 512
rline_ya = 512
rline_xb = 340
rline_yb = 263

mouse_x = 0
mouse_y = 0

def mouse_handler(event, x, y, flags, param):
    global mouse_x, mouse_y

    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_x = x
        mouse_y = y

if __name__ == "__main__":

    cap = cv2.VideoCapture("/home/nesvera/Documents/neural_nets/object_detection/occ_sign_detection/data/footages/run_04-09-19_20-35.avi")

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mouse_handler)

    ret, frame = cap.read()

    while True:

        #ret, frame = cap.read()
        #print(frame.shape)

        if ret:

            left_value = mouse_x*(lline_ya-lline_yb) + mouse_y*(lline_xb-lline_xa) + lline_xa*lline_yb - lline_xb*lline_ya
            right_value = mouse_x*(rline_ya-rline_yb) + mouse_y*(rline_xb-rline_xa) + rline_xa*rline_yb - rline_xb*rline_ya

            print(mouse_x, mouse_y)
            print(left_value)
            print(right_value)
            print()

            cv2.line(frame,
                     (lline_xa, lline_ya),
                     (lline_xb, lline_yb),
                     (0,255,0),
                     2)

            cv2.line(frame,
                     (rline_xa, rline_ya),
                     (rline_xb, rline_yb),
                     (0,255,0),
                     2)

            cv2.imshow("image", frame)
            cv2.waitKey(1)