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
        twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[1, -1]], [[1, -2]], [[3, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[2, -2], [0, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -2], [3, -1]]] #, [[2, -1], [0, -3]]
        cost_lst = [1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2]
        for twist, cost_pls in zip(twist_lst, cost_lst):
            twisted_cp = [i for i in cp]
            for each_twist in twist:
                twisted_cp = move_cp(twisted_cp, each_twist)
            twisted_idx = cp2idx(twisted_cp)
            n_cost = cost + cost_pls
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
        twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[1, -1]], [[1, -2]], [[3, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[2, -2], [0, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -2], [3, -1]]] #, [[2, -1], [0, -3]]
        cost_lst = [1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2]
        for twist, cost_pls in zip(twist_lst, cost_lst):
            twisted_co = [i for i in co]
            for each_twist in twist:
                twisted_co = move_co(twisted_co, each_twist)
            twisted_idx = co2idx(twisted_co)
            n_cost = cost + cost_pls
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
        twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[1, -1]], [[1, -2]], [[3, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[2, -2], [0, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -2], [3, -1]]] #, [[2, -1], [0, -3]]
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
        twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[1, -1]], [[1, -2]], [[3, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[2, -2], [0, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -2], [3, -1]]] #, [[2, -1], [0, -3]]
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

create_cp_cost()
create_co_cost()
#create_cp_trans()
#create_co_trans()