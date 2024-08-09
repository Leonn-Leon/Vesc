import cv2
from time import sleep
import os
import numpy as np
from realsense_depth import *
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

names = ['follow', 'stop', 'base', 'no_command']
inds = []
directory = 'data/images/'
if not os.path.exists(directory):
    os.makedirs(directory)

ind = []
for i in names:
    l = [int(i[:-4]) for i in os.listdir(directory + i) if i[:-4].isnumeric()]
    inds += [sorted(l)[-1]]

print(names)
print(inds)

for i in names:
    if not os.path.exists(directory+i):
        os.makedirs(directory+i)

real_sense = False
if real_sense:
    dc = DepthCamera()
else:
    cap = cv2.VideoCapture(0)

skip = 0
for ind, i in enumerate(names):
    print(i + f' [{ind}]')

_model = YOLO('models/best.pt')

while True:
    if real_sense:
        ret, depth_frame, color_frame = dc.get_frame()
    else:
        ret, color_frame = cap.read()
    skip += 1
    if skip < 5:
        continue
    skip = 0

    results = _model.predict(color_frame, verbose=False, conf=0.3)
    hand_box = []
    for r in results:
        annotator = Annotator(color_frame.copy())
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            if c == 0:
                hand_box = b
            annotator.box_label(b, _model.names[int(c)])
    img = annotator.result()


    cv2.imshow('video', img)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('p'):
        cv2.waitKey(0)
    elif k != -1:
        k = int(k) - 48
        clas = names[k] + '/'
        # np.save(directory + clas + str(inds[k]) + '.npy', color_frame)
        hand_box = [int(i) for i in hand_box]
        print(hand_box)
        hand = color_frame[hand_box[1]:hand_box[3], hand_box[0]:hand_box[2]]
        cv2.imwrite(directory + clas + str(inds[k]) + '.png', hand)
        print(names[k])
        inds[k] += 1

if real_sense:
    dc.release()
else:
    cap.release()
cv2.destroyAllWindows()