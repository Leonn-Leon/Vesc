import cv2
from time import sleep
import os
import numpy as np
from realsense_depth import *

names = ['0', '1', '2', '3']
inds = []
directory = 'data/images/'

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

while True:
    # ret, frame = cap.read()
    ret, depth_frame, color_frame = dc.get_frame()
    skip += 1
    if skip < 7:
        continue
    # sleep(0.005)
    skip = 0
    # depth_frame[depth_frame > 6000] = 6000
    # depth_frame[depth_frame < 500] = 0
    cv2.imshow('video', depth_frame)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('p'):
        cv2.waitKey(0)
    elif k != -1:
        k = int(k) - 48
        clas = names[k] + '/'
        np.save(directory + clas + str(inds[k]) + '.npy', depth_frame)
        # cv2.imwrite(directory + clas + str(inds[k]) + '.png', depth_frame)
        print(names[k])
        inds[k] += 1

dc.release()
cv2.destroyAllWindows()