import csv
from collections import deque
from copy import deepcopy
from itertools import permutations

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

inf = 1000
cp = [inf for _ in range(fac[8] + 1)]
co = [inf for _ in range(3 ** 8 + 1)]

rot_cost = 3

max_num = 5
neary_solved = []

solved_co = [[0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 2, 1, 1, 2, 2, 1], [2, 1, 1, 2, 2, 1, 1, 2]]
for i in range(3):
    tmp = 0
    for j in range(8):
        tmp *= 3
        tmp += solved_co[i][j]
    co[tmp] = 0

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

'''
for i in range(3):
    solved = Cube()
    solved.Co = solved_co[i]
    que = deque([[solved, 0, [-10, -10]]])
    while que:
        status, num, l_mov = que.popleft()
        lst = [[0, -1], [1, -1], [2, -1], [3, -1], [0, -2], [1, -2], [0, -3], [1, -3], [2, -3], [3, -3]]
        for mov in lst:
            if mov[0] == l_mov[0]:
                continue
            n_status = status.move(mov)
            #if abs(mov[0] - l_mov[0]) == 2:
            #    n_cost = cost - abs(l_mov[1]) + max(abs(l_mov[1]), abs(mov[1]))
            #else:
            #    n_cost = cost + rot_cost + abs(mov[1])
            coidx = n_status.co2i()
            if co[coidx] <= num + 1:
                continue
            co[coidx] = num + 1
            que.append([n_status, num + 1, mov])
print('co done')

for i in range(24):
    solved = Cube()
    solved.Cp = solved_cp[i]
    cp[solved.cp2i()] = 0
    que = deque([[solved, 0, [-10, -10]]])
    while que:
        status, num, l_mov = que.popleft()
        lst = [[0, -1], [1, -1], [2, -1], [3, -1], [0, -2], [1, -2], [0, -3], [1, -3], [2, -3], [3, -3]]
        for mov in lst:
            if mov[0] == l_mov[0]:
                continue
            n_status = status.move(mov)
            
            #if abs(mov[0] - l_mov[0]) == 2:
            #    n_cost = cost - abs(l_mov[1]) + max(abs(l_mov[1]), abs(mov[1]))
            #else:
            #    n_cost = cost + rot_cost + abs(mov[1])
            
            cpidx = n_status.cp2i()
            if cp[cpidx] <= num + 1:
                continue
            cp[cpidx] = num + 1
            que.append([n_status, num + 1, mov])
print('cp done')

with open('co.csv', mode='x') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(co)
print('co written')

with open('cp.csv', mode='x') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(cp)
print('cp written')
'''

#にぶたん
def search(cp_num, co_num):
    l = 0
    r = len(neary_solved) - 1
    cnt = 0
    while True:
        cnt += 1
        pre_r = r
        pre_l = l
        c = (r + l) // 2
        if neary_solved[c][0] > cp_num * 10000 + co_num:
            r = c
        elif neary_solved[c][0] < cp_num * 10000 + co_num:
            l = c
        else:
            r = c
        if pre_r == r and pre_l == l:
            break
    for i in range(l, r + 1):
        if neary_solved[i][0] == cp_num * 10000 + co_num:
            return i
    return -1

neary_solved.sort()
for cp_s, co_s in zip(solved_cp, cp_co):
    puzzle = Cube()
    puzzle.Cp = cp_s
    puzzle.Co = co_s
    que = deque([[puzzle, 0, [], 0]])
    while que:
        status, num, moves, cost = que.popleft()
        lst = [[0, -1], [1, -1], [2, -1], [3, -1], [0, -2], [1, -2], [2, -3], [3, -3]]
        if moves == 0:
            lst = [[0, -1], [1, -1], [2, -1], [3, -1], [0, -2], [1, -2]]
        for mov in lst:
            if len(moves) and moves[-1][0] == mov[0]:
                continue
            if len(moves) >= 2 and abs(moves[-2][0] - moves[-1][0]) == 2 and mov[0] == moves[-2][0]:
                continue
            n_status = status.move(mov)
            if len(moves) and abs(mov[0] - moves[-1][0]) == 2:
                n_cost = cost - abs(moves[-1][1]) + max(abs(moves[-1][1]), abs(mov[1]))
            else:
                n_cost = cost + rot_cost + abs(mov[1])
            if num + 1 <= max_num:
                n_moves = [[j for j in i] for i in moves]
                n_moves.append(mov)
                cp_idx = n_status.cp2i()
                co_idx = n_status.co2i()
                tmp = search(cp_idx, co_idx)
                if tmp == -1:
                    neary_solved.append([cp_idx * 10000 + co_idx, list(reversed(n_moves)), n_cost])
                    neary_solved.sort()
                    que.append([n_status, num + 1, n_moves, n_cost])
                elif neary_solved[tmp][2] > n_cost:
                    neary_solved[tmp] = [cp_idx * 10000 + co_idx, list(reversed(n_moves)), n_cost]
                    que.append([n_status, num + 1, n_moves, n_cost])
print('neary solved done')

with open('solved.csv', mode='x') as f:
    writer = csv.writer(f, lineterminator='\n')
    for i, j in enumerate(neary_solved):
        row = [j[0]]
        row.append(i)
        writer.writerow(row)
    '''
    for i in range(2):
        row = []
        for j in neary_solved:
            row.append(j[i])
        writer.writerow(row)
    '''
with open('solved_solution.csv', mode='x') as f:
    writer = csv.writer(f, lineterminator='\n')
    for i in neary_solved:
        row = []
        for j in i[1]:
            row.extend(j)
        writer.writerow(row)
print('neary solved written')