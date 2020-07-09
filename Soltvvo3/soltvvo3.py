# coding:utf-8
'''
Code for Soltvvo2
Written by Nyanyan
Copyright 2020 Nyanyan


Cube.Cp[その位置にあるパーツの番号]
Cube.Co[白または黄ステッカーの向き]
U面
        B
L [0, 0] [1, 0] R
L [2, 0] [3, 0] R
        F
D面
        F
L [4, 0] [5, 0] R
L [6, 0] [7, 0] R
        B

向きは揃っている方向(白黄ステッカー)から時計回りに1, 2となる

Cube.Cp[part number]
Cube.Co[direction of white or yellow sticker]
U face
        B
L [0, 0] [1, 0] R
L [2, 0] [3, 0] R
        F
D face
        F
L [4, 0] [5, 0] R
L [6, 0] [7, 0] R
        B
the direction of white or yellow sticker is 
0 if the sticker is on U or D face, 
1 if it is 120 degrees clockwise rotated from U or D face,
2 if it is 240 degrees clockwise rotated from U or D face.
'''

from copy import deepcopy
from collections import deque
from time import time, sleep
import tkinter
import cv2
import numpy as np
import serial
import csv
import RPi.GPIO as GPIO

class Cube:
    def __init__(self):
        self.Co = [0, 0, 0, 0, 0, 0, 0, 0]
        self.Cp = [0, 1, 2, 3, 4, 5, 6, 7]

    # 回転処理 CP
    # Rotate CP
    def move_cp(self, arr):
        surface = [[3, 1, 5, 7], [1, 0, 7, 6], [0, 2, 6, 4], [2, 3, 4, 5]]
        replace = [[1, 3, 0, 2], [3, 2, 1, 0], [2, 0, 3, 1]]
        res = [i for i in self.Cp]
        for i, j in zip(surface[arr[0]], replace[-arr[1] - 1]):
            res[i] = self.Cp[surface[arr[0]][j]]
        return res

    # 回転処理 CO
    # Rotate CO
    def move_co(self, arr):
        surface = [[3, 1, 5, 7], [1, 0, 7, 6], [0, 2, 6, 4], [2, 3, 4, 5]]
        replace = [[1, 3, 0, 2], [3, 2, 1, 0], [2, 0, 3, 1]]
        pls = [2, 1, 1, 2]
        res = [i for i in self.Co]
        for i, j in zip(surface[arr[0]], replace[-arr[1] - 1]):
            res[i] = self.Co[surface[arr[0]][j]]
        if arr[1] != -2:
            for i in range(4):
                res[surface[arr[0]][i]] += pls[i]
                res[surface[arr[0]][i]] %= 3
        return res

    # 回転番号に則って実際にパズルの状態配列を変化させる
    # Rotate CP and CO
    def move(self, arr):
        res = Cube()
        res.Co = self.move_co(arr)
        res.Cp = self.move_cp(arr)
        return res

    # cp配列から固有の番号を作成
    # Return the number of CP
    def cp2i(self):
        res = 0
        for i in range(4):
            cnt = 0
            for j in self.Cp[:i]:
                if j < self.Cp[i]:
                    cnt += 1
            res += fac[7 - i] * (self.Cp[i] - cnt)
        for i in range(4, 8):
            cnt = self.Cp[i]
            for j in self.Cp[i + 1:]:
                if j < self.Cp[i]:
                    cnt -= 1
            res += fac[7 - i] * (self.Cp[i] - cnt)
        return res
    
    # co配列から固有の番号を作成
    # Return the number of CO
    def co2i(self):
        res = 0
        for i in self.Co:
            res *= 3
            res += i
        return res

# アクチュエータを動かすコマンドを送る
# Send commands to move actuators
def move_actuator(num, arg1, arg2, arg3=None):
    if arg3 == None:
        com = str(arg1) + ' ' + str(arg2)
    else:
        com = str(arg1) + ' ' + str(arg2) + ' ' + str(arg3)
    ser_motor[num].write((com + '\n').encode())
    ser_motor[num].flush()

