from sklearn.svm import SVC
from sklearn.svm import LinearSVC
import numpy as np
import cv2
from os import listdir, mkdir
from pickle import dump

def start_ML():
    files = listdir('data/ML')
    if 'models' in files:
        files.remove('models')
    else:
        mkdir('models')
    for i in files:
        X = np.load('data/ML/' + i + '/X.npy')
        y = np.load('data/ML/' + i + '/y.npy')
        print(i)
        # if y.max() > 1:
        model = LinearSVC()
        # else:
        #     model = SVC(probability=True)
        model.fit(X, y)
        with open('models/' + i + '.pkl', 'wb') as file:
            dump(model, file)

if __name__ == '__main__':
    start_ML()