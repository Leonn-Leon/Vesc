from ultralytics import YOLO

model = YOLO("yolov10n.pt")

results = model.train(data="signs-obb3/dataset.yaml", imgsz=640, epochs=400, device=[0,1,2,3], batch=700)
