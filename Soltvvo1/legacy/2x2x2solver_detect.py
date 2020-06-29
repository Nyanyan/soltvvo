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
import cv2
import numpy as np

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

def scrm(n_arr, move_num):
    if len(scramble_arr) == move_num:
        return n_arr
    n_arr = move(n_arr, scramble_arr[move_num])
    n_arr = scrm(n_arr, move_num + 1)
    return n_arr

def num2moves(arr):
    res = ''
    for i in arr:
        res += move_candidate[i] + ' '
    return res

def moves2num(arr):
    res = []
    for i in arr:
        res.append(move_candidate.index(i))
    return res

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

def reverse(arr):
    arr = list(reversed(arr))
    for i in range(len(arr)):
        if arr[i] % 3 == 0:
            arr[i] += 2
        elif arr[i] % 3 == 2:
            arr[i] -= 2
    return arr

move_candidate = ["U", "U2", "U'", "F", "F2", "F'", "R", "R2", "R'"] #回転の候補

puzzle = [[i, 0] for i in range(7)] #パズルの状態

puzzle_back = [[i, 0] for i in range(7)] #パズルの状態

solved = [[i, 0] for i in range(7)]

surface = [[0, 1, 2, 3], [2, 3, 4, 5], [3, 1, 5, 6]]

colors_low = [np.array([100, 75, 75])]
colors_hgh = [np.array([160, 255, 255])]

capture = cv2.VideoCapture(0)


while(True):
    ret, frame = capture.read()
    windowsize = (400, 300)
    frame = cv2.resize(frame, windowsize)
    show_frame = deepcopy(frame)
    d = 50
    center = [200, 150]
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    val = [None for _ in range(4)]
    dx = [1, 1, -1, -1]
    dy = [1, -1, -1, 1]
    for i in range(4):
        val[i] = hsv[center[0] + dy[i] * d, center[1] + dx[i] * d]
        cv2.circle(show_frame, (center[0] + dy[i] * d, center[1] + dx[i] * d), 15, (255, 255, 255), thickness=3, lineType=cv2.LINE_8, shift=0)
    print(val)
    '''
    ex_img = cv2.inRange(hsv,colors_low[0], colors_hgh[0])
    contours, hierarchy = cv2.findContours(ex_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    areas = np.array(list(map(cv2.contourArea,contours)))
    areas = np.sort(areas)
    for i in reversed(range(len(areas))):
        #max_idx = np.argmax(areas)
        max_area = areas[i]
        result = cv2.moments(contours[i])
        if max_area / (h*w) < 0.005:
            break
        if result["m00"] == 0 or result["m00"] == 0:
            continue
        x = int(result["m10"]/result["m00"])
        y = int(result["m01"]/result["m00"])
        print(x, y)
        cv2.circle(show_frame, (x, y), 15, circle[0], thickness=3, lineType=cv2.LINE_8, shift=0)
    '''
    cv2.imshow('title',show_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
exit()
#scramble = list(input().split(' '))

strt = time()

'''
scramble_arr = moves2num(scramble)
print('scramble:', num2moves(scramble_arr))
puzzle = scrm(puzzle, 0)
print('scrambled:', puzzle)
'''

que = deque([[deepcopy(puzzle), 0, [], 0], [deepcopy(puzzle_back), 0, [], 1]])

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