from ultralytics import YOLO

model = YOLO('yolov10n.pt')

model.train(data='hands_human.yaml', epochs=300, imgsz=640, device=[0,1,2,3], batch=512)