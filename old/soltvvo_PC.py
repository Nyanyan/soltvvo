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

from copy import deepcopy
from collections import deque
from math import factorial
from time import time
import tkinter
import cv2
import numpy as np

# 回転番号に則って実際にパズルの状態配列を変化させる
def move(n_arr, num):
    idx = num // 3
    rot_arr1 = np.matrix([[n_arr[surface[idx][i]][0] for i in range(j * 2, j * 2 + 2)] for j in range(2)])
    rot_arr2 = np.matrix([[n_arr[surface[idx][i]][1] for i in range(j * 2, j * 2 + 2)] for j in range(2)])
    rot_arr1 = np.rot90(rot_arr1, 3 - num % 3).tolist()
    rot_arr2 = np.rot90(rot_arr2, 3 - num % 3).tolist()
    tmp = [[[2, 1], [1, 2]], [[0, 0], [0, 0]], [[2, 1], [1, 2]]]
    if num // 3 != 0:
        rot_arr2 = [[(rot_arr2[j][i] + tmp[num % 3][j][i]) % 3 for i in range(2)] for j in range(2)]
    for i in range(4):
        n_arr[surface[idx][i]][0] = rot_arr1[i // 2][i % 2]
        n_arr[surface[idx][i]][1] = rot_arr2[i // 2][i % 2]
    return n_arr

# スクランブルする 使用されていない
def scrm(n_arr, move_num):
    if len(scramble_arr) == move_num:
        return n_arr
    n_arr = move(n_arr, scramble_arr[move_num])
    n_arr = scrm(n_arr, move_num + 1)
    return n_arr

# 回転番号を回転記号に変換
def num2moves(arr):
    res = ''
    for i in arr:
        res += move_candidate[i] + ' '
    return res

# 回転記号を回転番号に変換 使用されていない
def moves2num(arr):
    res = []
    for i in arr:
        res.append(move_candidate.index(i))
    return res

# パズルの状態配列固有の番号を返す
def arr2num(arr):
    res1 = 0
    marked = set([])
    for i in range(7):
        res1 += factorial(6 - i) * len(set(range(arr[i][0])) - marked)
        marked.add(arr[i][0])
    res2 = 0
    for i in range(6):
        res2 *= 3
        res2 += arr[i][1]
    return res1, res2

# 逆手順を返す
def reverse(arr):
    arr = list(reversed(arr))
    for i in range(len(arr)):
        if arr[i] % 3 == 0:
            arr[i] += 2
        elif arr[i] % 3 == 2:
            arr[i] -= 2
    return arr

# ボックスから色の情報を取ってくる
def confirm_p():
    global colors

    # ボックスから色の情報を取る
    for i in range(6):
        for j in range(8):
            #colors[i][j] = ''
            if 1 < i < 4 or 1 < j < 4:
                #tmp = entry[i][j].get()
                tmp = colors[i][j]
                if tmp in j2color:
                    colors[i][j] = tmp
                    entry[i][j]['bg'] = dic[tmp]
                else:
                    colors[i][j] = ''
    
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

# メイン処理
def start_p():
    strt = time()
    
    # 色の情報からパズルの状態配列を作る
    confirm_p()
    puzzle = [[i, 0] for i in range(7)]
    set_parts_color = [set(i) for i in parts_color]
    for i in range(7):
        tmp = []
        for j in range(3):
            tmp.append(colors[parts_place[i][j][0]][parts_place[i][j][1]])
        tmp1 = 'w' if 'w' in tmp else 'y'
        puzzle[i][1] = tmp.index(tmp1)
        puzzle[i][0] = set_parts_color.index(set(tmp))
    tmp = [puzzle[i][0] for i in range(7)]
    tmp2 = list(set(range(7)) - set(tmp))
    if len(tmp2):
        tmp2 = tmp2[0]
        for i in range(7):
            if puzzle[i][0] > tmp2:
                puzzle[i][0] -= 1
    print('scramble:')
    for i in range(6):
        print(colors[i])
    print(puzzle)

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
    solved = [[-1, -1] for _ in range(7)]
    for i in range(7):
        tmp = []
        for j in range(3):
            tmp.append(solved_color[parts_place[i][j][0]][parts_place[i][j][1]])
        tmp1 = 'w' if 'w' in tmp else 'y'
        solved[i][1] = tmp.index(tmp1)
        solved[i][0] = set_parts_color.index(set(tmp))
    tmp = [solved[i][0] for i in range(7)]
    tmp2 = list(set(range(7)) - set(tmp))
    if len(tmp2):
        tmp2 = tmp2[0]
        for i in range(7):
            if solved[i][0] > tmp2:
                solved[i][0] -= 1
    print('solved:')
    for i in range(6):
        print(solved_color[i])
    print(solved)

    # 双方向幅優先探索
    que = deque([[deepcopy(puzzle), 0, [], 0], [deepcopy(solved), 0, [], 1]])
    marked = [[[[] for _ in range(3 ** 6)] for _ in range(factorial(7))] for _ in range(2)]
    idx1, idx2 = arr2num(solved)
    marked[0][idx1][idx2] = [-1]
    idx1, idx2 = arr2num(puzzle)
    marked[1][idx1][idx2] = [-1]
    flag = True
    fins = -1
    ans = []
    while flag and len(que):
        tmp = que.popleft()
        arr = tmp[0]
        num = tmp[1]
        moves = tmp[2]
        mode = tmp[3]
        if arr == solved and mode == 0:
            ans = moves
            fins = time()
            flag = False
        elif arr == puzzle and mode == 1:
            ans = reverse(moves)
            fins = time()
            flag = False
        if num < 6:
            for i in range(9):
                if num != 0 and i // 3 == moves[-1] // 3:
                    continue
                n_arr = move(deepcopy(arr), i)
                n_moves = deepcopy(moves)
                n_moves.append(i)
                if n_arr == solved and mode == 0:
                    ans = n_moves
                    fins = time()
                    flag = False
                    break
                elif n_arr == puzzle and mode == 1:
                    ans = reverse(n_moves)
                    fins = time()
                    flag = False
                    break
                idx1, idx2 = arr2num(n_arr)
                if len(marked[(mode + 1) % 2][idx1][idx2]):
                    res = []
                    if mode == 0:
                        res = n_moves
                        res.extend(reverse(marked[(mode + 1) % 2][idx1][idx2]))
                    else:
                        res = marked[(mode + 1) % 2][idx1][idx2]
                        res.extend(reverse(n_moves))
                    ans = res
                    fins = time()
                    flag = False
                    break
                elif len(marked[mode][idx1][idx2]):
                    continue
                marked[mode][idx1][idx2] = n_moves
                que.append([n_arr, num + 1, n_moves, mode])
    print('answer:', num2moves(ans))
    print(fins - strt, 's')

move_candidate = ["U", "U2", "U'", "F", "F2", "F'", "R", "R2", "R'"] #回転の候補
surface = [[0, 1, 2, 3], [2, 3, 4, 5], [3, 1, 5, 6]]

colors = [['' for _ in range(8)] for _ in range(6)]


j2color = ['g', 'b', 'r', 'o', 'y', 'w']


parts_place = [[[0, 2], [2, 0], [2, 7]], [[0, 3], [2, 6], [2, 5]], [[1, 2], [2, 2], [2, 1]], [[1, 3], [2, 4], [2, 3]], [[4, 2], [3, 1], [3, 2]], [[4, 3], [3, 3], [3, 4]], [[5, 3], [3, 5], [3, 6]], [[5, 2], [3, 7], [3, 0]]]
parts_color = [['w', 'o', 'b'], ['w', 'b', 'r'], ['w', 'g', 'o'], ['w', 'r', 'g'], ['y', 'o', 'g'], ['y', 'g', 'r'], ['y', 'r', 'b'], ['y', 'b', 'o']]


#scramble = list(input().split(' '))
root = tkinter.Tk()
root.title("2x2x2solver")
root.geometry("300x200")
canvas = tkinter.Canvas(root, width = 300, height = 200)
canvas.place(x=0,y=0)

grid = 20

offset = 50

entry = [[None for _ in range(8)] for _ in range(6)]

dic = {'w':'white', 'g':'green', 'r':'red', 'b':'blue', 'o':'magenta', 'y':'yellow'}

for i in range(6):
    for j in range(8):
        if 1 < i < 4 or 1 < j < 4:
            entry[i][j] = tkinter.Entry(width=2, bg='gray')
            entry[i][j].place(x = j * grid + offset, y = i * grid + offset)

confirm = tkinter.Button(canvas, text="confirm", command=confirm_p)
confirm.pack()

start = tkinter.Button(canvas, text="start", command=start_p)
start.pack()


# カメラでパズルの色を取ってくる
capture = cv2.VideoCapture(0)
surfacenum = [[[2, 0], [2, 1], [3, 0], [3, 1]], [[2, 2], [2, 3], [3, 2], [3, 3]], [[2, 4], [2, 5], [3, 4], [3, 5]], [[2, 6], [2, 7], [3, 6], [3, 7]]] #[[0, 2], [0, 3], [1, 2], [1, 3]], [[4, 2], [4, 3], [5, 2], [5, 3]]
#j2color = ['g', 'b', 'r', 'o', 'y', 'w']
color_low = [[50, 50, 50],   [80, 50, 50],    [160, 100, 50], [0, 50, 50],   [20, 50, 50],   [0, 0, 50]]
color_hgh = [[80, 255, 255], [140, 255, 255], [10, 255, 200], [20, 255, 255], [40, 255, 255], [179, 50, 255]]
circlecolor = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 170, 255), (0, 255, 255), (255, 255, 255)]
idx = 0

def detect():
    global idx, colors
    if idx >= 4:
        return
    ret, frame = capture.read()
    size_x = 400
    size_y = 300
    windowsize = (size_x, size_y)
    frame = cv2.resize(frame, windowsize)
    show_frame = deepcopy(frame)
    d = 70
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
        #print(val, end='')
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
    #print('')
    if cv2.waitKey(1) & 0xFF == ord('n'):
        for i in range(4):
            colors[surfacenum[idx][i][0]][surfacenum[idx][i][1]] = tmp_colors[surfacenum[idx][i][0]][surfacenum[idx][i][1]]
        print(idx)
        idx += 1
        confirm_p()
        '''
        for i in range(6):
            print(tmp_colors[i])
        print('')
        for i in range(6):
            print(colors[i])
        print('')
        '''
    cv2.imshow('title',show_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    root.after(5, detect)

root.after(5, detect)
root.mainloop()

capture.release()