'''
Code for Soltvvo2
Written by Nyanyan
Copyright 2020 Nyanyan
'''
import csv
from collections import deque
from copy import deepcopy
from itertools import permutations
from time import time
class Cube:
    def __init__(self):
        self.Co = [0, 0, 0, 0, 0, 0, 0, 0]
        self.Cp = [0, 1, 2, 3, 4, 5, 6, 7]

    # 回転処理 CP
    def move_cp(self, arr):
        surface = [[3, 1, 5, 7], [1, 0, 7, 6], [0, 2, 6, 4], [2, 3, 4, 5]]
        replace = [[2, 0, 3, 1], [3, 2, 1, 0], [1, 3, 0, 2]]
        res = [i for i in self.Cp]
        for i, j in zip(surface[arr[0]], replace[-arr[1] - 1]):
            res[i] = self.Cp[surface[arr[0]][j]]
        return res

    # 回転処理 CO
    def move_co(self, arr):
        surface = [[3, 1, 5, 7], [1, 0, 7, 6], [0, 2, 6, 4], [2, 3, 4, 5]]
        replace = [[2, 0, 3, 1], [3, 2, 1, 0], [1, 3, 0, 2]]
        pls = [2, 1, 1, 2]
        res = [i for i in self.Co]
        for i, j in zip(surface[arr[0]], replace[-arr[1] - 1]):
            res[i] = self.Co[surface[arr[0]][j]]
        if arr[1] != -2:
            for i in range(4):
                res[surface[arr[0]][i]] += pls[i]
                res[surface[arr[0]][i]] %= 3
        return res

    # 回転番号に則って実際にパズルの状態配列を変化させる
    def move(self, arr):
        res = Cube()
        res.Co = self.move_co(arr)
        res.Cp = self.move_cp(arr)
        return res

    # cp配列から固有の番号を作成
    def cp2i(self):
        res = 0
        for i in range(8):
            cnt = 0
            for j in self.Cp[:i]:
                if j < self.Cp[i]:
                    cnt += 1
            res += fac[7 - i] * (self.Cp[i] - cnt)
        return res
    
    # co配列から固有の番号を作成
    def co2i(self):
        res = 0
        for i in self.Co:
            res *= 3
            res += i
        return res

fac = [1]
for i in range(1, 9):
    fac.append(fac[-1] * i)

change_direction1 = [[1, -1], [3, -3]] #6種類 横回転, 最後は2回回す
change_direction2 = [[0, -1], [2, -3]] #4種類 縦回転

inf = 100
cp = [inf for _ in range(fac[8] + 1)]
co = [inf for _ in range(3 ** 8 + 1)]
cp_cost = [inf for _ in range(fac[8] + 1)]
co_cost = [inf for _ in range(3 ** 8 + 1)]

change_cost = 2
def calc_cost(arr):
    res = 0
    for j in range(len(arr)):
        if j > 0 and abs(arr[j - 1][0] - arr[j][0]) == 2:
            res -= abs(arr[j - 1][1])
            res += max(abs(arr[j - 1][1]), abs(arr[j][1]))
        elif j == 0:
            res += abs(arr[j][1])
        else:
            res += change_cost + abs(arr[j][1])
    return res

max_num = 5
neary_solved = []

solved_co = [[0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 2, 1, 1, 2, 2, 1], [2, 1, 1, 2, 2, 1, 1, 2]]

solved = Cube()
solved_cp = []
cp_co = []
for i in range(6):
    for j in range(4):
        solved_cp.append(deepcopy(solved.Cp))
        cp_co.append(deepcopy(solved.Co))
        neary_solved.append([solved.cp2i() * 10000 + solved.co2i(), [], 0])
        for k in change_direction2:
            solved = solved.move(k)
    if i < 3:
        for k in change_direction1:
            solved = solved.move(k)
    elif i == 3:
        for k in change_direction2:
            solved = solved.move(k)
        for k in change_direction1:
            solved = solved.move(k)
    elif i == 4:
        for j in range(2):
            for k in change_direction1:
                solved = solved.move(k)

