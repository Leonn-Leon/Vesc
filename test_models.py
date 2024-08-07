import os
import cv2
from skimage import feature
from realsense_depth import *
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

_model = YOLO('hands/models/best.pt')

real_sense = False
if real_sense:
    dc = DepthCamera()
else:
    cap = cv2.VideoCapture(0)

last_command = ''
while True:
    if real_sense:
        ret, depth_frame, color_frame = dc.get_frame()
    else:
        ret, color_frame = cap.read()

    results = _model.predict(color_frame, verbose=False, conf=0.3)
    for r in results:
        annotator = Annotator(color_frame)
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            if c == 0:
                print(b, color_frame.shape)
            annotator.box_label(b, _model.names[int(c)])
    img = annotator.result()

    cv2.imshow('YOLO Detection', img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('p'):
        cv2.waitKey(0)

    # if _command != last_command:
    #     last_command = _command
    #     print(_command)