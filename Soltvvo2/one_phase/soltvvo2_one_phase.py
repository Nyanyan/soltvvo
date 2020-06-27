# coding:utf-8
'''
arr[その位置にあるパーツの番号][ステッカーの向き]
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
'''
'''
direction
UFについて、
0: UF
1: UR
2: UB
3: UL
4: FD
8: RD
12: DB
16: BD
20: LD
'''
'''
move_num
["U", "U2", "U'", "F", "F2", "F'", "R", "R2", "R'", "D", "D2", "D'", "B", "B2", "B'", "L", "L2", "L'"]
面番号
U: 0
F: 1
R: 2
D: 3
B: 4
L: 5
'''

from copy import deepcopy
from collections import deque
from time import time, sleep
import tkinter
import cv2
import numpy as np
import serial
from tkinter import messagebox
#import RPi.GPIO as GPIO

class Cube:
    def __init__(self):
        self.Co = [0, 0, 0, 0, 0, 0, 0, 0]
        self.Cp = [0, 1, 2, 3, 4, 5, 6, 7]

    # 回転処理 CP
    def move_cp(self, arr):
        surface = [[3, 1, 5, 7], [1, 0, 7, 6], [0, 2, 6, 4], [2, 3, 4, 5]]
        replace = [[1, 3, 0, 2], [3, 2, 1, 0], [2, 0, 3, 1]]
        res = [i for i in self.Cp]
        for i, j in zip(surface[arr[0]], replace[-arr[1] - 1]):
            res[i] = self.Cp[surface[arr[0]][j]]
        return res

    # 回転処理 CO
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
    def move(self, arr):
        res = Cube()
        res.Co = self.move_co(arr)
        res.Cp = self.move_cp(arr)
        return res

    # cp配列から固有の番号を作成
    def cp2i(self):
        res = 0
        for i in range(8):
            cnt = 0
            for j in self.Cp[:i]:
                if j < self.Cp[i]:
                    cnt += 1
            res += fac[7 - i] * (self.Cp[i] - cnt)
        return res
    
    # co配列から固有の番号を作成
    def co2i(self):
        res = 0
        for i in self.Co:
            res *= 3
            res += i
        return res

# アクチュエータを動かすコマンドを送る
def move_actuator(num, arg1, arg2, arg3=None):
    if arg3 == None:
        com = str(arg1) + ' ' + str(arg2)
    else:
        com = str(arg1) + ' ' + str(arg2) + ' ' + str(arg3)
    ser_motor[num].write((com + '\n').encode())
    ser_motor[num].flush()
    print('num:', num, 'command:', com)

# キューブを掴む
def grab_p():
    for i in range(2):
        for j in range(2):
            move_actuator(j, i, 1000)
        sleep(3)

# キューブを離す
def release_p():
    for i in range(2):
        for j in range(2):
            move_actuator(i, j, 2000)

def calibration(num):
    def x():
        move_actuator(num // 2, num % 2, -5)
    return x

# ボックスに色を反映させる
def confirm_p():
    global colors
    for i in range(6):
        for j in range(8):
            if (1 < i < 4 or 1 < j < 4) and colors[i][j] in j2color:
                entry[i][j]['bg'] = dic[colors[i][j]]
    # 埋まっていないところで色が確定するところを埋める
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
    for i in range(6):
        for j in range(8):
            if (1 < i < 4 or 1 < j < 4) and colors[i][j] == '':
                entry[i][j]['bg'] = 'gray'

# パズルの状態の取得
def detect():
    global idx, colors
    for i in range(2):
        move_actuator(i, 0, 1000)
    for i in range(2):
        move_actuator(i, 1, 2000)
    idx = 0
    capture = cv2.VideoCapture(0)
    while idx < 4:
        #color: g, b, r, o, y, w
        color_low = [[50, 50, 50],   [90, 50, 50],   [160, 100, 50], [170, 50, 50],  [20, 50, 50],   [0, 0, 50]] #for PC
        color_hgh = [[90, 255, 255], [140, 255, 255], [10, 255, 200], [20, 255, 255], [50, 255, 255], [179, 50, 255]]
        circlecolor = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 170, 255), (0, 255, 255), (255, 255, 255)]
        surfacenum = [[[4, 2], [4, 3], [5, 2], [5, 3]], [[2, 2], [2, 3], [3, 2], [3, 3]], [[0, 2], [0, 3], [1, 2], [1, 3]], [[3, 7], [3, 6], [2, 7], [2, 6]]]
        for _ in range(10):
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
                
        cv2.imshow('title',show_frame)
        if cv2.waitKey(0) == 32: #スペースキーが押されたとき
            for i in range(4):
                colors[surfacenum[idx][i][0]][surfacenum[idx][i][1]] = tmp_colors[surfacenum[idx][i][0]][surfacenum[idx][i][1]]
            print(idx)
            idx += 1
            confirm_p()
            offset = -5
            rpm = 100
            move_actuator(0, 0, -90 + offset, rpm)
            move_actuator(1, 0, -270 + offset, rpm)
            sleep(0.6)
            move_actuator(0, 0, -offset, rpm)
            move_actuator(1, 0, -offset, rpm)
            sleep(0.6)
        cv2.destroyAllWindows()
    capture.release()

