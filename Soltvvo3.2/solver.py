from basic_functions import *

def distance(cp_idx, co_idx):
    return max(cp_cost[cp_idx], co_cost[co_idx])

def move(cp_idx, co_idx, twist):
    return cp_trans[cp_idx][twist], co_trans[co_idx][twist]

def search(cp_idx, co_idx, depth, mode):
    global solution
    if depth <= 0:
        return distance(cp_idx, co_idx) == 0
    print(' ' * depth, distance(cp_idx, co_idx))
    if mode == -1:
        twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[2, -2], [0, -1]], [[1, -1]], [[1, -2]], [[3, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -2], [3, -1]]]
    elif mode == 0:
        twist_lst = [[[1, -1]], [[1, -2]], [[3, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -2], [3, -1]]]
    elif mode == 1:
        twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[2, -2], [0, -1]]]
    n_mode = int(not mode) if mode != -1 else -1
    cost_lst = [1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2]
    dis = distance(cp_idx, co_idx)
    if dis <= depth:
        for twist, cost in enumerate(cost_lst):
            n_cp_idx, n_co_idx = move(cp_idx, co_idx, twist)
            n_depth = depth - cost - grip_cost
            solution.append(twist_lst[twist])
            if mode == -1:
                n_mode = twist // 6
            if distance(n_cp_idx, n_co_idx) > dis:
                continue
            if search(n_cp_idx, n_co_idx, n_depth, n_mode):
                return True
            solution.pop()
    return False

def solver(cp, co):
    global solution
    cp_idx = cp2idx(cp)
    co_idx = co2idx(co)
    if distance(cp_idx, co_idx) == 0:
        return solution, depth
    l = 0
    r = 34
    while l < r:
        solution = []
        c = (l + r) // 2
        print(c)
        if search(cp_idx, co_idx, c, -1):
            r = c
        else:
            l = c + 1
    if solution == []:
        return -1, l
    return solution, l

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

solution = []
solved_cp_idx = 0
solved_co_idx = 0

scramble_cp = [0, 1, 2, 3, 4, 5, 6, 7]
scramble_co = [0, 0, 0, 0, 0, 0, 0, 0]
scramble = [[[0, -1]], [[1, -2]], [[0, -1], [2, -1]]] #, [[1, -2], [3, -1]], [[0, -1]], [[1, -2]], [[0, -1], [2, -1]], [[1, -2], [3, -1]], [[0, -1]], [[1, -2]], [[0, -1], [2, -1]], [[1, -2], [3, -1]]]
for twist in scramble:
    for each_twist in twist:
        scramble_cp = move_cp(scramble_cp, each_twist)
        scramble_co = move_co(scramble_co, each_twist)

grip_cost = 1

print(scramble_cp, scramble_co)

print(solver(scramble_cp, scramble_co))