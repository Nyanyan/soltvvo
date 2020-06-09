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
L [欠番] [6, 0] R
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

class Cube:
    def __init__(self):
        self.Co = [0, 0, 0, 0, 0, 0, 0]
        self.Cp = [0, 1, 2, 3, 4, 5, 6]
        self.Moves = []
        self.Movnum = 0

    # 回転処理 CP
    def move_cp(self, num):
        surface = [[0, 1, 2, 3], [2, 3, 4, 5], [3, 1, 5, 6]]
        replace = [[2, 0, 3, 1], [3, 2, 1, 0], [1, 3, 0, 2]]
        idx = num // 3
        res = Cube()
        res.Cp = [i for i in self.Cp]
        for i, j in zip(surface[idx], replace[num % 3]):
            res.Cp[i] = self.Cp[surface[idx][j]]
        res.Moves = [i for i in self.Moves]
        res.Moves.append(num)
        res.Movnum = self.Movnum + 1
        res.Movnum += 1 if len(self.Moves) >= 2 and num // 3 != self.Moves[-1] // 3 and num // 3 != self.Moves[-2] // 3 else 0
        res.Movnum += 1 if len(self.Moves) < 2 and num // 3 == 1 else 0
        return res

    # 回転処理 CO
    def move_co(self, num):
        surface = [[0, 1, 2, 3], [2, 3, 4, 5], [3, 1, 5, 6]]
        replace = [[2, 0, 3, 1], [3, 2, 1, 0], [1, 3, 0, 2]]
        pls = [2, 1, 1, 2]
        idx = num // 3
        res = Cube()
        res.Co = [i for i in self.Co]
        for i, j in zip(surface[idx], replace[num % 3]):
            res.Co[i] = self.Co[surface[idx][j]]
        if num // 3 != 0 and num % 3 != 1:
            for i in range(4):
                res.Co[surface[idx][i]] += pls[i]
                res.Co[surface[idx][i]] %= 3
        res.Moves = [i for i in self.Moves]
        res.Moves.append(num)
        res.Movnum = self.Movnum + 1
        res.Movnum += 1 if len(self.Moves) >= 2 and num // 3 != self.Moves[-1] // 3 and num // 3 != self.Moves[-2] // 3 else 0
        res.Movnum += 1 if len(self.Moves) < 2 and num // 3 == 1 else 0
        return res

    # 回転番号に則って実際にパズルの状態配列を変化させる
    def move(self, num):
        res = Cube()
        res = self.move_co(num)
        res.Cp = self.move_cp(num).Cp
        return res

    # cp配列から固有の番号を作成
    def cp2i(self):
        res = 0
        marked = set([])
        for i in range(7):
            res += fac[6 - i] * len(set(range(self.Cp[i])) - marked)
            marked.add(self.Cp[i])
        return res
    
    # co配列から固有の番号を作成
    def co2i(self):
        res = 0
        for i in self.Co:
            res *= 3
            res += i
        return res

# 回転番号を回転記号に変換
def num2moves(arr):
    res = ''
    for i in arr:
        res += move_candidate[i] + ' '
    return res

