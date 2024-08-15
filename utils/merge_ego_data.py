import time
from ultralytics import YOLO
import os

model = YOLO("yolov10x.pt")
for path in os.listdir('egohands/images'):
    for file in os.listdir('egohands/images/'+path):
        print('egohands/images/'+path + "/"+ file)
        if '.' == file[0]:
            continue
        with open('egohands/labels/'+path + "/"+ file[:-4]+".txt", 'r') as annot_file:
            f = annot_file.read().split('\n')
            if len(f) > 1 and f[-2][0] == '1':
                print('Уже распознавали')
                continue
        try:
            results = model.predict('egohands/images/'+path + "/"+ file, verbose=False, classes=[0], conf = 0.5)
        except Exception as exc:
            print('Error with', 'egohands/images/'+path + "/"+ file, exc)
            continue
        # for human in people_results:
        annotations = []
        res = results[0].boxes
        people_results = res.xyxy
        print(results[0].orig_shape)

        # Формирование строк аннотации
        for x1, y1, x2, y2 in people_results:
            xc, yc, w, h = (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1
            # Нормализация координат относительно размера изображения
            img_w, img_h = results[0].orig_shape[1], results[0].orig_shape[0]
            xc /= img_w
            yc /= img_h
            w /= img_w
            h /= img_h
            annotations.append(f'1 {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n')

        with open('egohands/labels/'+path + "/"+ file[:-4]+".txt", 'a') as annot_file:
            annot_file.writelines(annotations)