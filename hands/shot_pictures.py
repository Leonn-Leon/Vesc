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

inds = np.arange(len(names))
print(names)
print(inds)

for i in names:
    if not os.path.exists(directory+i):
        os.makedirs(directory+i)

dc = DepthCamera()

skip = 0
for ind, i in enumerate(names):
    print(i + f' [{ind}]')

_model = YOLO('hands/models/best.pt')

while True:
    # ret, frame = cap.read()
    ret, depth_frame, color_frame = dc.get_frame()
    skip += 1
    if skip < 7:
        continue

    results = _model.predict(color_frame, verbose=False, conf=0.3)
    hand_box = []
    for r in results:
        annotator = Annotator(color_frame)
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            if c == 0:
                hand_box = b
            annotator.box_label(b, _model.names[int(c)])
    img = annotator.result()

    skip = 0
    cv2.imshow('video', color_frame)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('p'):
        cv2.waitKey(0)
    elif k != -1:
        k = int(k) - 48
        clas = names[k] + '/'
        # np.save(directory + clas + str(inds[k]) + '.npy', color_frame)
        hand = color_frame[hand_box[1]:hand_box[3], hand_box[0]:hand_box[2]]
        cv2.imwrite(directory + clas + str(inds[k]) + '.png', hand)
        print(names[k])
        inds[k] += 1

dc.release()
cv2.destroyAllWindows()