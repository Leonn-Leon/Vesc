import time
from ultralytics import YOLO
import os

model = YOLO("yolov10x.pt")

current_path = 'neurolearning/signs-obb3'

for type in ['train/', 'val/']:
    for file in os.listdir(current_path+'/images/'+type):
        print(current_path+'/images/'+type+ file)
        if '.' == file[0]:
            continue
        last_annotations = []
        with open(current_path+'/labels/'+type+file[:-4]+".txt", 'r') as annot_file:
            f = annot_file.read().split('\n')
            for line in f:
                if len(line) < 3:
                    continue
                coords = line.split()
                c = coords[0]
                coords = [float(c) for c in coords][1:]
                last_annotations += [[int(c), min(coords[0::2]), min(coords[1::2]), max(coords[0::2]), max(coords[1::2])]]
                if с == '5':
                    print('Уже распознавали')
                    continue
        try:
            results = model.predict(current_path+'/images/'+type+ file, verbose=False, classes=[0], conf = 0.7)
        except Exception as exc:
            print('Error with', current_path+'/images/'+type+ file, exc)
            continue
        # for human in people_results:
        res = results[0].boxes
        people_results = res.xyxy
        print(results[0].orig_shape)

        annotations = []
        # Сохранение obb аннотации просто как квадратики
        for c, x1, y1, x2, y2 in last_annotations:
            xc, yc, w, h = (x1 + x2) / 2, (y1 + y2) / 2, abs(x2 - x1), abs(y2 - y1)
            # Нормализация координат относительно размера изображения
            # img_w, img_h = results[0].orig_shape[1], results[0].orig_shape[0]
            # xc /= img_w
            # yc /= img_h
            # w /= img_w
            # h /= img_h
            annotations.append(f'{c} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n')

        # Формирование строк аннотации
        for x1, y1, x2, y2 in people_results:
            xc, yc, w, h = (x1 + x2) / 2, (y1 + y2) / 2, abs(x2 - x1), abs(y2 - y1)
            # Нормализация координат относительно размера изображения
            img_w, img_h = results[0].orig_shape[1], results[0].orig_shape[0]
            xc /= img_w
            yc /= img_h
            w /= img_w
            h /= img_h
            annotations.append(f'5 {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n')

        with open(current_path+'/labels/'+type+ file[:-4]+".txt", 'w') as annot_file:
            annot_file.writelines(annotations)