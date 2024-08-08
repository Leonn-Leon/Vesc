import os
import cv2
import numpy as np
from skimage import feature
from realsense_depth import *
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import pickle

_model = YOLO('hands/models/best.pt')
with open('hands/models/follow.pkl', 'rb') as file:
    hand_model = pickle.load(file)

print("Модельки Открыты!")

names = ['follow', 'stop', 'base', 'no_command']

real_sense = False
if real_sense:
    dc = DepthCamera()
else:
    cap = cv2.VideoCapture(0)

last_command = ''
print("Получилось поключиться к камере!")
while True:
    if real_sense:
        ret, depth_frame, color_frame = dc.get_frame()
    else:
        ret, color_frame = cap.read()

    results = _model.predict(color_frame, verbose=False, conf=0.3)
    hand_box = [0,0,0,0,0]
    for r in results:
        annotator = Annotator(color_frame.copy())
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            if c == 0:
                _square = (b[2]-b[0])*(b[3]-b[1])
                if hand_box[4] < _square:
                    hand_box = [int(i) for i in b] + [_square]
                    # print(hand_box)
            annotator.box_label(b, _model.names[int(c)])
    img = annotator.result()
    image = np.zeros((128, 128))
    if hand_box[4] > 10:
        image = color_frame[hand_box[1]:hand_box[3], hand_box[0]:hand_box[2]]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (128, 128))
        hog = feature.hog(image, orientations=9,
                          pixels_per_cell=(8, 8), cells_per_block=(2, 2),
                          block_norm='L2-Hys', visualize=False, transform_sqrt=True)
        res = hand_model.predict(hog.reshape(1, -1))
        print(res)

    cv2.imshow('YOLO Detection', img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('p'):
        cv2.waitKey(0)

    # if _command != last_command:
    #     last_command = _command
    #     print(_command)

if real_sense:
    dc.release()
else:
    cap.release()