# 回転記号番号の配列から回すモーターを決定する
def proc_motor(rot, num, direction):
    if num == len(ans):
        return rot, num, direction
    turn_arr = [1, 2, -1]
    r_arr = [[-1, 2, 4, -1, 5, 1], [5, -1, 0, 2, -1, 3], [1, 3, -1, 4, 0, -1], [-1, 5, 1, -1, 2, 4], [2, -1, 3, 5, -1, 0], [4, 0, -1, 1, 3, -1]]
    f_arr = [[1, 2, 4, 5], [3, 2, 0, 5], [3, 4, 0, 1], [4, 2, 1, 5], [3, 5, 0, 2], [3, 1, 0, 4]]
    regrip_arr = [[4, 8, 16, 20, 12, 9, 2, 23, 15, 17, 3, 7, 18, 10, 6, 22, 14, 21, 0, 11, 13, 5, 1, 19], [21, 5, 9, 17, 20, 13, 10, 3, 4, 12, 18, 0, 23, 19, 11, 7, 8, 15, 22, 1, 16, 14, 6, 2]]
    regrip_rot = [[[1, 1], [3, -1]], [[0, 1], [2, -1]]]
    u_face = direction // 4
    f_face = f_arr[u_face][direction % 4]
    r_face = r_arr[u_face][f_face]
    d_face = (u_face + 3) % 6
    b_face = (f_face + 3) % 6
    l_face = (r_face + 3) % 6
    move_able = [f_face, r_face, b_face, l_face]
    move_face = ans[num] // 3
    move_amount = turn_arr[ans[num] % 3]
    if move_face == u_face or move_face == d_face:
        rot_tmp = [[i for i in rot] for _ in range(2)]
        direction_tmp = [-1, -1]
        num_tmp = [num, num]
        for j in range(2):
            rot_tmp[j].extend(regrip_rot[j])
            direction_tmp[j] = regrip_arr[j][direction]
            rot_tmp[j], num_tmp[j], direction_tmp[j] = proc_motor(rot_tmp[j], num_tmp[j], direction_tmp[j])
        idx = 0 if len(rot_tmp[0]) < len(rot_tmp[1]) else 1
        rot_res = rot_tmp[idx]
        num_res = num_tmp[idx]
        direction_res = direction_tmp[idx]
    else:
        tmp = move_able.index(move_face)
        rot_res = [i for i in rot]
        rot_res.append([tmp, move_amount])
        rot_res, num_res, direction_res = proc_motor(rot_res, num + 1, direction)
    return rot_res, num_res, direction_res

# ロボットの手順の最適化
def rot_optimise():
    global rot
    i = 0
    tmp_arr = [2, -1, 0, 1, 2, -1, 0]
    while i < len(rot):
        if i < len(rot) - 1 and rot[i][0] == rot[i + 1][0]:
            tmp = tmp_arr[rot[i][1] + rot[i + 1][1] + 2]
            del rot[i + 1]
            if tmp == 0:
                del rot[i]
                i -= 1
            else:
                rot[i][1] = tmp
        elif i < len(rot) - 2 and rot[i][0] == rot[i + 2][0] and rot[i][0] % 2 == rot[i + 1][0] % 2:
            tmp = tmp_arr[rot[i][1] + rot[i + 2][1] + 2]
            del rot[i + 2]
            if tmp == 0:
                del rot[i]
                i -= 1
            else:
                rot[i][1] = tmp
        i += 1

def move_motor_solenoid(num, com):
    ser_motor[num].flush()
    while True:
        try:
            ser_motor[num].write((com + '\n').encode())
            ser_motor[num].flush()
            break
        except:
            continue
    print('num:', num, 'command:', com)