# インスペクション処理
cnt = 0
def inspection_p():
    global ans, ans_all, total_cost, colors, cnt

    ans = []
    colors = [['' for _ in range(8)] for _ in range(6)]
    
    colors[0] = ['', '', 'w', 'g', '', '', '', '']
    colors[1] = ['', '', 'w', 'g', '', '', '', '']
    colors[2] = ['o', 'o', 'g', 'y', 'r', 'r', 'w', 'b']
    colors[3] = ['o', 'o', 'g', 'y', 'r', 'r', 'w', 'b']
    colors[4] = ['', '', 'y', 'b', '', '', '', '']
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
    
    detect()
    '''
    strt = time()
    
    # 色の情報からパズルの状態配列を作る
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

    # 前計算
    with open('cp.csv', mode='r') as f:
        cp = [int(i) for i in f.readline().replace('\n', '').split(',')]
    with open('co.csv', mode='r') as f:
        co = [int(i) for i in f.readline().replace('\n', '').split(',')]
    neary_solved = []
    solved_solution = []
    with open('solved.csv', mode='r') as f:
        for line in map(str.strip, f):
            neary_solved.append([int(i) for i in line.replace('\n', '').split(',')])
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
    #neary_solved = [[0, 0], [11824, 5576], [23616, 0], [34560, 5576], [9680, 4264], [18290, 4264], [12316, 4264], [3706, 4264], [40319, 0], [28495, 5576], [16703, 0], [5759, 5576], [30639, 4264], [22029, 4264], [28003, 4264], [36613, 4264], [10210, 0], [16313, 5576], [30109, 0], [24006, 5576], [33826, 0], [39049, 5576], [6493, 0], [1270, 5576]]
    #にぶたん
    def search(cp_num, co_num):
        l = 0
        r = len(neary_solved) - 1
        cnt = 0
        while True:
            cnt += 1
            pre_r = r
            pre_l = l
            c = (r + l) // 2
            if neary_solved[c][0] > cp_num:
                r = c
            elif neary_solved[c][0] < cp_num:
                l = c
            else:
                r = c
            if pre_r == r and pre_l == l:
                break
        for i in range(l, r + 1):
            if neary_solved[i][0] == cp_num and neary_solved[i][1] == co_num:
                return i
        return -1
    
    # 深さ優先探索with枝刈り
    def dfs(status, depth, num, flag):
        global ans, total_cost, cnt, ans_all
        flag = False
        #cost_rot = 5
        l_mov = ans[-1] if len(ans) else [-10, -10]
        lst_all = [[[0, -1], [0, -2]], [[1, -1], [1, -2]], [[2, -1], [2, -3]], [[3, -1], [3, -3]]]
        lst = []
        for i in range(4):
            if i == l_mov[0]:
                continue
            if flag and abs(l_mov[0] - i) == 2:
                continue
            lst.extend(lst_all[i])
        lst.sort(key=lambda x:-x[1])
        for mov in lst:
            cnt += 1
            n_status = status.move(mov)
            n_flag = False
            if abs(l_mov[0] - mov[0]) == 2:
                n_flag = True
            co_idx = n_status.co2i()
            cp_idx = n_status.cp2i()
            if len(ans) + max(co[co_idx], cp[cp_idx]) - 5 > depth:
                continue
            ans.append(mov)
            tmp = search(cp_idx, co_idx)
            if tmp != -1:
                ans_tmp = [[j for j in i] for i in ans]
                ans_tmp.extend(reversed(solved_solution[tmp]))
                print(ans_tmp)
                ans_all.append(ans_tmp)
                flag = True
            elif dfs(n_status, depth, num + 1, n_flag):
                flag = True
            ans.pop()
        return flag

    # IDA*
    for depth in range(1, 15):
        cnt = 0
        ans = []
        if dfs(puzzle, depth, 0, False):
            print(depth, cnt)
            break
        print(depth, cnt)
    print(str(len(ans_all)) + ' answers found')
    if ans_all:
        min_cost = 1000
        idx = -1
        for ii, ans in enumerate(ans_all):
            cost = 0
            cost_rot = 5
            for i in range(len(ans)):
                if i > 0 and abs(ans[i - 1][0] - ans[i][0]) == 2:
                    cost -= abs(ans[i - 1][1])
                    cost += max(abs(ans[i - 1][1]), abs(ans[i][1]))
                else:
                    cost += cost_rot + abs(ans[i][1])
            if min_cost > cost:
                min_cost = cost
                idx = ii
        print('answer:', ans_all[idx])
        solutionvar.set(str(len(ans)) + 'moves, ' + str(min_cost) + 'cost')
        print('all', time() - strt, 's')
    else:
        solutionvar.set('cannot solve!')
        print('cannot solve!')
        print('all', time() - strt, 's')

# 実際にロボットを動かす
def start_p():
    print('start!')
    strt_solv = time()
    i = 0
    while i < len(ans):
        if GPIO.input(4) == GPIO.LOW:
            solvingtimevar.set('emergency stop')
            print('emergency stop')
            return
        grab = ans[i][0] % 2
        for j in range(2):
            move_actuator(j, grab, 1000)
        sleep(0.4)
        for j in range(2):
            move_actuator(j, (grab + 1) % 2, 2000)
        sleep(0.1)
        ser_num = ans[i][0] // 2
        rpm = 100
        offset = -5
        move_actuator(ser_num, ans[i][0] % 2, ans[i][1] * 90 + offset, rpm)
        max_turn = abs(ans[i][1])
        flag = i < len(ans) - 1 and ans[i + 1][0] % 2 == ans[i][0] % 2
        if flag:
            move_actuator(ans[i + 1][0] // 2, ans[i + 1][0] % 2, ans[i + 1][1] * 90 + offset, rpm)
            max_turn = max(max_turn, abs(ans[i + 1][1]))
        slptim = 60 / rpm * (max_turn * 90 + offset) / 360 * 1.1
        sleep(slptim)
        move_actuator(ser_num, ans[i][0] % 2, -offset, rpm)
        if flag:
            move_actuator(ans[i + 1][0] // 2, ans[i + 1][0] % 2, -offset, rpm)
            i += 1
        i += 1
        slptim2 = abs(60 / rpm * offset / 360) * 1.1
        sleep(slptim2)
        print('done', i, 'sleep:', slptim, slptim2)
    solv_time = time() - strt_solv
    solvingtimevar.set(str(round(solv_time, 3)) + 's')
    print('solving time:', solv_time, 's')


move_candidate = ["U", "U2", "U'", "F", "F2", "F'", "R", "R2", "R'"] #回転の候補
parts_place = [[[0, 2], [2, 0], [2, 7]], [[0, 3], [2, 6], [2, 5]], [[1, 2], [2, 2], [2, 1]], [[1, 3], [2, 4], [2, 3]], [[4, 2], [3, 1], [3, 2]], [[4, 3], [3, 3], [3, 4]], [[5, 2], [3, 7], [3, 0]], [[5, 3], [3, 5], [3, 6]]]
parts_color = [['w', 'o', 'b'], ['w', 'b', 'r'], ['w', 'g', 'o'], ['w', 'r', 'g'], ['y', 'o', 'g'], ['y', 'g', 'r'], ['y', 'b', 'o'], ['y', 'r', 'b']]

colors = [['' for _ in range(8)] for _ in range(6)]

ans_all = []
ans = []
total_cost = 0

j2color = ['g', 'b', 'r', 'o', 'y', 'w']
dic = {'w':'white', 'g':'green', 'r':'red', 'b':'blue', 'o':'magenta', 'y':'yellow'}

fac = [1]
for i in range(1, 9):
    fac.append(fac[-1] * i)

'''
ser_motor = [None, None]
ser_motor[0] = serial.Serial('/dev/ttyUSB0', 9600, write_timeout=0)
ser_motor[1] = serial.Serial('/dev/ttyUSB1', 9600, write_timeout=0)

sleep(2)
release_p()
sleep(1)
for i in range(2):
    for j in range(2):
        move_actuator(j, i, 90, 100)
        move_actuator(j, i, -90, 100)

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)
'''
root = tkinter.Tk()
root.title("2x2x2solver")
root.geometry("300x150")

grid = 20
offset = 30

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
solution.place(x=70, y=0)

solvingtimevar = tkinter.StringVar(master=root, value='')
solvingtime = tkinter.Label(textvariable=solvingtimevar)
solvingtime.place(x=120, y=20)

grab = tkinter.Button(root, text="grab", command=grab_p)
grab.place(x=0, y=120)

release = tkinter.Button(root, text="release", command=release_p)
release.place(x=120, y=120)

calib = []
for i in range(4):
    calib.append(tkinter.Button(root, text=str(i), command=calibration(i)))
    calib[i].place(x=230, y=i * 30)
'''
stop = tkinter.Button(root, text="STOP",command="break")
stop.place(x=230, y=120)
'''
root.mainloop()

for i in range(2):
    ser_motor[i].close()
