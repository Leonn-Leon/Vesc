import cv2
import os
import numpy as np
from ML import start_ML
from skimage import feature

rev_dict = {
    'follow':['stop', 'base', 'no_command']
}
dir_start = '../hands/data/images/'

for i, name in enumerate(rev_dict.keys()):
    print(name)

    dir = 'data/ML/' + name + '/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    path = dir_start + name + '/'
    files = os.listdir(path)
    X = []
    y = []
    for i in files:
        # image = np.load(path + i)
        image = cv2.imread(path + i)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (128, 128))
        hog = feature.hog(image, orientations=9,
                                   pixels_per_cell=(4, 4), cells_per_block=(2, 2),
                                   block_norm='L2-Hys', visualize=False, transform_sqrt=True)
        X += [hog]

    y += [0] * len(files)


    for ind, j in enumerate(rev_dict[name]):
        path_rev = dir_start + j + '/'
        files_rev = os.listdir(path_rev)
        for i in files_rev:
            # image = np.load(path_rev + i)
            image = cv2.imread(path_rev + i)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (128, 128))
            hog = feature.hog(image, orientations=9,
                                       pixels_per_cell=(4, 4), cells_per_block=(2, 2),
                                       block_norm='L2-Hys', visualize=False, transform_sqrt=True)
            X += [hog]
        y += [ind+1] * len(files_rev)

    X = np.array(X)
    np.save(dir + 'X.npy', X)
    y = np.array(y)
    np.save(dir + 'y.npy', y)

print('...ML...')
start_ML()