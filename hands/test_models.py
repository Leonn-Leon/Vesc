import os
import pickle
import cv2
from skimage import feature
from realsense_depth import *

model_name = os.listdir('data/ML/models')[0]
with open('data/ML/models/' + model_name, 'rb') as file:
    _model = pickle.load(file)

last_command = ''
dc = DepthCamera()
while True:
    ret, depth_frame, color_frame = dc.get_frame()
    image = cv2.resize(color_frame, (512, 512))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hog = feature.hog(image, orientations=9,
                      pixels_per_cell=(8, 8), cells_per_block=(2, 2),
                      block_norm='L2-Hys', visualize=False, transform_sqrt=True).reshape(1, -1)
    cv2.imshow('video', color_frame)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('p'):
        cv2.waitKey(0)

    _command = _model.predict(hog)[0]
    #if _command != last_command:
     #   last_command = _command
    print(_command)