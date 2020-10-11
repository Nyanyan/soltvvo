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
    solved_cp_idx = [cp2idx(i) for i in solved_cp]
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
    solved_co_idx = list(set([co2idx(i) for i in solved_co]))
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
    cp_trans_rev = [[-1 for _ in range(12)] for _ in range(fac[8])]
    for idx in range(fac[8]):
        if idx % 1000 == 0:
            print(idx / fac[8])
        cp = idx2cp(idx)
        for i, twist in enumerate(twist_lst):
            twisted_cp = [j for j in cp]
            for each_twist in twist:
                lst = [0, -3, -2, -1]
                each_twist[1] = lst[-each_twist[1]]
                twisted_cp = move_cp(twisted_cp, each_twist)
            twisted_idx = cp2idx(twisted_cp)
            cp_trans_rev[idx][i] = twisted_idx
    with open('cp_trans_rev.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in cp_trans_rev:
            writer.writerow(line)
    print('cp trans rev done')

def create_co_trans_rev():
    co_trans_rev = [[-1 for _ in range(12)] for _ in range(3 ** 7)]
    for idx in range(3 ** 7):
        if idx % 1000 == 0:
            print(idx / 3 ** 7)
        co = idx2co(idx)
        for i, twist in enumerate(twist_lst):
            twisted_co = [j for j in co]
            for each_twist in twist:
                lst = [0, -3, -2, -1]
                each_twist[1] = lst[-each_twist[1]]
                twisted_co = move_co(twisted_co, each_twist)
            twisted_idx = co2idx(twisted_co)
            co_trans_rev[idx][i] = twisted_idx
    with open('co_trans_rev.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in co_trans_rev:
            writer.writerow(line)
    print('co trans rev done')

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
    solved_cp_idx = [cp2idx(i) for i in solved_cp]
    solved_co_idx = [co2idx(i) for i in solved_co]
    for i in range(24):
        twisted_idx = solved_cp_idx[i] * 2187 + solved_co_idx[i]
        neary_solved_idx.add(twisted_idx)
        neary_solved_cost_dic[twisted_idx] = 0
        neary_solved_idx_dic[twisted_idx] = len(neary_solved)
        neary_solved.append([twisted_idx, 0, []])
    que = deque([[solved_cp_idx[i], solved_co_idx[i], 0, [], 2] for i in range(24)])
    cnt = 0
    while que:
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt, len(que))
        cp_idx, co_idx, cost, move, mode = que.popleft()
        twists = [range(6, 12), range(6), range(12)]
        for twist in twists[mode]:
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

#create_cp_trans()
#create_co_trans()
create_cp_cost()
create_co_cost()
#create_cp_trans_rev()
#create_co_trans_rev()
#create_neary_solved()