for i in range(3):
    solved = Cube()
    solved.Co = solved_co[i]
    coidx = solved.co2i()
    co[coidx] = 0
    co_cost[coidx] = 0
    que = deque([[solved, 0, [-10, -10], 0]])
    while que:
        status, num, l_mov, cost = que.popleft()
        lst_all = [[[[0, -1]], [[0, -2]]], [[[1, -1]], [[1, -2]]], [[[2, -1]]], [[[3, -1]]]]
        lst_addition = [[[1, -1], [3, -1]], [[1, -2], [3, -1]], [[3, -2], [1, -1]], [[3, -3], [1, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[2, -2], [0, -1]], [[2, -1], [0, -3]]]
        lst = []
        for i in range(4):
            if i == l_mov[0] or abs(l_mov[0] - i) == 2:
                continue
            lst.extend(lst_all[i])
        if l_mov[0] == -10:
            lst.extend(lst_addition)
        else:
            l_mov_s = (l_mov[0] % 2) * 4
            for i in range(4):
                lst.append(lst_addition[i + l_mov_s])
        for movs in lst:
            n_status = Cube()
            n_status.Cp = [i for i in status.Cp]
            n_status.Co = [i for i in status.Co]
            max_rot_cost = 0
            for mov in movs:
                max_rot_cost = max(max_rot_cost, abs(mov[1]))
                n_status = n_status.move(mov)
            n_cost = cost + change_cost + max_rot_cost
            coidx = n_status.co2i()
            if co[coidx] <= num + 1 or co_cost[coidx] <= n_cost:
                continue
            co[coidx] = num + 1
            co_cost[coidx] = n_cost
            que.append([n_status, num + 1, mov, n_cost])
print('co done')

for i in range(24):
    solved = Cube()
    solved.Cp = solved_cp[i]
    cpidx = solved.cp2i()
    cp[cpidx] = 0
    cp_cost[cpidx] = 0
    que = deque([[solved, 0, [-10, -10], 0]])
    while que:
        status, num, l_mov, cost = que.popleft()
        lst_all = [[[[0, -1]], [[0, -2]]], [[[1, -1]], [[1, -2]]], [[[2, -1]]], [[[3, -1]]]]
        lst_addition = [[[1, -1], [3, -1]], [[1, -2], [3, -1]], [[3, -2], [1, -1]], [[3, -3], [1, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[2, -2], [0, -1]], [[2, -1], [0, -3]]]
        lst = []
        for i in range(4):
            if i == l_mov[0] or abs(l_mov[0] - i) == 2:
                continue
            lst.extend(lst_all[i])
        if l_mov[0] == -10:
            lst.extend(lst_addition)
        else:
            l_mov_s = (l_mov[0] % 2) * 4
            for i in range(4):
                lst.append(lst_addition[i + l_mov_s])
        for movs in lst:
            n_status = Cube()
            n_status.Cp = [i for i in status.Cp]
            n_status.Co = [i for i in status.Co]
            max_rot_cost = 0
            for mov in movs:
                max_rot_cost = max(max_rot_cost, abs(mov[1]))
                n_status = n_status.move(mov)
            n_cost = cost + change_cost + max_rot_cost
            cpidx = n_status.cp2i()
            if cp[cpidx] <= num + 1 or cp_cost[cpidx] <= n_cost:
                continue
            cp[cpidx] = num + 1
            cp_cost[cpidx] = n_cost
            que.append([n_status, num + 1, mov, n_cost])
print('cp done')

with open('co.csv', mode='x') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(co)

with open('co_cost.csv', mode='x') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(co_cost)

with open('cp.csv', mode='x') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(cp)

with open('cp_cost.csv', mode='x') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(cp_cost)
print('co cp written')

#にぶたん
def search(cp_num, co_num):
    l = 0
    r = len(neary_solved) - 1
    cocp = cp_num * 10000 + co_num
    cnt = 0
    while True:
        cnt += 1
        pre_r = r
        pre_l = l
        c = (r + l) // 2
        if neary_solved[c][0] > cocp:
            r = c
        elif neary_solved[c][0] < cocp:
            l = c
        else:
            r = c
        if pre_r == r and pre_l == l:
            break
    return_value = 0
    for i in range(l, r + 1):
        if neary_solved[i][0] == cocp:
            return [True, i]
        elif neary_solved[i][0] < cocp:
            return_value = i
    return [False, return_value + 1]

neary_solved.sort()
for cp_s, co_s in zip(solved_cp, cp_co):
    strt = time()
    puzzle = Cube()
    puzzle.Cp = cp_s
    puzzle.Co = co_s
    que = deque([[puzzle, 0, [], 0]])
    while que:
        status, num, moves, cost = que.popleft()
        if num == max_num:
            continue
        #lst = [[0, -1], [1, -1], [2, -1], [3, -1], [0, -2], [1, -2], [0, -3], [1, -3], [2, -3], [3, -3]]
        lst_all = [[[[0, -1]], [[0, -2]]], [[[1, -1]], [[1, -2]]], [[[2, -1]]], [[[3, -1]]]]
        lst_addition = [[[1, -1], [3, -1]], [[1, -2], [3, -1]], [[3, -2], [1, -1]], [[3, -3], [1, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[2, -2], [0, -1]], [[2, -1], [0, -3]]]
        lst = []
        l_mov = [-10, -10] if len(moves) == 0 else [i for i in moves[-1]]
        for i in range(4):
            if i == l_mov[0] or abs(l_mov[0] - i) == 2:
                continue
            lst.extend(lst_all[i])
        if l_mov[0] == -10:
            lst.extend(lst_addition)
        else:
            l_mov_s = (l_mov[0] % 2) * 4
            for i in range(4):
                lst.append(lst_addition[i + l_mov_s])
        for movs in lst:
            n_status = Cube()
            n_status.Cp = [i for i in status.Cp]
            n_status.Co = [i for i in status.Co]
            max_rot_cost = 0
            for mov in movs:
                max_rot_cost = max(max_rot_cost, abs(mov[1]))
                n_status = n_status.move(mov)
            cost_pls = change_cost + max_rot_cost
            n_moves = [[j for j in i] for i in moves]
            n_moves.extend(movs)
            ans = list(reversed([[j for j in i] for i in n_moves]))
            n_cost = cost + cost_pls
            cp_idx = n_status.cp2i()
            co_idx = n_status.co2i()
            tmp = search(cp_idx, co_idx)
            if tmp[0] == False:
                neary_solved.insert(tmp[1], [cp_idx * 10000 + co_idx, ans, n_cost])
                que.append([n_status, num + 1, n_moves, n_cost])
            elif neary_solved[tmp[1]][2] > n_cost:
                neary_solved[tmp[1]] = [cp_idx * 10000 + co_idx, ans, n_cost]
                que.append([n_status, num + 1, n_moves, n_cost])
    print(len(neary_solved), time() - strt)
print('neary solved done')

with open('solved.csv', mode='x') as f:
    writer = csv.writer(f, lineterminator='\n')
    for i, j in enumerate(neary_solved):
        row = [j[0]]
        row.append(i)
        writer.writerow(row)
with open('solved_solution.csv', mode='x') as f:
    writer = csv.writer(f, lineterminator='\n')
    for i in neary_solved:
        row = []
        for j in i[1]:
            row.extend(j)
        writer.writerow(row)
print('neary solved written')