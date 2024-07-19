from pyvesc import VESC
import time

# serial port that VESC is connected to. Something like "COM3" for windows and as below for linux/mac
serial_port = 'COM3'


# a function to show how to use the class as a static object.
def run_motor_as_object():
    motor = VESC(serial_port=serial_port, timeout=0.5)
    print("Firmware: ", motor.get_firmware_version())

    motor.set_rpm(7000)
    time.sleep(3)
    motor.set_rpm(0)
    time.sleep(1)
    motor.set_rpm(-7000)
    time.sleep(3)
    motor.stop_heartbeat()



if __name__ == '__main__':
    # run_motor_using_with()
    run_motor_as_object()
    # time_get_values()
