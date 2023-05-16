# coding:utf-8
from basic_functions import *
from controller import move_actuator
import cv2
from time import sleep

# 埋まっていないところで色が確定するところを埋める
# Fill boxes if the color can be decided
def fill(colors):
    for i in range(6):
        for j in range(8):
            if (1 < i < 4 or 1 < j < 4) and colors[i][j] == '':
                done = False
                for k in range(8):
                    if [i, j] in parts_place[k]:
                        for strt in range(3):
                            if parts_place[k][strt] == [i, j]:
                                idx = [colors[parts_place[k][l % 3][0]][parts_place[k][l % 3][1]] for l in range(strt + 1, strt + 3)]
                                for strt2 in range(3):
                                    idx1 = strt2
                                    idx2 = (strt2 + 1) % 3
                                    idx3 = (strt2 + 2) % 3
                                    for l in range(8):
                                        if parts_color[l][idx1] == idx[0] and parts_color[l][idx2] == idx[1]:
                                            colors[i][j] = parts_color[l][idx3]
                                            done = True
                                            break
                                    if done:
                                        break
                                break
                    if done:
                        break
    return colors

# パズルの状態の取得
# Get colors of stickers
def detector():
    colors = [['' for _ in range(8)] for _ in range(6)]
    for i in range(2):
        move_actuator(i, 0, 1000)
    for i in range(2):
        move_actuator(i, 1, 2000)
    sleep(0.3)
    rpm = 200
    capture = cv2.VideoCapture(0)
    idx = 0
    for idx in range(4):
        #color: g, b, r, o, y, w
        # for normal sticker
        #color_low = [[50, 50, 50],   [90, 50, 50],    [160, 70, 50],  [170, 20, 50],  [20, 50, 50],   [0, 0, 50]]
        #color_hgh = [[90, 255, 255], [140, 255, 255], [10, 255, 200], [20, 255, 255], [50, 255, 255], [179, 50, 255]]
        #color_low = [[40, 50, 50],   [90, 50, 70],    [160, 50, 50],   [170, 50, 50],    [20, 50, 30],   [0, 0, 50]]
        #color_hgh = [[90, 255, 255], [140, 255, 200], [170, 255, 255], [10, 255, 255], [40, 255, 255], [179, 50, 255]]
        color_center = [(80, 116, 61), (103, 53, 38), (0, 0, 255), (0, 170, 255), (72, 149, 149), (157, 144, 145)]
        circlecolor = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 170, 255), (0, 255, 255), (255, 255, 255)]
        surfacenum = [[[4, 2], [4, 3], [5, 2], [5, 3]], [[2, 2], [2, 3], [3, 2], [3, 3]], [[0, 2], [0, 3], [1, 2], [1, 3]], [[3, 7], [3, 6], [2, 7], [2, 6]]]
        for _ in range(5):
            ret, frame = capture.read()
        d = 10
        size_x = 130
        size_y = 100
        center = [size_x // 2, size_y // 2]
        dx = [-1, -1, 1, 1]
        dy = [-1, 1, -1, 1]
        ret, show_frame = capture.read()
        show_frame = cv2.resize(show_frame, (size_x, size_y))
        #cv2.imshow('title',show_frame)
        #hsv = cv2.cvtColor(show_frame,cv2.COLOR_BGR2HSV)
        for i in range(4):
            y = center[0] + dy[i] * d
            x = center[1] + dx[i] * d
            val = [elem for elem in show_frame[x, y]]
            min_dis = 100000000
            min_color_idx = 0
            for j in range(6):
                dis = 0
                for k in range(3):
                    dis += (color_center[j][k] - val[k]) ** 2
                if dis < min_dis:
                    min_dis = dis
                    min_color_idx = j
            colors[surfacenum[idx][i][0]][surfacenum[idx][i][1]] = j2color[min_color_idx]
            cv2.circle(show_frame, (y, x), 2, circlecolor[min_color_idx], thickness=2, lineType=cv2.LINE_8, shift=0)
            print(idx, i, y, x, val, j2color[min_color_idx])
        cv2.imshow('face',show_frame)
        cv2.waitKey(0)
        colors = fill(colors)
        move_actuator(0, 0, -90, rpm)
        move_actuator(1, 0, 90, rpm)
        sleep(0.2)
        #cv2.destroyAllWindows()
    capture.release()
    return colors

print('detector initialized')

'''
colors[0] = ['', '', 'w', 'g', '', '', '', '']
colors[1] = ['', '', 'o', 'o', '', '', '', '']
colors[2] = ['o', 'y', 'g', 'g', 'w', 'r', 'w', 'b']
colors[3] = ['o', 'b', 'y', 'y', 'g', 'r', 'w', 'b']
colors[4] = ['', '', 'r', 'r', '', '', '', '']
colors[5] = ['', '', 'y', 'b', '', '', '', '']
'''