# キューブを掴む
# Grab arms
def grab_p():
    for i in range(2):
        for j in range(2):
            move_actuator(j, i, 1000)
        sleep(3)

# キューブを離す
# Release arms
def release_p():
    for i in range(2):
        for j in range(2):
            move_actuator(i, j, 2000)

# アームのキャリブレーション
# Calibration arms
def calibration(num, deg):
    def x():
        move_actuator(num // 2, num % 2, deg, 100)
    return x

# ボックスに色を反映させる
# Color the boxes
def confirm_p():
    global colors
    for i in range(6):
        for j in range(8):
            if (1 < i < 4 or 1 < j < 4) and colors[i][j] in j2color:
                entry[i][j]['bg'] = dic[colors[i][j]]
    # 埋まっていないところで色が確定するところを埋める
    # Fill boxes if the color can be decided
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
                                            entry[i][j]['bg'] = dic[colors[i][j]]
                                            done = True
                                            break
                                    if done:
                                        break
                                break
                    if done:
                        break
    
    # 埋まっていないところの背景色をgrayに
    # Fill boxes gray if the color is not decided
    for i in range(6):
        for j in range(8):
            if (1 < i < 4 or 1 < j < 4) and colors[i][j] == '':
                entry[i][j]['bg'] = 'gray'

# パズルの状態の取得
# Get colors of stickers
def detect():
    global idx, colors
    for i in range(2):
        move_actuator(i, 0, 1000)
    for i in range(2):
        move_actuator(i, 1, 2000)
    sleep(0.3)
    rpm = 200
    '''
    for i in range(2):
        move_actuator(0, 0, 45, rpm)
    '''
    capture = cv2.VideoCapture(0)
    idx = 0
    for idx in range(4):
        #color: g, b, r, o, y, w
        color_low = [[50, 50, 50],   [90, 50, 50],   [160, 70, 50], [170, 20, 50],  [20, 50, 50],   [0, 0, 50]] #for PC
        color_hgh = [[90, 255, 255], [140, 255, 255], [10, 255, 200], [20, 255, 255], [50, 255, 255], [179, 50, 255]]
        circlecolor = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 170, 255), (0, 255, 255), (255, 255, 255)]
        surfacenum = [[[4, 2], [4, 3], [5, 2], [5, 3]], [[2, 2], [2, 3], [3, 2], [3, 3]], [[0, 2], [0, 3], [1, 2], [1, 3]], [[3, 7], [3, 6], [2, 7], [2, 6]]]
        for _ in range(5):
            ret, frame = capture.read()
        d = 30
        size_x = 130
        size_y = 100
        center = [size_x // 2, size_y // 2]
        tmp_colors = [['' for _ in range(8)] for _ in range(6)]
        dx = [-1, -1, 1, 1]
        dy = [-1, 1, -1, 1]
        loopflag = [1 for _ in range(4)]
        while sum(loopflag):
            ret, show_frame = capture.read()
            show_frame = cv2.resize(show_frame, (size_x, size_y))
            #cv2.imshow('title',show_frame)
            hsv = cv2.cvtColor(show_frame,cv2.COLOR_BGR2HSV)
            for i in range(4):
                y = center[0] + dy[i] * d
                x = center[1] + dx[i] * d
                cv2.circle(show_frame, (y, x), 5, (0, 0, 0), thickness=3, lineType=cv2.LINE_8, shift=0)
                val = hsv[x, y]
                for j in range(6):
                    flag = True
                    for k in range(3):
                        if not ((color_low[j][k] < color_hgh[j][k] and color_low[j][k] <= val[k] <= color_hgh[j][k]) or (color_low[j][k] > color_hgh[j][k] and (color_low[j][k] <= val[k] or val[k] <= color_hgh[j][k]))):
                            flag = False
                    if flag:
                        tmp_colors[surfacenum[idx][i][0]][surfacenum[idx][i][1]] = j2color[j]
                        cv2.circle(show_frame, (y, x), 15, circlecolor[j], thickness=3, lineType=cv2.LINE_8, shift=0)
                        cv2.circle(show_frame, (y, x), 20, (0, 0, 0), thickness=2, lineType=cv2.LINE_8, shift=0)
                        loopflag[i] = 0
                        break
        #cv2.imshow('title',show_frame)
        #if cv2.waitKey(0) == 32: #スペースキーが押されたとき When space key pressed
        for i in range(4):
            colors[surfacenum[idx][i][0]][surfacenum[idx][i][1]] = tmp_colors[surfacenum[idx][i][0]][surfacenum[idx][i][1]]
        confirm_p()
        move_actuator(0, 0, -90, rpm)
        move_actuator(1, 0, 90, rpm)
        sleep(0.2)
        #cv2.destroyAllWindows()
    capture.release()
    '''
    for i in range(2):
        move_actuator(i, 0, -45, rpm)
    '''

# インスペクション処理
# Inspection
def inspection_p():
    global ans, ans_adopt, ans_cost, colors

    ans = []
    colors = [['' for _ in range(8)] for _ in range(6)]
    
    colors[0] = ['', '', 'w', 'w', '', '', '', '']
    colors[1] = ['', '', 'w', 'w', '', '', '', '']
    colors[2] = ['o', 'o', 'g', 'g', 'r', 'r', 'b', 'b']
    colors[3] = ['o', 'o', 'g', 'g', 'r', 'r', 'b', 'b']
    colors[4] = ['', '', 'y', 'y', '', '', '', '']
    colors[5] = ['', '', 'y', 'y', '', '', '', '']
    
    colors[0] = ['', '', 'w', 'g', '', '', '', '']
    colors[1] = ['', '', 'o', 'o', '', '', '', '']
    colors[2] = ['o', 'y', 'g', 'g', 'w', 'r', 'w', 'b']
    colors[3] = ['o', 'b', 'y', 'y', 'g', 'r', 'w', 'b']
    colors[4] = ['', '', 'r', 'r', '', '', '', '']
    colors[5] = ['', '', 'y', 'b', '', '', '', '']

    colors[0] = ['', '', 'w', 'o', '', '', '', '']
    colors[1] = ['', '', 'w', 'g', '', '', '', '']
    colors[2] = ['b', 'o', 'g', 'y', 'r', 'w', 'b', 'r']
    colors[3] = ['o', 'o', 'g', 'g', 'w', 'r', 'b', 'b']
    colors[4] = ['', '', 'y', 'r', '', '', '', '']
    colors[5] = ['', '', 'y', 'y', '', '', '', '']
    
    colors[0] = ['', '', 'b', 'b', '', '', '', '']
    colors[1] = ['', '', 'w', 'y', '', '', '', '']
    colors[2] = ['r', 'o', 'g', 'r', 'g', 'o', 'w', 'w']
    colors[3] = ['o', 'o', 'g', 'r', 'g', 'r', 'b', 'b']
    colors[4] = ['', '', 'y', 'w', '', '', '', '']
    colors[5] = ['', '', 'y', 'y', '', '', '', '']
    
    colors[0] = ['', '', 'b', 'r', '', '', '', '']
    colors[1] = ['', '', 'o', 'w', '', '', '', '']
    colors[2] = ['o', 'w', 'b', 'r', 'b', 'g', 'y', 'y']
    colors[3] = ['o', 'w', 'g', 'y', 'r', 'w', 'r', 'y']
    colors[4] = ['', '', 'o', 'b', '', '', '', '']
    colors[5] = ['', '', 'g', 'g', '', '', '', '']
    
    colors[0] = ['', '', 'w', 'w', '', '', '', '']
    colors[1] = ['', '', 'w', 'w', '', '', '', '']
    colors[2] = ['o', 'o', 'g', 'r', 'b', 'g', 'r', 'b']
    colors[3] = ['o', 'o', 'g', 'g', 'r', 'r', 'b', 'b']
    colors[4] = ['', '', 'y', 'y', '', '', '', '']
    colors[5] = ['', '', 'y', 'y', '', '', '', '']
    '''
    colors[0] = ['', '', 'w', 'w', '', '', '', '']
    colors[1] = ['', '', 'o', 'g', '', '', '', '']
    colors[2] = ['o', 'g', 'w', 'r', 'w', 'r', 'b', 'b']
    colors[3] = ['o', 'o', 'g', 'y', 'g', 'r', 'b', 'b']
    colors[4] = ['', '', 'y', 'r', '', '', '', '']
    colors[5] = ['', '', 'y', 'y', '', '', '', '']
    
    colors[0] = ['', '', 'g', 'w', '', '', '', '']
    colors[1] = ['', '', 'g', 'w', '', '', '', '']
    colors[2] = ['r', 'r', 'w', 'b', 'o', 'o', 'g', 'y']
    colors[3] = ['g', 'w', 'b', 'b', 'o', 'b', 'y', 'o']
    colors[4] = ['', '', 'r', 'y', '', '', '', '']
    colors[5] = ['', '', 'y', 'r', '', '', '', '']
    
    colors[0] = ['', '', 'r', 'y', '', '', '', '']
    colors[1] = ['', '', 'r', 'r', '', '', '', '']
    colors[2] = ['g', 'g', 'y', 'b', 'w', 'b', 'r', 'w']
    colors[3] = ['o', 'b', 'o', 'w', 'g', 'o', 'b', 'y']
    colors[4] = ['', '', 'y', 'o', '', '', '', '']
    colors[5] = ['', '', 'g', 'w', '', '', '', '']
    
    colors[0] = ['', '', 'w', 'b', '', '', '', '']
    colors[1] = ['', '', 'w', 'b', '', '', '', '']
    colors[2] = ['o', 'o', 'g', 'w', 'r', 'r', 'y', 'b']
    colors[3] = ['o', 'o', 'g', 'w', 'r', 'r', 'y', 'b']
    colors[4] = ['', '', 'y', 'g', '', '', '', '']
    colors[5] = ['', '', 'y', 'g', '', '', '', '']
    '''
    #detect()
    
    with open('log.txt', mode='w') as f:
        f.write(str(colors) + '\n')
    
    strt = time()
    
    # 色の情報からパズルの状態配列を作る
    # Make CO and CP array from the colors of stickers
    confirm_p()
    for i in j2color:
        cnt = 0
        for j in colors:
            if i in j:
                cnt += j.count(i)
        if cnt != 4:
            solutionvar.set('cannot solve!')
            print('cannot solve!')
            return
    puzzle = Cube()
    set_parts_color = [set(i) for i in parts_color]
    for i in range(8):
        tmp = []
        for j in range(3):
            tmp.append(colors[parts_place[i][j][0]][parts_place[i][j][1]])
        tmp1 = 'w' if 'w' in tmp else 'y'
        puzzle.Co[i] = tmp.index(tmp1)
        if not set(tmp) in set_parts_color:
            solutionvar.set('cannot solve!')
            print('cannot solve!')
            return
        puzzle.Cp[i] = set_parts_color.index(set(tmp))
    tmp2 = list(set(range(7)) - set(puzzle.Cp))
    if len(tmp2):
        tmp2 = tmp2[0]
        for i in range(7):
            if puzzle.Cp[i] > tmp2:
                puzzle.Cp[i] -= 1
    print('scramble:')
    for i in range(6):
        print(colors[i])
    print(puzzle.Cp)
    print(puzzle.Co)
    
    
    # 回転記号をくっつける
    # Join rotation arrays
    def rot_join(arr1, arr2):
        if len(arr1) == 0:
            return arr2
        elif len(arr2) == 0:
            return arr1
        if len(arr1) >= 2 and arr1[-2][0] == arr2[0][0] and abs(arr1[-1][0] - arr1[-2][0]) == 2:
            arr1[-1], arr1[-2] = arr1[-2], arr1[-1]
        if len(arr2) >= 2 and arr2[1][0] == arr1[-1][0] and abs(arr2[0][0] - arr2[1][0]) == 2:
            arr2[0], arr2[1] = arr2[1], arr2[0]
        if arr1[-1][0] != arr2[0][0]:
            arr1.extend(arr2)
            return arr1
        tmp = arr1.pop()
        rot_new = -((-tmp[1] - arr2[0][1]) % 4)
        if rot_new == 0:
            arr2 = [[j for j in i] for i in arr2[1:]]
        else:
            arr2[0][1] = rot_new
        return rot_join(arr1, arr2)
    

    #コスト計算
    # calculate cost
    change_cost = 2
    def calc_cost(arr):
        res = 0
        for j in range(len(arr)):
            if j > 0 and abs(arr[j - 1][0] - arr[j][0]) == 2:
                res -= abs(arr[j - 1][1])
                res += max(abs(arr[j - 1][1]), abs(arr[j][1]))
            elif j == 0:
                res += abs(arr[j][1])
            else:
                res += change_cost + abs(arr[j][1])
        return res

    # 深さ優先探索with枝刈り
    # DFS with pruning
    def dfs(status, depth, num, mode):
        global ans, ans_adopt, ans_cost
        return_val = False
        lst_all = [[[0, -1]], [[0, -2]], [[2, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[2, -2], [0, -1]], [[2, -1], [0, -3]]]
        if num == 0:
            lst = [[[k for k in j] for j in i] for i in lst_all[:6]]
            lst.extend([[[j[0] + 1, j[1]] for j in i] for i in lst_all[:6]])
        else:
            ad = (ans[-1][0] + 1) % 2
            lst = [[[j[0] + ad, j[1]] for j in i] for i in lst_all]
        for movs in lst:
            n_status = status.move(movs[0])
            max_rot_cost = -movs[0][1]
            if len(movs) == 2:
                max_rot_cost = max(max_rot_cost, -movs[1][1])
                n_status = n_status.move(movs[1])
            cost_pls = change_cost + max_rot_cost if num != 0 else max_rot_cost
            co_idx = n_status.co2i()
            cp_idx = n_status.cp2i()
            if num + 1 + max(co[co_idx], cp[cp_idx]) > depth + 4 or ans_cost + cost_pls + max(co_cost[co_idx], cp_cost[cp_idx]) >= ans_adopt[1]:
                continue
            ans_cost += cost_pls
            ans.extend(movs)
            if num + 1 == depth:
                tmp = neary_solved.get(cp_idx * 10000 + co_idx)
                if tmp != None:
                    ans_candidate = [[j for j in i] for i in ans]
                    pls = [[j for j in i] for i in solved_solution[tmp]]
                    ans_candidate = rot_join(ans_candidate, pls)
                    #ans_candidate.extend(pls)
                    joined_cost = calc_cost(ans_candidate)
                    if joined_cost < ans_adopt[1]:
                        with open('log.txt', mode='a') as f:
                            f.write(str(mode) + ' ' + str(joined_cost) + ' ' + str(ans_candidate) + '\n')
                        ans_adopt = [ans_candidate, joined_cost, mode]
                        print(ans_adopt)
                        return_val = True
            elif dfs(n_status, depth, num + 1, mode):
                return_val = True
            for _ in range(len(movs)):
                ans.pop()
            ans_cost -= cost_pls
        return return_val

    # IDA*
    ans_adopt = [[], 100, -1]
    former_depth = 6
    for i in range(2):
        tmp = neary_solved.get(puzzle.cp2i() * 10000 + puzzle.co2i())
        if tmp == None:
            min_depth = 1 if i == 0 else former_depth - 2
            for depth in range(min_depth, former_depth + 1):
                ans = []
                ans_cost = 0
                if dfs(puzzle, depth, 0, i):
                    former_depth = depth
                    break
        else:
            cost = 0
            ans = solved_solution[tmp]
            cost = calc_cost(ans)
            if ans_adopt[1] > cost:
                ans_adopt = [ans, cost, i]
        puzzle = puzzle.move([0, -1])
        puzzle = puzzle.move([2, -3])
    
    # 解の表示と持ち替え
    # Show the solution and regrip
    if ans_adopt[1] < 1000:
        ans = ans_adopt[0]
        min_cost = ans_adopt[1]
        with open('log.txt', mode='a') as f:
            f.write('answer\n')
            f.write(str(min_cost) + ' ' + str(ans))
        print('answer:', ans)
        solutionvar.set(str(len(ans)) + 'moves, ' + str(min_cost) + 'cost')
        solvingtimevar.set('expect:' + str(round(min_cost * 0.1, 2)) + 's')
        print('all', time() - strt, 's')
        if ans_adopt[2]:
            move_actuator(0, 0, -90, 200)
            move_actuator(1, 0, 90, 200)
            sleep(0.3)
        grab = ans[0][0] % 2
        for j in range(2):
            move_actuator(j, grab, 1000)
        sleep(0.2)
        for j in range(2):
            move_actuator(j, (grab + 1) % 2, 2000)
        print('all', time() - strt, 's')
    else:
        solutionvar.set('cannot solve!')
        print('cannot solve!')
        print('all', time() - strt, 's')

# 実際にロボットを動かす
# Move robot
def start_p():
    print('start!')
    strt_solv = time()
    i = 0
    while i < len(ans):
        if GPIO.input(21) == GPIO.LOW:
            solvingtimevar.set('emergency stop')
            print('emergency stop')
            return
        if i != 0:
            grab = ans[i][0] % 2
            for j in range(2):
                move_actuator(j, grab, 1000)
            sleep(0.07)
            for j in range(2):
                move_actuator(j, (grab + 1) % 2, 2000)
            sleep(0.07)
        ser_num = ans[i][0] // 2
        rpm = 400
        offset = -5
        move_actuator(ser_num, ans[i][0] % 2, ans[i][1] * 90 + offset, rpm)
        max_turn = abs(ans[i][1])
        flag = i < len(ans) - 1 and ans[i + 1][0] % 2 == ans[i][0] % 2
        if flag:
            move_actuator(ans[i + 1][0] // 2, ans[i + 1][0] % 2, ans[i + 1][1] * 90 + offset, rpm)
            max_turn = max(max_turn, abs(ans[i + 1][1]))
        slptim = 2 * 60 / rpm * (max_turn * 90 - offset) / 360
        sleep(slptim)
        move_actuator(ser_num, ans[i][0] % 2, -offset, rpm)
        if flag:
            move_actuator(ans[i + 1][0] // 2, ans[i + 1][0] % 2, -offset, rpm)
        #slptim = 2 * 60 / rpm * (-offset) / 360 * 0.9
        #sleep(slptim)
        if flag:
            i += 1
        i += 1
        #slptim2 = abs(2 * 60 / rpm * offset / 360)
        #sleep(slptim2)
        #print('done', i, 'sleep:', slptim, slptim2)
    solv_time = str(int((time() - strt_solv) * 1000) / 1000).ljust(5, '0')
    solvingtimevar.set(solv_time + 's')
    print('solving time:', solv_time, 's')


move_candidate = ["U", "U2", "U'", "F", "F2", "F'", "R", "R2", "R'"] #回転の候補
parts_place = [[[0, 2], [2, 0], [2, 7]], [[0, 3], [2, 6], [2, 5]], [[1, 2], [2, 2], [2, 1]], [[1, 3], [2, 4], [2, 3]], [[4, 2], [3, 1], [3, 2]], [[4, 3], [3, 3], [3, 4]], [[5, 2], [3, 7], [3, 0]], [[5, 3], [3, 5], [3, 6]]]
parts_color = [['w', 'o', 'b'], ['w', 'b', 'r'], ['w', 'g', 'o'], ['w', 'r', 'g'], ['y', 'o', 'g'], ['y', 'g', 'r'], ['y', 'b', 'o'], ['y', 'r', 'b']]

colors = [['' for _ in range(8)] for _ in range(6)]

ans_adopt = [[], 1000, -1]
ans = []
ans_cost = 0

j2color = ['g', 'b', 'r', 'o', 'y', 'w']
dic = {'w':'white', 'g':'green', 'r':'red', 'b':'blue', 'o':'magenta', 'y':'yellow'}

fac = [1]
for i in range(1, 9):
    fac.append(fac[-1] * i)

# 前計算
# Read data from csv
with open('cp.csv', mode='r') as f:
    cp = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('co.csv', mode='r') as f:
    co = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('cp_cost.csv', mode='r') as f:
    cp_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('co_cost.csv', mode='r') as f:
    co_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]
neary_solved = []
solved_solution = []
with open('solved.csv', mode='r') as f:
    for line in map(str.strip, f):
        neary_solved.append([int(i) for i in line.replace('\n', '').split(',')])
neary_solved = dict(neary_solved)
with open('solved_solution.csv', mode='r') as f:
    for line in map(str.strip, f):
        solved_solution.append(line.replace('\n', '').split(','))
for i in range(len(solved_solution)):
    tmp = []
    if solved_solution[i] == ['']:
        solved_solution[i] = []
        continue
    else:
        solved_solution[i] = [int(j) for j in solved_solution[i]]
    for j in range(0, len(solved_solution[i]), 2):
        tmp.append([solved_solution[i][j], solved_solution[i][j + 1]])
    solved_solution[i] = tmp


ser_motor = [None, None]
ser_motor[0] = serial.Serial('/dev/ttyUSB0', 9600, write_timeout=0)
ser_motor[1] = serial.Serial('/dev/ttyUSB1', 9600, write_timeout=0)

sleep(2)
release_p()
sleep(1)
for i in range(2):
    for j in range(2):
        move_actuator(j, i, 90, 250)
        move_actuator(j, i, -90, 250)

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)

root = tkinter.Tk()
root.title("2x2x2solver")
root.geometry("400x250")

grid = 20
offset = 50

entry = [[None for _ in range(8)] for _ in range(6)]

for i in range(6):
    for j in range(8):
        if 1 < i < 4 or 1 < j < 4:
            entry[i][j] = tkinter.Entry(master=root, width=2, bg='gray')
            entry[i][j].place(x = j * grid + offset, y = i * grid + offset)

inspection = tkinter.Button(root, text="inspection", command=inspection_p)
inspection.place(x=0, y=0)

start = tkinter.Button(root, text="start", command=start_p)
start.place(x=0, y=40)


solutionvar = tkinter.StringVar(master=root, value='')
solution = tkinter.Label(textvariable=solutionvar)
solution.place(x=120, y=0)

solvingtimevar = tkinter.StringVar(master=root, value='')
solvingtime = tkinter.Label(textvariable=solvingtimevar)
solvingtime.place(x=120, y=20)

grab = tkinter.Button(root, text="grab", command=grab_p)
grab.place(x=0, y=150)

release = tkinter.Button(root, text="release", command=release_p)
release.place(x=150, y=150)

calib_small = []
for i in range(4):
    calib_small.append(tkinter.Button(root, text=str(i), command=calibration(i, -3)))
    calib_small[i].place(x=275, y=i * 30)

calib_big = []
for i in range(4):
    calib_big.append(tkinter.Button(root, text=str(i), command=calibration(i, -10)))
    calib_big[i].place(x=325, y=i * 30)


root.mainloop()

for i in range(2):
    ser_motor[i].close()
