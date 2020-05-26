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

from numpy import matrix, rot90
from copy import deepcopy
from collections import deque
from math import factorial
from time import time
import tkinter

def move(n_arr, num):
    idx = num // 3
    rot_arr1 = matrix([[n_arr[surface[idx][i]][0] for i in range(j * 2, j * 2 + 2)] for j in range(2)])
    rot_arr2 = matrix([[n_arr[surface[idx][i]][1] for i in range(j * 2, j * 2 + 2)] for j in range(2)])
    rot_arr1 = rot90(rot_arr1, 3 - num % 3).tolist()
    rot_arr2 = rot90(rot_arr2, 3 - num % 3).tolist()
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

def confirm_p():
    global colors
    for i in range(6):
        for j in range(8):
            if 1 < i < 4 or 1 < j < 4:
                tmp = entry[i][j].get()
                colors[i][j] = tmp
                entry[i][j]['bg'] = dic[tmp]

def start_p():
    strt = time()
    confirm_p()
    parts_place = [[[0, 2], [2, 0], [2, 7]], [[0, 3], [2, 6], [2, 5]], [[1, 2], [2, 2], [2, 1]], [[1, 3], [2, 4], [2, 3]], [[4, 2], [3, 1], [3, 2]], [[4, 3], [3, 3], [3, 4]], [[5, 3], [3, 5], [3, 6]]]
    parts_color = [set(['w', 'o', 'b']), set(['w', 'b', 'r']), set(['w', 'g', 'o']), set(['w', 'r', 'g']), set(['y', 'o', 'g']), set(['y', 'g', 'r']), set(['y', 'r', 'b'])]
    puzzle = [[i, 0] for i in range(7)]
    for i in range(7):
        tmp = []
        for j in range(3):
            tmp.append(colors[parts_place[i][j][0]][parts_place[i][j][1]])
        tmp1 = 'w' if 'w' in tmp else 'y'
        puzzle[i][1] = tmp.index(tmp1)
        tmp = set(tmp)
        puzzle[i][0] = parts_color.index(tmp)

    solved = [[i, 0] for i in range(7)]
    que = deque([[deepcopy(puzzle), 0, [], 0], [[[i, 0] for i in range(7)], 0, [], 1]])
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

#scramble = list(input().split(' '))
root = tkinter.Tk()
root.title("2x2x2solver")
root.geometry("400x300")
canvas = tkinter.Canvas(root, width = 400, height = 300)
canvas.place(x=0,y=0)

grid = 50

entry = [[None for _ in range(8)] for _ in range(6)]

dic = {'w':'white', 'g':'green', 'r':'red', 'b':'blue', 'o':'magenta', 'y':'yellow'}

for i in range(6):
    for j in range(8):
        if 1 < i < 4 or 1 < j < 4:
            canvas.create_rectangle(j * grid, i * grid, (j + 1) * grid, (i + 1) * grid, fill = 'gray')
            entry[i][j] = tkinter.Entry(width=2)
            entry[i][j].place(x = j * grid, y = i * grid)

confirm = tkinter.Button(canvas, text="confirm", command=confirm_p)
confirm.pack()

start = tkinter.Button(canvas, text="start", command=start_p)
start.pack()

root.mainloop()