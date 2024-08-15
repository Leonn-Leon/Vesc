import torch
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
import numpy as np
import cv2
from os import listdir, mkdir
from pickle import dump
from ultralytics import YOLO
from fastai.vision.all import *
from torchvision import transforms
# from torchvision import models
# models.mobilenet_v3_small
# models.inception_v3


def start_ML():
    files = listdir('data/ML')
    if 'models' in files:
        files.remove('models')
    if 'models' not in listdir():
        mkdir('../hands/models')
    for i in files:
        X = np.load('data/ML/' + i + '/X.npy')
        y = np.load('data/ML/' + i + '/y.npy')
        print(i)
        # if y.max() > 1:
        model = LinearSVC()
        # model = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
        # else:
        #     model = SVC(probability=True)
        model.fit(X, y)
        with open('models/' + i + '.pkl', 'wb') as file:
            dump(model, file)

def train_YOLO():
    path = Path('data/images')
    db = DataBlock(
        blocks=(ImageBlock, CategoryBlock),
        get_items=get_image_files,
        splitter=RandomSplitter(valid_pct=0.0, seed=42),
        get_y=parent_label,
        item_tfms=Resize(128),
        batch_tfms=[Normalize.from_stats(*imagenet_stats),
                    *aug_transforms(mult=1.0,
                        do_flip=True,
                        flip_vert=True,
                        max_rotate=45.0,
                        min_zoom=1.0,
                        max_zoom=1.1,
                        max_lighting=0.2,
                        max_warp=0.1,
                        p_affine=0.75,
                        p_lighting=0.75,
                        xtra_tfms=None,
                        size=None,
                        mode='bilinear',
                        pad_mode='zeros',
                        align_corners=True,
                        batch=False,
                        min_scale=1.0)
                    ]
    )
    dls = db.dataloaders(path, bs=32, num_workers=0)
    dls.show_batch()
    learn = vision_learner(dls, mobilenet_v3_small, metrics=accuracy)
    learn.fine_tune(450)
    learn.save('follow2', with_opt=False)
    model_architecture = learn.model
    model_scripted = torch.jit.script(model_architecture)
    model_scripted.save('models/follow2.pt')


if __name__ == '__main__':
    # start_ML()
    print('CUDA: ', torch.cuda.is_available())
    train_YOLO()
#%%
