from flask import Flask, render_template, request, Response
from datetime import datetime
from cam_test import Cam_3d
import numpy as np
import cv2
_test = False
if not _test:
    import use_rover

app = Flask(__name__)

# Инициализация состояния
current_location = "1"
liquid_level = "50%"
battery_level = "87%"



@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control', methods=['POST'])
def control():
    global current_location, liquid_level, battery_level, rover, camera
    command = request.form['command']

    # Эмуляция управления вместо использования GPIO
    print(f"Команда получена: {command}")

    # Обновление состояния (пример логики, заменить на реальную)
    if not _test:
        if command == 'СУПЕР СТОП':
            rover.emergency_stop()
        if command == 'автопилот_вкл':
            camera.start_cam()
            # camera.start_auto()
        elif command.isdigit():
            rover.set_max_value(int(command))
        else:
            camera.stop_auto()


        if command == 'автопилот_выкл':
            camera.stop_auto()
            camera.stop_cam()
        if command == 'стоп':
            rover.stop()
        if command == 'вперед':
            # print(datetime.now())
            rover.forward()
        if command == 'назад':
            rover.back()
        if command == 'влево':
            rover.left()
        if command == 'вправо':
            rover.right()
    # Пример обновления уровня жидкости
    liquid_level = "85%" if liquid_level == "87%" else "87%"
    # Пример обновления уровня заряда
    battery_level = "85%" if battery_level == "87%" else "87%"

    return 'OK'


if __name__ == '__main__':
    if not _test:
        rover = use_rover.Rover()
    else:
        rover = None
    camera = Cam_3d(_show=True, _show_color=True, rover= rover, _with_rover=bool(rover))
    app.run(host='0.0.0.0', port=5000)
