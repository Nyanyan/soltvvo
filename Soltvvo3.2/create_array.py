# coding:utf-8
from collections import deque
import csv

from basic_functions import *

def create_cp_cost():
    cp_cost = [1000 for _ in range(fac[8])]
    solved_cp = [0, 1, 2, 3, 4, 5, 6, 7]
    que = deque([[solved_cp, 0]])
    cp_cost[cp2idx(solved_cp)] = 0
    while que:
        cp, cost = que.popleft()
        twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[0, -1], [2, -2]], [[1, -1]], [[1, -2]], [[3, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -1], [3, -3]]]
        cost_lst = [1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2]
        for twist, cost_pls in zip(twist_lst, cost_lst):
            twisted_cp = [i for i in cp]
            for each_twist in twist:
                twisted_cp = move_cp(twisted_cp, each_twist)
            twisted_idx = cp2idx(twisted_cp)
            n_cost = cost + grip_cost + cost_pls
            if cp_cost[twisted_idx] > n_cost:
                cp_cost[twisted_idx] = n_cost
                que.append([twisted_cp, n_cost])

    with open('cp_cost.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(cp_cost)
    print('cp cost done')

def create_co_cost():
    co_cost = [1000 for _ in range(3 ** 7)]
    solved_co = [0, 0, 0, 0, 0, 0, 0, 0]
    que = deque([[solved_co, 0]])
    co_cost[co2idx(solved_co)] = 0
    while que:
        co, cost = que.popleft()
        twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[0, -1], [2, -2]], [[1, -1]], [[1, -2]], [[3, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -1], [3, -3]]]
        cost_lst = [1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2]
        for twist, cost_pls in zip(twist_lst, cost_lst):
            twisted_co = [i for i in co]
            for each_twist in twist:
                twisted_co = move_co(twisted_co, each_twist)
            twisted_idx = co2idx(twisted_co)
            n_cost = cost + grip_cost + cost_pls
            if co_cost[twisted_idx] > n_cost:
                co_cost[twisted_idx] = n_cost
                que.append([twisted_co, n_cost])

    with open('co_cost.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(co_cost)
    print('co cost done')

def create_cp_trans():
    cp_trans = [[-1 for _ in range(12)] for _ in range(fac[8])]
    for idx in range(fac[8]):
        cp = idx2cp(idx)
        twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[0, -1], [2, -2]], [[1, -1]], [[1, -2]], [[3, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -1], [3, -3]]]
        for i, twist in enumerate(twist_lst):
            twisted_cp = [i for i in cp]
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
        co = idx2co(idx)
        twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[0, -1], [2, -2]], [[1, -1]], [[1, -2]], [[3, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -1], [3, -3]]]
        for i, twist in enumerate(twist_lst):
            twisted_co = [i for i in co]
            for each_twist in twist:
                twisted_co = move_co(twisted_co, each_twist)
            twisted_idx = co2idx(twisted_co)
            co_trans[idx][i] = twisted_idx

    with open('co_trans.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in co_trans:
            writer.writerow(line)
    print('co trans done')

def create_neary_solved():
    neary_solved_depth = 15
    cp_trans = []
    with open('cp_trans.csv', mode='r') as f:
        for line in map(str.strip, f):
            cp_trans.append([int(i) for i in line.replace('\n', '').split(',')])
    co_trans = []
    with open('co_trans.csv', mode='r') as f:
        for line in map(str.strip, f):
            co_trans.append([int(i) for i in line.replace('\n', '').split(',')])
    neary_solved = []
    neary_solved_idx = set()
    solved_cp_idx = 0
    solved_co_idx = 0
    que = deque([[solved_cp_idx, solved_co_idx, 0, [], -1]])
    while que:
        cp_idx, co_idx, cost, move, mode = que.popleft()
        if mode == -1:
            twist_lst = range(12)
        elif mode == 0:
            twist_lst = range(6, 12)
        elif mode == 1:
            twist_lst = range(6)
        #twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[0, -1], [2, -2]], [[1, -1]], [[1, -2]], [[3, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -1], [3, -3]]]
        cost_lst = [1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2]
        for twist in twist_lst:
            cost_pls = cost_lst[twist]
            twisted_cp_idx = cp_trans[cp_idx][twist]
            twisted_co_idx = co_trans[co_idx][twist]
            twisted_idx = twisted_cp_idx * 2187 + twisted_co_idx
            n_cost = cost + grip_cost + cost_pls
            n_mode = twist // 6
            n_move = [i for i in move]
            n_move.append(twist)
            if neary_solved_depth + 3 >= n_cost >= neary_solved_depth and not twisted_idx in neary_solved_idx:
                neary_solved_idx.add(twisted_idx)
                neary_solved.append([twisted_idx, n_cost, n_move])
            elif n_cost < neary_solved_depth:
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

#create_cp_cost()
#create_co_cost()
#create_cp_trans()
#create_co_trans()
#create_neary_solved()