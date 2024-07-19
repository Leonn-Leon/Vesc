import cv2
import pyrealsense2 as rs
from realsense_depth import *
import sys

dc = DepthCamera()

if 'show' in sys.argv:
    _show = True
else:
    _show = False
_show = True

if 'color' in sys.argv:
    _show_color = True
else:
    _show_color = False

up_line = 150
down_line = 430

print('Run!')
while True:
    ret, depth_frame, color_frame = dc.get_frame()
    if not ret:
        continue
    threshold_down = 0
    threshold_up = 1200
    if _show:
        if _show_color:
            cv2.imshow('Color frame', color_frame)
        else:
            depth_frame_out = depth_frame.copy()
            depth_frame_out[depth_frame_out > threshold_up] = threshold_up
            depth_frame_out[depth_frame_out < threshold_down] = threshold_down
            # depth_frame = cv2.GaussianBlur(depth_frame,(7, 7),0)
            # depth_frame = cv2.medianBlur(depth_frame, 5)
            depth_frame_out = depth_frame_out/depth_frame_out.max()
            cv2.line(depth_frame_out, (0, up_line), (640, up_line), (0, 0, 255), 3)
            cv2.line(depth_frame_out, (0, down_line), (640, down_line), (0, 0, 255), 3)
            goal_depth = depth_frame[up_line:down_line]
            goal_depth[goal_depth == threshold_down] = threshold_up
            # depth_frame_out = cv2.applyColorMap(depth_frame_out.astype(np.uint8), cv2.COLORMAP_JET)
            minns = np.where(goal_depth == goal_depth.min())
            nearest_point = minns[1][0], minns[0][0]+up_line
            cv2.circle(color_frame, (nearest_point), 10, (255, 0, 0), 3)
            if goal_depth.min() < 700:
                if nearest_point[0] > 330:
                    cv2.putText(color_frame, 'Vlevo', (200, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,
                                (255, 0, 0), 3, 2)
                elif nearest_point[0] < 310:
                    cv2.putText(color_frame, 'Vpravo', (200, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,
                                (255, 0, 0), 3, 2)
                else:
                    cv2.putText(color_frame, 'STOP', (200, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,
                                (0, 0, 255), 3, 2)
            else:
                cv2.putText(color_frame, 'Vpered', (200, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,
                            (0, 255, 0), 3, 2)
            # cv2.imshow("depth frame", depth_frame_out)
            cv2.imshow('Color frame', color_frame)

    # Stop
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

dc.release()
