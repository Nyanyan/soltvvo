# coding:utf-8
from collections import deque
import csv

from basic_functions import *

def create_cp_trans():
    cp_trans = [[-1 for _ in range(12)] for _ in range(fac[8])]
    for idx in range(fac[8]):
        if idx % 1000 == 0:
            print(idx / fac[8])
        cp = idx2cp(idx)
        for i, twist in enumerate(twist_lst):
            twisted_cp = [j for j in cp]
            for each_twist in twist:
                twisted_cp = move_cp(twisted_cp, each_twist)
            twisted_idx = cp2idx(twisted_cp)
            cp_trans[idx][i] = twisted_idx
    with open('cp_trans.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in cp_trans:
            writer.writerow(line)
    print('cp trans done')

def create_co_trans():
    co_trans = [[-1 for _ in range(12)] for _ in range(3 ** 7)]
    for idx in range(3 ** 7):
        if idx % 1000 == 0:
            print(idx / 3 ** 7)
        co = idx2co(idx)
        for i, twist in enumerate(twist_lst):
            twisted_co = [j for j in co]
            for each_twist in twist:
                twisted_co = move_co(twisted_co, each_twist)
            twisted_idx = co2idx(twisted_co)
            co_trans[idx][i] = twisted_idx
    with open('co_trans.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in co_trans:
            writer.writerow(line)
    print('co trans done')

def create_cp_cost():
    cp_trans = []
    with open('cp_trans.csv', mode='r') as f:
        for line in map(str.strip, f):
            cp_trans.append([int(i) for i in line.replace('\n', '').split(',')])
    cp_cost = [1000 for _ in range(fac[8])]
    solved_cp_idx = [0, 11824, 23616, 34560, 9680, 18290, 12316, 3706, 40319, 28495, 16703, 5759, 30639, 22029, 28003, 36613, 10210, 16313, 30109, 24006, 33826, 39049, 6493, 1270]
    que = deque([[i, 0] for i in solved_cp_idx])
    for i in solved_cp_idx:
        cp_cost[i] = 0
    cnt = 0
    while que:
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt, len(que))
        cp, cost = que.popleft()
        twists = range(12)
        for twist, cost_pls in zip(twists, cost_lst):
            twisted_idx = cp_trans[cp][twist]
            n_cost = cost + grip_cost + cost_pls
            if cp_cost[twisted_idx] > n_cost:
                cp_cost[twisted_idx] = n_cost
                que.append([twisted_idx, n_cost])
    with open('cp_cost.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(cp_cost)
    print('cp cost done')

def create_co_cost():
    co_trans = []
    with open('co_trans.csv', mode='r') as f:
        for line in map(str.strip, f):
            co_trans.append([int(i) for i in line.replace('\n', '').split(',')])
    co_cost = [1000 for _ in range(3 ** 7)]
    solved_co_idx = [0, 1858, 1421]
    que = deque([[i, 0] for i in solved_co_idx])
    for i in solved_co_idx:
        co_cost[i] = 0
    cnt = 0
    while que:
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt, len(que))
        co, cost = que.popleft()
        twists = range(12)
        for twist, cost_pls in zip(twists, cost_lst):
            twisted_idx = co_trans[co][twist]
            n_cost = cost + grip_cost + cost_pls
            if co_cost[twisted_idx] > n_cost:
                co_cost[twisted_idx] = n_cost
                que.append([twisted_idx, n_cost])
    with open('co_cost.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(co_cost)
    print('co cost done')

def create_cp_trans_rev():
    cp_trans = [[-1 for _ in range(12)] for _ in range(fac[8])]
    for idx in range(fac[8]):
        if idx % 1000 == 0:
            print(idx / fac[8])
        if idx % 1000 == 0:
            print(idx / fac[8])
        cp = idx2cp(idx)
        twist_lst_rev = [[[0, 1]], [[0, 2]], [[2, 1]], [[0, 1], [2, 1]], [[0, 2], [2, 1]], [[0, 1], [2, 2]], [[1, 1]], [[1, 2]], [[3, 1]], [[1, 1], [3, 1]], [[1, 2], [3, 1]], [[1, 1], [3, 2]]]
        for i, twist in enumerate(twist_lst_rev):
            twisted_cp = [j for j in cp]
            for each_twist in twist:
                twisted_cp = move_cp(twisted_cp, each_twist)
            twisted_idx = cp2idx(twisted_cp)
            cp_trans[twisted_idx][i] = idx
    with open('cp_trans_rev.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in cp_trans:
            writer.writerow(line)
    print('cp trans done')

def create_co_trans_rev():
    co_trans = [[-1 for _ in range(12)] for _ in range(3 ** 7)]
    for idx in range(3 ** 7):
        if idx % 1000 == 0:
            print(idx / 3 ** 7)
        co = idx2co(idx)
        twist_lst_rev = [[[0, 1]], [[0, 2]], [[2, 1]], [[0, 1], [2, 1]], [[0, 2], [2, 1]], [[0, 1], [2, 2]], [[1, 1]], [[1, 2]], [[3, 1]], [[1, 1], [3, 1]], [[1, 2], [3, 1]], [[1, 1], [3, 2]]]
        for i, twist in enumerate(twist_lst_rev):
            twisted_co = [j for j in co]
            for each_twist in twist:
                twisted_co = move_co(twisted_co, each_twist)
            twisted_idx = co2idx(twisted_co)
            co_trans[twisted_idx][i] = idx
    with open('co_trans_rev.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in co_trans:
            writer.writerow(line)
    print('co trans done')

def create_neary_solved():
    neary_solved_depth = 15
    cp_trans_rev = []
    with open('cp_trans_rev.csv', mode='r') as f:
        for line in map(str.strip, f):
            cp_trans_rev.append([int(i) for i in line.replace('\n', '').split(',')])
    co_trans_rev = []
    with open('co_trans_rev.csv', mode='r') as f:
        for line in map(str.strip, f):
            co_trans_rev.append([int(i) for i in line.replace('\n', '').split(',')])
    neary_solved = []
    neary_solved_idx = set()
    neary_solved_cost_dic = {}
    neary_solved_idx_dic = {}
    #solved_cp = [[0, 1, 2, 3, 4, 5, 6, 7], [2, 3, 4, 5, 6, 7, 0, 1], [4, 5, 6, 7, 0, 1, 2, 3], [6, 7, 0, 1, 2, 3, 4, 5], [1, 7, 3, 5, 2, 4, 0, 6], [3, 5, 2, 4, 0, 6, 1, 7], [2, 4, 0, 6, 1, 7, 3, 5], [0, 6, 1, 7, 3, 5, 2, 4], [7, 6, 5, 4, 3, 2, 1, 0], [5, 4, 3, 2, 1, 0, 7, 6], [3, 2, 1, 0, 7, 6, 5, 4], [1, 0, 7, 6, 5, 4, 3, 2], [6, 0, 4, 2, 5, 3, 7, 1], [4, 2, 5, 3, 7, 1, 6, 0], [5, 3, 7, 1, 6, 0, 4, 2], [7, 1, 6, 0, 4, 2, 5, 3], [2, 0, 3, 1, 5, 7, 4, 6], [3, 1, 5, 7, 4, 6, 2, 0], [5, 7, 4, 6, 2, 0, 3, 1], [4, 6, 2, 0, 3, 1, 5, 7], [6, 4, 7, 5, 1, 3, 0, 2], [7, 5, 1, 3, 0, 2, 6, 4], [1, 3, 0, 2, 6, 4, 7, 5], [0, 2, 6, 4, 7, 5, 1, 3]]
    #solved_co = [[0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [1, 2, 2, 1, 1, 2, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [1, 2, 2, 1, 1, 2, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2]]
    solved_cp_idx = [0, 11824, 23616, 34560, 9680, 18290, 12316, 3706, 40319, 28495, 16703, 5759, 30639, 22029, 28003, 36613, 10210, 16313, 30109, 24006, 33826, 39049, 6493, 1270]
    solved_co_idx = [0, 1858, 0, 1858, 1421, 1421, 1421, 1421, 0, 1858, 0, 1858, 1421, 1421, 1421, 1421, 0, 1858, 0, 1858, 0, 1858, 0, 1858]
    que = deque([[solved_cp_idx[i], solved_co_idx[i], 0, [], -1] for i in range(24)])
    cnt = 0
    while que:
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt, len(que))
        cp_idx, co_idx, cost, move, mode = que.popleft()
        if mode == -1:
            twists = range(12)
        elif mode == 0:
            twists = range(6, 12)
        elif mode == 1:
            twists = range(6)
        for twist in twists:
            cost_pls = cost_lst[twist]
            twisted_cp_idx = cp_trans_rev[cp_idx][twist]
            twisted_co_idx = co_trans_rev[co_idx][twist]
            twisted_idx = twisted_cp_idx * 2187 + twisted_co_idx
            n_cost = cost + grip_cost + cost_pls
            n_mode = twist // 6
            n_move = [i for i in move]
            n_move.append(twist)
            if neary_solved_depth >= n_cost and not twisted_idx in neary_solved_idx:
                neary_solved_idx.add(twisted_idx)
                neary_solved_cost_dic[twisted_idx] = n_cost
                neary_solved_idx_dic[twisted_idx] = len(neary_solved)
                neary_solved.append([twisted_idx, n_cost, list(reversed(n_move))])
                que.append([twisted_cp_idx, twisted_co_idx, n_cost, n_move, n_mode])
            elif neary_solved_depth >= n_cost and neary_solved_cost_dic[twisted_idx] > n_cost:
                neary_solved_cost_dic[twisted_idx] = n_cost
                neary_solved[neary_solved_idx_dic[twisted_idx]] = [twisted_idx, n_cost, list(reversed(n_move))]
                que.append([twisted_cp_idx, twisted_co_idx, n_cost, n_move, n_mode])
    neary_solved.sort()
    with open('neary_solved_idx.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in [i[:2] for i in neary_solved]:
            writer.writerow(line)
    with open('neary_solved_solution.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in [i[2] for i in neary_solved]:
            writer.writerow(line)
    print('neary solved done')

create_cp_trans()
create_co_trans()
create_cp_cost()
create_co_cost()
create_co_trans_rev()
create_cp_trans_rev()
create_neary_solved()