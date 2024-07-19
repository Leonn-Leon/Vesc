from pyvesc import VESC
import asyncio
import time
import threading

# serial port that VESC is connected to. Something like "COM3" for windows and as below for linux/mac
serial_port = 'COM4'


class Rover:

    def __init__(self):
        self._forward = True
        self._stop = True
        self.motor = VESC(serial_port=serial_port, timeout=0.5)
        threading.Thread(target=self.move).start()


    def move(self):
        while True:
            try:
                print("Firmware: ", motor.get_firmware_version())
            except:
                pass

            try:
                rpm = self.motor.get_measurements().rpm
            except Exception as e:
                print(f'Tраблы с получением RPM: {e}')


            if self._stop:
                self.motor.set_rpm(0)
                self.motor.stop_heartbeat()
            else:
                self.motor.set_rpm(7000 if self._forward else -7000)

    def stop(self):
        self._stop = True
        # self.move()

    def forward(self):
        self._stop = False
        self._forward = True
        # self.move()

    def back(self):
        self._stop = False
        self._forward = False
        # self.move()


if __name__ == '__main__':
    rover = Rover()
    rover.forward()
    time.sleep(3)
    rover.back()
    time.sleep(5)
