from pyvesc import VESC
import asyncio
import time
import threading
import fs

# serial port that VESC is connected to. Something like "COM3" for windows and as below for linux/mac


class Rover:

    def __init__(self):
        serials = fs.get_serials()
        serial_port_1 = serials[0]
        serial_port_2 = serials[1]
        self._forward_1 = True
        self._stop_1 = True
        self.motor_1 = VESC(serial_port=serial_port_1, timeout=0.5)
        time.sleep(1)

        self._forward_2 = True
        self._stop_2 = True
        self.motor_2 = VESC(serial_port=serial_port_2, timeout=0.5)

        self.speed_1 = 0
        self.speed_2 = 0

        self._max_speed_1 = 7170
        self._max_speed_2 = 7170

        self._smooth = 0.5

        threading.Thread(target=self.move_1).start()
        threading.Thread(target=self.move_2).start()


    def move_1(self):
        try:
            print("Firmware: ", self.motor_1.get_firmware_version())
        except:
            pass
        _stopped_1 = False
        while True:

            if self._forward_1:
                self.speed_1 += self._smooth
                if self._stop_1:
                    self.speed_1 += self._smooth
                    if self.speed_1 > 0:
                        self.speed_1 = 0
                        if not _stopped_1:
                            _stopped_1 = True
                            self.motor_1.stop_heartbeat()
                else:
                    _stopped_1 = False
                    if self.speed_1 > self._max_speed_1:
                        self.speed_1 = self._max_speed_1
            else:
                self.speed_1 -= self._smooth
                if self._stop_1:
                    self.speed_1 -= self._smooth
                    if self.speed_1 < 0:
                        self.speed_1 = 0
                        if not _stopped_1:
                            _stopped_1 = True
                            self.motor_1.stop_heartbeat()
                else:
                    _stopped_1 = False
                    if self.speed_1 < -self._max_speed_1:
                        self.speed_1 = -self._max_speed_1

            self.motor_1.set_rpm(int(self.speed_1))

    def move_2(self):
        try:
            print("Firmware: ", self.motor_2.get_firmware_version())
        except:
            pass

        _stopped_2 = False
        while True:

            if self._forward_2:
                self.speed_2 += self._smooth
                if self._stop_2:
                    self.speed_2 += self._smooth
                    if self.speed_2 > 0:
                        self.speed_2 = 0
                        if  not _stopped_2:
                            _stopped_2 = True
                            self.motor_2.stop_heartbeat()
                else:
                    _stopped_2 = False
                    if self.speed_2 > self._max_speed_2:
                        self.speed_2 = self._max_speed_2
            else:
                self.speed_2 -= self._smooth
                if self._stop_2:
                    self.speed_2 -= self._smooth
                    if self.speed_2 < 0:
                        self.speed_2 = 0
                        if not _stopped_2:
                            _stopped_2 = True
                            self.motor_1.stop_heartbeat()
                else:
                    _stopped_2 = False
                    if self.speed_2 < -self._max_speed_2:
                        self.speed_2 = -self._max_speed_2

            self.motor_2.set_rpm(int(self.speed_2))


    def stop(self):
        self._stop_1 = True
        self._stop_2 = True
        self._forward_1 = not self._forward_1
        self._forward_2 = not self._forward_2
        # self.move()

    def forward(self):
        self._stop_1 = False
        self._stop_2 = False
        self._forward_1 = True
        self._forward_2 = True
        # self.move()

    def back(self):
        self._stop_1 = False
        self._stop_2 = False
        self._forward_1 = False
        self._forward_2 = False
        # self.move()

    def left(self):
        self._stop_1 = False
        self._stop_2 = False
        self._forward_1 = True
        self._forward_2 = False
        # self.move()

    def right(self):
        self._stop_1 = False
        self._stop_2 = False
        self._forward_1 = False
        self._forward_2 = True
        # self.move()


if __name__ == '__main__':
    rover = Rover()
    rover.forward()
    time.sleep(3)
    rover.back()
    time.sleep(5)
