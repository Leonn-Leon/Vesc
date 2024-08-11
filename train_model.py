from ultralytics import YOLO

# model = YOLO('yolov10n.pt')
# model.train(data='hands_human.yaml', epochs=300, imgsz=640, device=[0,1,2,3], batch=512)

model = YOLO('runs/detect/train3/weights/last.pt')
model.train(epochs=300, imgsz=640, device=[0,1,2,3], batch=512, flipud=0.5, degrees=45, shear=10)