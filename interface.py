from flask import Flask, render_template, request
from datetime import datetime
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


@app.route('/control', methods=['POST'])
def control():
    global current_location, liquid_level, battery_level, rover
    command = request.form['command']

    # Эмуляция управления вместо использования GPIO
    print(f"Команда получена: {command}")

    # Обновление состояния (пример логики, заменить на реальную)
    if not _test:
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
    app.run(host='0.0.0.0', port=5000)
