# coding:utf-8
'''
Code for Soltvvo3.2
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

''' 色の情報からパズルの状態配列を作る '''
''' Create CO and CP arrays from the colors of stickers '''

def create_arr(colors):
    # すべての色が4つずつ現れているかチェック
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
    # パーツ1つずつCPとCOを埋めていく
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
    if tmp2:
        tmp2 = tmp2[0]
        for i in range(7):
            if cp[i] > tmp2:
                cp[i] -= 1
    return cp, co


''' その状態から解までの距離を返す '''
''' Returns the distance between the state and the solved state '''

def distance(cp_idx, co_idx):
    # CPだけ、COだけを揃えるときのそれぞれの最小コストの最大値を返す
    return max(cp_cost[cp_idx], co_cost[co_idx])


''' 遷移テーブルを使ってパズルの状態を変化させる '''
''' Change the state using transition tables '''

def move(cp_idx, co_idx, twist):
    return cp_trans[cp_idx][twist], co_trans[co_idx][twist]


''' 二分探索 '''
''' Binary search '''

def bin_search(num):
    # 二分探索でneary_solvedの中で目的のインデックスを探す
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


''' 深さ優先探索 '''
''' Depth-first search '''

def search(cp_idx, co_idx, depth, mode):
    global solution
    # 前回に回した手と直交する方向の回転を使う
    twist_idx_lst = [range(6, 12), range(6), range(12)]
    for twist in twist_idx_lst[mode]:
        # パズルを回転させる
        cost = cost_lst[twist]
        n_cp_idx, n_co_idx = move(cp_idx, co_idx, twist)
        # 残り深さを更新
        n_depth = depth - cost - grip_cost
        # 次の再帰に使う値を計算
        n_mode = twist // 6
        n_dis = distance(n_cp_idx, n_co_idx)
        if n_dis > n_depth:
            continue
        # グローバルの手順配列に要素を追加
        solution.append(twist)
        # 前計算した少ないコストで揃う状態のどれかになった場合
        if n_dis <= neary_solved_depth <= n_depth:
            tmp = bin_search(n_cp_idx * 2187 + n_co_idx)
            if tmp >= 0 and neary_solved_solution[tmp][0] // 6 != solution[-1] // 6:
                solution.extend(neary_solved_solution[tmp])
                return True, grip_cost + neary_solved_idx[tmp][1]
        # 次の深さの探索
        tmp, ans_cost = search(n_cp_idx, n_co_idx, n_depth, n_mode)
        if tmp:
            return True, ans_cost
        # 解が見つからなかったらグローバルの手順配列から要素をpop
        solution.pop()
    return False, -1


''' IDA*探索 '''
''' IDA* algorithm '''

def solver(colors):
    global solution
    # CPとCOのインデックスを求める
    cp, co = create_arr(colors)
    if cp == -1 or co == -1:
        return -1, -1
    cp_idx = cp2idx(cp)
    co_idx = co2idx(co)
    # 探索する前にもう答えがわかってしまう場合
    if distance(cp_idx, co_idx) <= neary_solved_depth:
        tmp = bin_search(cp_idx * 2187 + co_idx)
        if tmp >= 0:
            return [twist_lst[i] for i in neary_solved_solution[tmp]], neary_solved_idx[tmp][1]
    res_cost = 0
    # IDA*
    for depth in range(1, 34):
        solution = []
        tmp, cost = search(cp_idx, co_idx, depth, 2)
        if tmp:
            res_cost = depth + cost
            break
    if solution == []:
        return -1, res_cost
    return [twist_lst[i] for i in solution], res_cost


''' 配列の読み込み '''
''' Load arrays '''

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
        if line.replace('\n', '') == '':
            neary_solved_solution.append([])
        else:
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
num = 100
max_scramble_num = 100
time_lst = []
cnt = 0
for i in range(num):
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
    #print(i, solv_time, cost)
print('cnt', cnt)
print('time max, avg', max(time_lst), sum(time_lst) / num)
print('cost max, avg', max(cost_lst), sum(cost_lst) / num)
'''
'''
colors = [None for _ in range(6)]

# F' U2 R U' R2 U F2 U R'
colors[0] = ['', '', 'g', 'r', '', '', '', '']
colors[1] = ['', '', 'o', 'y', '', '', '', '']
colors[2] = ['y', 'g', 'w', 'r', 'g', 'b', 'w', 'o']
colors[3] = ['o', 'y', 'r', 'b', 'w', 'r', 'g', 'b']
colors[4] = ['', '', 'b', 'o', '', '', '', '']
colors[5] = ['', '', 'y', 'w', '', '', '', '']

# U' R F R F' U2 R' F2 R2
colors[0] = ['', '', 'g', 'o', '', '', '', '']
colors[1] = ['', '', 'r', 'y', '', '', '', '']
colors[2] = ['w', 'b', 'w', 'b', 'r', 'w', 'b', 'r']
colors[3] = ['o', 'y', 'g', 'w', 'g', 'o', 'g', 'b']
colors[4] = ['', '', 'r', 'o', '', '', '', '']
colors[5] = ['', '', 'y', 'y', '', '', '', '']

colors[0] = ['', '', 'w', 'g', '', '', '', '']
colors[1] = ['', '', 'b', 'y', '', '', '', '']
colors[2] = ['o', 'r', 'y', 'g', 'o', 'w', 'o', 'b']
colors[3] = ['o', 'w', 'b', 'r', 'y', 'r', 'g', 'b']
colors[4] = ['', '', 'r', 'g', '', '', '', '']
colors[5] = ['', '', 'y', 'w', '', '', '', '']

colors[0] = ['', '', 'w', 'w', '', '', '', '']
colors[1] = ['', '', 'w', 'w', '', '', '', '']
colors[2] = ['o', 'o', 'g', 'g', 'r', 'r', 'b', 'b']
colors[3] = ['o', 'o', 'g', 'g', 'r', 'r', 'b', 'b']
colors[4] = ['', '', 'y', 'y', '', '', '', '']
colors[5] = ['', '', 'y', 'y', '', '', '', '']

colors[0] = ['', '', 'w', 'o', '', '', '', '']
colors[1] = ['', '', 'w', 'g', '', '', '', '']
colors[2] = ['b', 'o', 'g', 'y', 'r', 'w', 'b', 'r']
colors[3] = ['o', 'o', 'g', 'g', 'w', 'r', 'b', 'b']
colors[4] = ['', '', 'y', 'r', '', '', '', '']
colors[5] = ['', '', 'y', 'y', '', '', '', '']

print(solver(colors))
'''