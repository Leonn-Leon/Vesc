import cv2
import numpy as np
import pyrealsense2 as rs
from realsense_depth import *
from ultralytics.utils.plotting import Annotator
from ultralytics import YOLO
import threading
import sys


class Cam_3d():
    def __init__(self, _show:bool = True, _show_color:bool = True, rover = None, _with_rover = True):

        self._model = YOLO('hands/models/hands_only.pt')
        self.autopilot_in = False

        self._with_rover = _with_rover
        if _with_rover:
            if not rover:
                import use_rover
                self.rover = use_rover.Rover()
            else:
                self.rover = rover
        self._show = _show
        self._show_color = _show_color


        self.up_line = 280
        self.down_line = 370

        self.left_line = 320-50
        self.right_line = 320+50

        self.forward_left_line = 320 - 160
        self.forward_right_line = 320 + 160

        self._distance = 1000
        self.shut_down = False
        self.frame = np.zeros((640, 480))
        try:
            self.cam_open()
        except Exception as exc:
            print('Камеру НЕ подключу', exc)
            pass

    def cam_open(self):
        self.dc = DepthCamera()

    def start_cam(self):
        print('Run!')
        self.shut_down = False
        self.cam_tread = threading.Thread(target=self.camera)
        self.cam_tread.start()

    def stop_cam(self):
        print('STOP Auto!')
        self.shut_down = True
        self.rover.stop()
        try:
            self.cam_tread.join()
        except:
            return

    def start_auto(self):
        self.autopilot_in = True

    def stop_auto(self):
        self.rover.stop()
        self.autopilot_in = False

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
        threshold_down = 20000
        threshold_up = 65000
        last_command = ''
        command = ''

        last_hand_command = ''
        new_hand_command = ''
        hand_command = ''
        MAX_CONF = 3
        confidence = MAX_CONF

        send_command_period = 1
        send_command_count = send_command_period
        not_forward_count = 5
        center_shift = 0

        skip = 0

        img = np.zeros((640, 640))
        while True:
            if self.shut_down:
                break
            ret, depth_frame, color_frame = self.dc.get_frame()

            self.frame = color_frame

            if not ret:
                continue

            skip += 1
            if skip == 3:
                results = self._model.predict(color_frame, verbose=False)
                skip = 0
                hand_box = [0, 0, 0, 0, 0, 0]
                for r in results:
                    if self._show:
                        annotator = Annotator(color_frame.copy())
                    boxes = r.obb
                    for box in boxes:
                        b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                        c = box.cls.item()
                        if c < 5 or True:
                            _square = (b[2] - b[0]) * (b[3] - b[1])
                            if hand_box[4] < _square:
                                hand_box = [int(i) for i in b] + [_square] + [int(c)]
                                # print(hand_box)
                        if _show:
                            annotator.box_label(b, self._model.names[int(c)])
                if self._show:
                    img = annotator.result()
                if hand_box[4] > 300:
                    hand_command = hand_box[5]

                    if new_hand_command == hand_command:
                        confidence -= 1
                    else:
                        confidence = MAX_CONF

                    if confidence == 0 and last_hand_command != hand_command:
                        last_hand_command = hand_command
                        print(self._model.names[hand_box[5]])
                        if hand_command == 0:
                            self.start_auto()
                        else:
                            print("СТОП ПО РУКАМ")
                            self.stop_auto()
                        confidence = MAX_CONF

                    new_hand_command = hand_command



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
            goal_depth = depth_frame[self.up_line:self.down_line, 40:-40]
            # goal_depth[goal_depth > 12000] = 0
            # fartherest_value = goal_depth.max()
            _hist = goal_depth.mean(axis=0)
            direction_line = np.argmax(_hist)+40
            # direction_line = (np.argmin(_hist[self.forward_right_line:])+self.forward_right_line+20 + np.argmin(_hist[:self.forward_left_line]))/2
            # maxxs = np.where(goal_depth == fartherest_value)
            goal_depth[goal_depth == 0] = 65000
            nearest_value = goal_depth.min()
            minns = np.where(goal_depth == nearest_value)
            nearest_point = [minns[1][0]+40, minns[0][0] + self.up_line]
            # fartherest_point = [maxxs[1][0]+20, maxxs[0][0] + self.up_line]
            # direction_points = direction_points[-40:] + [direction_line]
            # direction_line = np.array(direction_points).mean()
            # print(direction_line)
            if self._show:
                if self._show_color:
                    # cv2.circle(color_frame, (point), 15, (255, 0, 0), 5)
                    cv2.circle(color_frame, (nearest_point), 15, (0, 0, 255), 5)
                    cv2.line(color_frame, (direction_line, 0), (direction_line, 480), (0, 0, 255), 3)
                else:
                    cv2.line(depth_frame_out, (direction_line, 0), (direction_line, 480), (0, 0, 255), 3)
            # print(direction_line, nearest_point)
            if nearest_value < self._distance:
                if last_command != 'STOP':
                    command = 'STOP'
            else:
                center_shift -= 1
                if center_shift < 0:
                    center_shift = 0

            if nearest_value > self._distance and direction_line < self.left_line and center_shift == 0:
                command = 'Vlevo'

            if nearest_value > self._distance and direction_line > self.right_line and center_shift == 0:
                command = 'Vpravo'

            if direction_line < nearest_point[0] and command == 'STOP':
                command = 'Vlevo'
                center_shift = 50

            if direction_line > nearest_point[0] and command == 'STOP':
                command = 'Vpravo'
                center_shift = 50

            if nearest_value > self._distance and direction_line > self.forward_left_line and direction_line < self.forward_right_line:
                if last_command != 'Vpered':
                    command = 'Vpered'
                not_forward_count = 5

            if last_command != command:
                send_command_count -= 1
                if send_command_count == 0:
                    last_command = command
                    send_command_count = send_command_period
                    if command != 'Vpered':
                        not_forward_count -= 1
                        if not_forward_count <= 0:
                            not_forward_count = 0
                            command = 'STOP'
                            last_command = 'STOP'
                    if self._with_rover and self.autopilot_in:
                        self.send_command(command)
                    print(command, self.autopilot_in)
            else:
                send_command_count = send_command_period
            if self._show:
                if self._show_color:
                    cv2.putText(color_frame, last_command, (200, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,
                            (0, 255, 0), 3, 2)
                    # cv2.imshow('Color frame', color_frame)
                    cv2.imshow('Yolo out', img)
                else:
                    cv2.imshow("depth frame", depth_frame_out)
            # Stop
            if self._show:
                k = cv2.waitKey(1)
                if k == ord('q'):
                    break

        # self.dc.release()

if __name__ == '__main__':
    Cam_3d(_show=True, _show_color=True, rover=None, _with_rover=False).start_auto()
