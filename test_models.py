import cv2
import numpy as np
from skimage import feature
from realsense_depth import *
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import pickle
import torch
from torchvision import transforms
from matplotlib import pyplot as plt

_model = YOLO('hands/models/best.pt')

model_path = 'hands/models/'
hand_model = torch.jit.load(model_path+'follow.pt')
hand_model.load_state_dict(torch.load(model_path+'follow.pth', map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu')))
hand_model.to('cuda')
hand_model.eval()

norm_method = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

print("Модельки Открыты!")

names = ['base', 'follow', 'no_command', 'stop']

real_sense = True
if real_sense:
    dc = DepthCamera()
else:
    cap = cv2.VideoCapture(0)

last_command = ''
new_command = ''
_command = ''
print("Получилось поключиться к камере!")
confidence = 5
skip = 0
while True:
    if real_sense:
        ret, depth_frame, color_frame = dc.get_frame()
    else:
        ret, color_frame = cap.read()

    if not ret:
        continue

    skip += 1
    if skip < 5:
        continue
    skip = 0

    results = _model.predict(color_frame, verbose=False)
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
    image = np.zeros((256, 256))
    if hand_box[4] > 100:
        image = color_frame[hand_box[1]:hand_box[3], hand_box[0]:hand_box[2]]
        image = cv2.resize(image, (256, 256))
        tens = torch.from_numpy(image[None, :, :] / 255).permute(0, 3, 1, 2)
        tens = norm_method(tens)

        if torch.cuda.is_available():
            input_batch = tens.to('cuda')
            input_batch = input_batch.float()
        else:
            print('CUDA недоступна')
            break
        with torch.no_grad():
            output = hand_model(input_batch).cpu()[0]
        print(output)
        _command = names[np.argmax(output)]

    cv2.imshow('YOLO Detection', img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('p'):
        cv2.waitKey(0)

    if new_command == _command:
        confidence -= 1
    else:
        confidence = 5
    if confidence == 0 and last_command != _command:
        last_command = _command
        print(_command)
        confidence = 5

    new_command = _command

if real_sense:
    dc.release()
else:
    cap.release()