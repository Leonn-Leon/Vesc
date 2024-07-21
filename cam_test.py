import cv2
import numpy as np
import pyrealsense2 as rs
from realsense_depth import *
import threading
import sys


class Cam_3d():
    def __init__(self, _show:bool = True, _show_color:bool = True, rover = None, _with_rover = True):
        self._with_rover = _with_rover
        if _with_rover:
            if not rover:
                import use_rover
                self.rover = use_rover.Rover()
            else:
                self.rover = rover
        self._show = _show
        self._show_color = _show_color


        self.up_line = 220
        self.down_line = 330

        self.left_line = 320-120
        self.right_line = 320+120

        self._distance = 930
        self.shut_down = False
        self.frame = np.zeros((640, 480))

    def cam_open(self):
        self.dc = DepthCamera()

    def stop_auto(self):
        print('STOP Auto!')
        self.shut_down = True
        self.rover.stop()
        try:
            self.cam_tread.join()
        except:
            return

    def start_auto(self):
        print('Run!')
        try:
            self.cam_open()
        except Exception as exc:
            print('Камеру НЕ подключу', exc)
            pass
        self.shut_down = False
        self.cam_tread = threading.Thread(target=self.camera)
        self.cam_tread.start()

    def send_command(self, comand):
        if comand == 'Vpered':
            self.rover.forward()
        elif comand == 'Vlevo':
            self.rover.left()
        elif comand == 'Vpravo':
            self.rover.right()
        elif comand == 'STOP':
            self.rover.stop()

    def get_frame(self):
        return self.frame

    def camera(self):
        threshold_down = 3000
        threshold_up = 5000
        last_command = ''
        command = ''
        fartherest_points = [[0, 0]]
        send_command_period = 1
        send_command_count = send_command_period
        not_forward_count = 100
        while True:
            if self.shut_down:
                break
            ret, depth_frame, color_frame = self.dc.get_frame()

            self.frame = color_frame
            if not ret:
                continue
            if self._show:
                if not self._show_color:
                    depth_frame_out = depth_frame.copy()
                    depth_frame_out[depth_frame_out > threshold_up] = threshold_up
                    depth_frame_out[depth_frame_out < threshold_down] = threshold_down
                    depth_frame_out = depth_frame_out/depth_frame_out.max()
                else:
                    cv2.line(color_frame, (0, self.up_line), (640, self.up_line), (0, 0, 255), 3)
                    cv2.line(color_frame, (0, self.down_line), (640, self.down_line), (0, 0, 255), 3)
                    # cv2.line(color_frame, (80, 0), (80, 480), (0, 0, 255), 3)
                    # cv2.line(color_frame, (640-80, 0), (640-80, 480), (0, 0, 255), 3)
            goal_depth = depth_frame[self.up_line:self.down_line, 20:]
            goal_depth[goal_depth > 12000] = 0
            fartherest_value = goal_depth.max()
            direction_line = np.argmax(goal_depth.mean(axis=0))+20
            maxxs = np.where(goal_depth == fartherest_value)
            goal_depth[goal_depth == 0] = 65000
            nearest_value = goal_depth.min()
            minns = np.where(goal_depth == nearest_value)
            nearest_point = [minns[1][0]+20, minns[0][0] + self.up_line]
            fartherest_point = [maxxs[1][0]+20, maxxs[0][0] + self.up_line]
            fartherest_points = fartherest_points[-40:] + [fartherest_point]
            if self._show:
                point = np.array(fartherest_points).mean(axis=0)
                point = int(point[0]), int(point[1])
                if self._show_color:
                    cv2.circle(color_frame, (point), 15, (255, 0, 0), 5)
                    cv2.circle(color_frame, (nearest_point), 15, (0, 0, 255), 5)
                    cv2.line(color_frame, (direction_line, 0), (direction_line, 480), (0, 0, 255), 3)
                else:
                    cv2.circle(depth_frame_out, (point), 15, (0, 0, 0), 5)
            # print(direction_line, nearest_point)
            if nearest_value < self._distance:
                if last_command != 'STOP':
                    command = 'STOP'
            if (nearest_value > self._distance and direction_line < self.left_line) or (direction_line < nearest_point[0] and command == 'STOP'):
                if last_command != 'Vlevo':
                    command = 'Vlevo'
            elif nearest_value > self._distance and direction_line > self.right_line or (direction_line > nearest_point[0] and command == 'STOP'):
                if last_command != 'Vpravo':
                    command = 'Vpravo'
            elif fartherest_value > self._distance and direction_line > self.left_line and direction_line < self.right_line:
                if last_command != 'Vpered':
                    command = 'Vpered'
                    not_forward_count = 100

            if last_command != command:
                send_command_count -= 1
                if send_command_count == 0:
                    last_command = command
                    send_command_count = send_command_period
                    if command != 'Vpered':
                        not_forward_count -= 1
                        if not_forward_count <= 0:
                            command = 'STOP'
                    if self._with_rover:
                        self.send_command(command)
                    print(command)
            else:
                send_command_count = send_command_period
            if self._show:
                if self._show_color:
                    cv2.putText(color_frame, last_command, (200, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,
                            (0, 255, 0), 3, 2)
                    cv2.imshow('Color frame', color_frame)
                else:
                    cv2.imshow("depth frame", depth_frame_out)
            # Stop
            if self._show:
                k = cv2.waitKey(1)
                if k == ord('q'):
                    break

        self.dc.release()

if __name__ == '__main__':
    Cam_3d(_show=True, _show_color=True, rover=None, _with_rover=False).start_auto()
