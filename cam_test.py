import cv2
import numpy as np
import pyrealsense2 as rs
from realsense_depth import *
_with_rover = True
import use_rover
import sys


class Cam_3d():
    def __init__(self, _show:bool = True, _show_color:bool = True):
        self.dc = DepthCamera()
        if _with_rover:
            self.rover = use_rover.Rover()
        self._show = _show
        self._show_color = _show_color


        self.up_line = 150
        self.down_line = 400

        self.left_line = 320-100
        self.right_line = 320+100

        self._distance = 1000

    def start_auto(self):
        print('Run!')
        threshold_down = 3000
        threshold_up = 5000
        last_command = ''
        command = ''
        fartherest_points = [[0, 0]]
        while True:
            ret, depth_frame, color_frame = self.dc.get_frame()
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
            goal_depth = depth_frame[self.up_line:self.down_line, 20:]
            goal_depth[goal_depth > 10000] = 0
            fartherest_value = goal_depth.max()
            maxxs = np.where(goal_depth == fartherest_value)
            goal_depth[goal_depth == 0] = 65000
            nearest_value = goal_depth.min()
            minns = np.where(goal_depth == nearest_value)
            nearest_point = [minns[1][0], minns[0][0] + self.up_line]
            fartherest_point = [maxxs[1][0], maxxs[0][0] + self.up_line]
            fartherest_points = fartherest_points[-20:] + [fartherest_point]
            if self._show:
                point = np.array(fartherest_points).mean(axis=0)
                point = int(point[0]), int(point[1])
                if self._show_color:
                    cv2.circle(color_frame, (point), 15, (255, 0, 0), 5)
                    cv2.circle(color_frame, (nearest_point), 15, (0, 0, 255), 5)
                else:
                    cv2.circle(depth_frame_out, (point), 15, (0, 0, 0), 5)

            if nearest_value < self._distance:
                if last_command != 'STOP':
                    if _with_rover:
                        self.rover.stop()
                    command = 'STOP'
            elif nearest_value > self._distance+100 and fartherest_point[0] < self.left_line:
                if last_command != 'Vlevo':
                    if _with_rover:
                        self.rover.left()
                    command = 'Vlevo'
            elif nearest_value > self._distance+100 and fartherest_point[0] > self.right_line:
                if last_command != 'Vpered':
                    if _with_rover:
                        self.rover.right()
                    command = 'Vpravo'
            elif fartherest_value > self._distance+100:
                if last_command != 'Vpered':
                    if _with_rover:
                        self.rover.forward()
                    command = 'Vpered'

            if last_command != command:
                last_command = command
                print(command)
            if self._show:
                if self._show_color:
                    cv2.putText(color_frame, command, (200, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,
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
    Cam_3d(_show=False).start_auto()