def wait_motor_solenoid(num):
    tmp = ''
    while not len(tmp):
        #print(ser_motor[num].inWaiting())
        if ser_motor[num].inWaiting():
            tmp = ser_motor[num].readline().decode('utf8', 'ignore').replace('\n', '')
    ser_motor[num].flush()

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
    #color_low = [[50, 50, 50],   [80, 50, 50],    [160, 150, 50], [170, 50, 50],   [20, 50, 50],   [0, 0, 50]] #for RPi
    #color_hgh = [[80, 255, 255], [140, 255, 255], [5, 255, 200], [20, 255, 255], [40, 255, 255], [179, 50, 255]]
    color_low = [[40, 50, 50],   [90, 50, 50],    [160, 150, 50], [170, 50, 50],   [20, 50, 50],   [0, 0, 50]] #for PC
    color_hgh = [[90, 255, 255], [140, 255, 255], [10, 255, 200], [20, 255, 255], [40, 255, 255], [179, 50, 255]]
    circlecolor = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 170, 255), (0, 255, 255), (255, 255, 255)]
    surfacenum = [[[4, 2], [4, 3], [5, 2], [5, 3]], [[2, 2], [2, 3], [3, 2], [3, 3]], [[0, 2], [0, 3], [1, 2], [1, 3]], [[3, 7], [3, 6], [2, 7], [2, 6]]]
    if idx >= 4:
        return
    ret, frame = capture.read()
    size_x = 200
    size_y = 150
    frame = cv2.resize(frame, (size_x, size_y))
    show_frame = deepcopy(frame)
    d = 50
    center = [size_x // 2, size_y // 2]
    tmp_colors = [['' for _ in range(8)] for _ in range(6)]
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    dx = [-1, -1, 1, 1]
    dy = [-1, 1, -1, 1]
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
                #print(j2color[j], end=' ')
                cv2.circle(show_frame, (y, x), 15, circlecolor[j], thickness=3, lineType=cv2.LINE_8, shift=0)
                break
    '''
    sleep(1)
    '''
    if cv2.waitKey(1) & 0xFF == ord('n'):
        for i in range(4):
            colors[surfacenum[idx][i][0]][surfacenum[idx][i][1]] = tmp_colors[surfacenum[idx][i][0]][surfacenum[idx][i][1]]
        print(idx)
        idx += 1
        confirm_p()
    '''
    for i in range(4):
        colors[surfacenum[idx][i][0]][surfacenum[idx][i][1]] = tmp_colors[surfacenum[idx][i][0]][surfacenum[idx][i][1]]
    print(idx)
    idx += 1
    confirm_p()
    move_motor(0, '0 -1e')
    move_motor(1, '3 1e')
    wait_motor(0)
    wait_motor(1)
    idx += 1
    '''
    cv2.imshow('title',show_frame)
    root.after(5, detect)

# インスペクション処理
def inspection_p():
    global ans, rot

    strt = time()
    
    # 色の情報からパズルの状態配列を作る
    confirm_p()
    puzzle = Cube()
    set_parts_color = [set(i) for i in parts_color]
    for i in range(7):
        tmp = []
        for j in range(3):
            tmp.append(colors[parts_place[i][j][0]][parts_place[i][j][1]])
        tmp1 = 'w' if 'w' in tmp else 'y'
        puzzle.Co[i] = tmp.index(tmp1)
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

    # パズルの向きから、solved状態の配列を作る
    solved_color = [['' for _ in range(8)] for _ in range(6)]
    solved_color[5][2] = colors[5][2]
    solved_color[3][7] = colors[3][7]
    solved_color[3][0] = colors[3][0]
    solved_color[2][2] = j2color[(j2color.index(solved_color[3][7]) // 2) * 2 - j2color.index(solved_color[3][7]) % 2 + 1]
    solved_color[3][4] = j2color[(j2color.index(solved_color[3][0]) // 2) * 2 - j2color.index(solved_color[3][0]) % 2 + 1]
    solved_color[0][2] = j2color[(j2color.index(solved_color[5][2]) // 2) * 2 - j2color.index(solved_color[5][2]) % 2 + 1]
    for i in range(6):
        for j in range(8):
            if (1 < i < 4 or 1 < j < 4) and solved_color[i][j] == '':
                if i % 2 and j % 2:
                    dx = [0, -1, -1]
                    dy = [-1, -1, 0]
                elif i % 2 and (not j % 2):
                    dx = [0, 1, 1]
                    dy = [-1, -1, 0]
                elif (not i % 2) and j % 2:
                    dx = [-1, -1, 0]
                    dy = [0, 1, 1]
                elif (not i % 2) and (not j % 2):
                    dx = [1, 1, 0]
                    dy = [0, 1, 1]
                #print(i, j, dx, dy)
                for k in range(3):
                    if solved_color[i + dy[k]][j + dx[k]] != '':
                        solved_color[i][j] = solved_color[i + dy[k]][j + dx[k]]
    solved = Cube()
    for i in range(7):
        tmp = []
        for j in range(3):
            tmp.append(solved_color[parts_place[i][j][0]][parts_place[i][j][1]])
        tmp1 = 'w' if 'w' in tmp else 'y'
        solved.Co[i] = tmp.index(tmp1)
        solved.Cp[i] = set_parts_color.index(set(tmp))
    tmp2 = list(set(range(7)) - set(solved.Cp))
    if len(tmp2):
        tmp2 = tmp2[0]
        for i in range(7):
            if solved.Cp[i] > tmp2:
                solved.Cp[i] -= 1
    print('solved:')
    for i in range(6):
        print(solved_color[i])
    print(solved.Cp)
    print(solved.Co)
    print('pre', time() - strt, 's')

    '''
    # 枝刈り用のco配列とcp配列
    inf = 100
    cp = [inf for _ in range(fac[7])]
    cp_solved = Cube()
    cp_solved.Cp = solved.Cp
    cp[cp_solved.cp2i()] = 0
    que = deque([cp_solved])
    while len(que):
        status = que.popleft()
        num = len(status.Moves)
        l_mov = status.Moves[-1] if num else -1
        t = (l_mov // 3) * 3
        lst = set(range(9)) - set([t, t + 1, t + 2])
        for mov in lst:
            n_status = status.move_cp(mov)
            n_idx = n_status.cp2i()
            if cp[n_idx] == inf:
                cp[n_idx] = status.Movnum
                que.append(n_status)
    print('cp:', time() - strt, 's')
    co = [inf for _ in range(3 ** 7)]
    co_solved = Cube()
    co_solved.Co = solved.Co
    co[co_solved.co2i()] = 0
    que = deque([co_solved])
    while len(que):
        status = que.popleft()
        num = len(status.Moves)
        l_mov = status.Moves[-1] if num else -1
        t = (l_mov // 3) * 3
        lst = set(range(9)) - set([t, t + 1, t + 2])
        for mov in lst:
            n_status = status.move_co(mov)
            n_idx = n_status.co2i()
            if co[n_idx] == inf:
                co[n_idx] = status.Movnum
                que.append(n_status)
    print('co:', time() - strt, 's')
    '''
    
    # 枝刈り用のco配列とcp配列
    direction = -1
    direction_arr = [21, 12, 15, 18, 2, 22, 20, 4, 8, 13, 23, 1, 6, 0, 3, 9, 11, 16, 14, 7, 5, 19, 17, 10]
    for idx, d in enumerate(direction_arr):
        if solved_color[5][2] == parts_color[d // 3][d % 3] and solved_color[3][7] == parts_color[d // 3][(d % 3 + 1) % 3]:
            direction = idx
    with open('cp'+ str(direction) + '.csv', mode='r') as f:
        cp = [int(i) for i in f.readline().replace('\n', '').split(',')]
    with open('co'+ str(direction) + '.csv', mode='r') as f:
        co = [int(i) for i in f.readline().replace('\n', '').split(',')]

    # IDA*
    for depth in range(1, 16):
        que = [puzzle]
        while que and not ans:
            status = que.pop()
            num = len(status.Moves)
            l_mov = status.Moves[-1] if num else -1
            t = (l_mov // 3) * 3
            lst = set(range(9)) - set([t, t + 1, t + 2])
            for mov in lst:
                n_status = status.move(mov)
                if n_status.Cp == solved.Cp and n_status.Co == solved.Co:
                    ans = n_status.Moves
                    break
                if n_status.Movnum + max(cp[n_status.cp2i()], co[n_status.co2i()]) < depth:
                    que.append(n_status)
        if ans:
            break
    print('answer:', num2moves(ans))
    print('IDA*', time() - strt, 's')

    if ans:
        solution = tkinter.Label(text=num2moves(ans))
        solution.place(x = 0, y = 9 * grid)
        rot, _, _ = proc_motor(rot, 0, 4)
        print('before:', len(rot))
        rot_optimise()
        print('after:', len(rot))
        print(rot)
        print('all', time() - strt, 's')
        start.pack()
    else:
        print('cannot solve!')

# 実際にロボットを動かす
def start_p():
    print('start!')
    strt_solv = time()
    i = 0
    while i < len(rot):
        grab = sorted([rot[i][0], (rot[i][0] + 2) % 4])
        move_motor_solenoid(0, str(grab[0]) + ' 0')
        wait_motor_solenoid(0)
        sleep(0.2)
        ser_num = rot[i][0] // 2
        if ser_num == 0:
            move_motor_solenoid(ser_num, str(rot[i][0]) + ' ' + str(rot[i][1]))
            wait_motor_solenoid(ser_num)
        print('done', i)
        i += 1        
    '''
    while i < len(rot):
        grab = sorted([rot[i][0], (rot[i][0] + 2) % 4])
        for j in range(2):
            ser_motor[j].write((str(grab[j]) + ' 0').encode())
        sleep(0.2)
        ser_num = rot[i][0] // 2
        move_motor(ser_num, str(rot[i][0]) + ' ' + str(rot[i][1]))
        if i < len(rot) - 1 and ser_num != rot[i + 1][0] // 2:
            move_motor(rot[i + 1][0] // 2, str(rot[i + 1][0]) + ' ' + str(rot[i + 1][1]))
            wait_motor(rot[i + 1][0] // 2)
            i += 1
        wait_motor(ser_num)
        print('done', i)
        i += 1
    '''
    print('solving time:', time() - strt_solv, 's')


move_candidate = ["U", "U2", "U'", "F", "F2", "F'", "R", "R2", "R'"] #回転の候補
parts_place = [[[0, 2], [2, 0], [2, 7]], [[0, 3], [2, 6], [2, 5]], [[1, 2], [2, 2], [2, 1]], [[1, 3], [2, 4], [2, 3]], [[4, 2], [3, 1], [3, 2]], [[4, 3], [3, 3], [3, 4]], [[5, 3], [3, 5], [3, 6]], [[5, 2], [3, 7], [3, 0]]]
parts_color = [['w', 'o', 'b'], ['w', 'b', 'r'], ['w', 'g', 'o'], ['w', 'r', 'g'], ['y', 'o', 'g'], ['y', 'g', 'r'], ['y', 'r', 'b'], ['y', 'b', 'o']]


colors = [['' for _ in range(8)] for _ in range(6)]
ans = []
rot = []

j2color = ['g', 'b', 'r', 'o', 'y', 'w']
dic = {'w':'white', 'g':'green', 'r':'red', 'b':'blue', 'o':'magenta', 'y':'yellow'}
idx = 0

fac = [1]
for i in range(1, 8):
    fac.append(fac[-1] * i)

ser_motor = [None, None]
#ser_motor[0] = serial.Serial('COM8', 1200, write_timeout=0) #/dev/ttyUSB0
#ser_motor[1] = serial.Serial('COM6', 9600)

root = tkinter.Tk()
root.title("2x2x2solver")
root.geometry("300x200")
canvas = tkinter.Canvas(root, width = 300, height = 200)
canvas.place(x=0,y=0)

grid = 20
offset = 50

entry = [[None for _ in range(8)] for _ in range(6)]

for i in range(6):
    for j in range(8):
        if 1 < i < 4 or 1 < j < 4:
            entry[i][j] = tkinter.Entry(width=2, bg='gray')
            entry[i][j].place(x = j * grid + offset, y = i * grid + offset)

inspection = tkinter.Button(canvas, text="inspection", command=inspection_p)
inspection.pack()

start = tkinter.Button(canvas, text="start", command=start_p)
start.pack()

capture = cv2.VideoCapture(0)

root.after(5, detect)
root.mainloop()

capture.release()
ser_motor[0].close()