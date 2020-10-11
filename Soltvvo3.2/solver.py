# coding:utf-8
'''
Code for Soltvvo2
Written by Nyanyan
Copyright 2020 Nyanyan


cp[その位置にあるパーツの番号]
co[白または黄ステッカーの向き]
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

cp[part number]
co[direction of white or yellow sticker]
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

from basic_functions import *

# 色の情報からパズルの状態配列を作る
# Make CO and CP array from the colors of stickers
def create_arr(colors):
    for i in j2color:
        cnt = 0
        for j in colors:
            if i in j:
                cnt += j.count(i)
        if cnt != 4:
            return -1, -1
    cp = [-1 for _ in range(8)]
    co = [-1 for _ in range(8)]
    set_parts_color = [set(i) for i in parts_color]
    for i in range(8):
        tmp = []
        for j in range(3):
            tmp.append(colors[parts_place[i][j][0]][parts_place[i][j][1]])
        tmp1 = 'w' if 'w' in tmp else 'y'
        co[i] = tmp.index(tmp1)
        if not set(tmp) in set_parts_color:
            return -1, -1
        cp[i] = set_parts_color.index(set(tmp))
    tmp2 = list(set(range(7)) - set(cp))
    if len(tmp2):
        tmp2 = tmp2[0]
        for i in range(7):
            if cp[i] > tmp2:
                cp[i] -= 1
    return cp, co

def distance(cp_idx, co_idx):
    return max(cp_cost[cp_idx], co_cost[co_idx])

def move(cp_idx, co_idx, twist):
    return cp_trans[cp_idx][twist], co_trans[co_idx][twist]

def bin_search(num):
    l = 0
    r = len_neary_solved
    while r - l > 1:
        c = (l + r) // 2
        if neary_solved_idx[c][0] == num:
            return c
        elif neary_solved_idx[c][0] > num:
            r = c
        else:
            l = c
    if r == len_neary_solved:
        return -1
    if num == neary_solved_idx[l][0]:
        return l
    elif num == neary_solved_idx[r][0]:
        return r
    else:
        return -1

def search(cp_idx, co_idx, depth, mode, now_cost):
    global solution
    twist_idx_lst = [range(6, 12), range(6), range(12)]
    for twist in twist_idx_lst[mode]:
        cost = cost_lst[twist]
        n_cp_idx, n_co_idx = move(cp_idx, co_idx, twist)
        n_depth = depth - cost - grip_cost
        n_now_cost = now_cost + grip_cost + cost
        n_mode = twist // 6
        n_dis = distance(n_cp_idx, n_co_idx)
        if n_dis > n_depth:
            continue
        solution.append(twist)
        #print(n_dis, n_depth, solution, idx2cp(n_cp_idx))
        if n_dis == 0:
            return True, n_now_cost
        '''
        if n_dis <= 17:
            tmp = bin_search(n_cp_idx * 2187 + n_co_idx)
            if tmp >= 0:
                print(idx2cp(n_cp_idx))
                print(neary_solved_solution[tmp])
                solution.extend(neary_solved_solution[tmp])
                return True, now_cost + grip_cost + neary_solved_idx[tmp][1]
        '''
        tmp, ans_cost = search(n_cp_idx, n_co_idx, n_depth, n_mode, n_now_cost)
        if tmp:
            return True, ans_cost
        solution.pop()
    return False, -1

def solver(colors):
    global solution
    cp, co = create_arr(colors)
    if cp == -1 or co == -1:
        return -1, -1
    cp_idx = cp2idx(cp)
    co_idx = co2idx(co)
    print(cp_cost[cp_idx], co_cost[co_idx])
    print(distance(cp_idx, co_idx))
    if distance(cp_idx, co_idx) == 0:
        return solution, 0
    res = []
    res_cost = 0
    # IDA* Algorithm
    for depth in range(1, 30):
        tmp, cost = search(cp_idx, co_idx, depth, 2, 0)
        if tmp:
            res = solution
            res_cost = cost
            break
    '''
    # BDA* Algorithm
    l = 0
    r = 30
    while l < r:
        solution = []
        c = (l + r) // 2
        tmp, cost = search(cp_idx, co_idx, c, 2, 0)
        if tmp:
            res = [i for i in solution]
            res_cost = cost
            r = min(c, cost)
        else:
            l = c + 1
    '''
    if res == []:
        return -1, res_cost
    twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[0, -1], [2, -2]], [[1, -1]], [[1, -2]], [[3, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -1], [3, -2]]]
    return [twist_lst[i] for i in res], res_cost

with open('cp_cost.csv', mode='r') as f:
    cp_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('co_cost.csv', mode='r') as f:
    co_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]
cp_trans = []
with open('cp_trans.csv', mode='r') as f:
    for line in map(str.strip, f):
        cp_trans.append([int(i) for i in line.replace('\n', '').split(',')])
co_trans = []
with open('co_trans.csv', mode='r') as f:
    for line in map(str.strip, f):
        co_trans.append([int(i) for i in line.replace('\n', '').split(',')])
neary_solved_idx = []
with open('neary_solved_idx.csv', mode='r') as f:
    for line in map(str.strip, f):
        neary_solved_idx.append([int(i) for i in line.replace('\n', '').split(',')])
neary_solved_solution = []
with open('neary_solved_solution.csv', mode='r') as f:
    for line in map(str.strip, f):
        neary_solved_solution.append([int(i) for i in line.replace('\n', '').split(',')])

len_neary_solved = len(neary_solved_idx)

solution = []
solved_cp_idx = 0
solved_co_idx = 0

print('solver initialized')

'''
# TEST
from time import time
from random import randint
num = 1000
max_scramble_num = 100
twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[0, -1], [2, -2]], [[1, -1]], [[1, -2]], [[3, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -1], [3, -3]]]
time_lst = []
cost_lst = []
cnt = 0
for _ in range(num):
    scramble_cp = [0, 1, 2, 3, 4, 5, 6, 7]
    scramble_co = [0, 0, 0, 0, 0, 0, 0, 0]
    scramble_num = randint(1, max_scramble_num)
    scramble = [twist_lst[i] for i in [randint(0, 11) for _ in range(scramble_num)]]
    for twist in scramble:
        for each_twist in twist:
            scramble_cp = move_cp(scramble_cp, each_twist)
            scramble_co = move_co(scramble_co, each_twist)
    #print(scramble_cp, scramble_co)
    strt = time()
    tmp = solver(scramble_cp, scramble_co)
    if tmp != -1:
        cnt += 1
    cost = tmp[1]
    solv_time = time() - strt
    #print(solv_time)
    time_lst.append(solv_time)
    cost_lst.append(cost)
print('cnt', cnt)
print('time max, avg', max(time_lst), sum(time_lst) / num)
print('cost max, avg', max(cost_lst), sum(cost_lst) / num)
'''
colors = [None for _ in range(6)]
colors[0] = ['', '', 'w', 'g', '', '', '', '']
colors[1] = ['', '', 'o', 'o', '', '', '', '']
colors[2] = ['o', 'y', 'g', 'g', 'w', 'r', 'w', 'b']
colors[3] = ['o', 'b', 'y', 'y', 'g', 'r', 'w', 'b']
colors[4] = ['', '', 'r', 'r', '', '', '', '']
colors[5] = ['', '', 'y', 'b', '', '', '', '']
'''
colors[0] = ['', '', 'w', 'g', '', '', '', '']
colors[1] = ['', '', 'b', 'y', '', '', '', '']
colors[2] = ['o', 'r', 'y', 'g', 'o', 'w', 'o', 'b']
colors[3] = ['o', 'w', 'b', 'r', 'y', 'r', 'g', 'b']
colors[4] = ['', '', 'r', 'g', '', '', '', '']
colors[5] = ['', '', 'y', 'w', '', '', '', '']
'''
print(solver(colors))
