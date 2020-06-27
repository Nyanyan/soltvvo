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
'''
cp2i_lst = [[[0 for _ in range(8)] for _ in range(fac[8])] for _ in range(8)]
def func(arr, num):
    if len(arr) == 8:
        return
    for i in range(8):
        if i in arr:
            continue
        cnt = 0
        for j in arr:
            if j < i:
                cnt += 1
        #print(len(arr) - 1, num)
        cp2i_lst[len(arr)][num][i] = i - cnt
        n_arr = deepcopy(arr)
        n_arr.append(i)
        res = num + fac[7 - len(arr)] * (i - cnt)
        func(n_arr, res)
for i in range(8):
    cp2i_lst[0][0][i] = 7 - i
    func([], 0)
print(cp2i_lst[0][:100])
'''
change_direction1 = [[1, -1], [3, -3]] #6種類 横回転, 最後は2回回す
change_direction2 = [[0, -1], [2, -3]] #4種類 縦回転

inf = 1000
cp = [inf for _ in range(fac[8] + 1)]
co = [inf for _ in range(3 ** 8 + 1)]

rot_cost = 5

solved_co = [1, 2, 2, 1, 1, 2, 2, 1]
co[4264] = 0
'''
for i in range(3):
    tmp = 0
    for j in range(8):
        tmp *= 3
        tmp += solved_co[i][j]
    co[tmp] = 0
'''
solved = Cube()
solved_cp = []
#print_arr = []
cp_co = []
for i in range(6):
    for j in range(4):
        solved_cp.append(deepcopy(solved.Cp))
        #print_arr.append(deepcopy(solved.Co))
        cp_co.append(solved.co2i())
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
#print(solved_cp)
#print(print_arr)

solved = Cube()
solved.Co = solved_co
que = deque([[solved, 0, [-10, -10]]])
while que:
    status, cost, l_mov = que.popleft()
    lst = [[0, -1], [1, -1], [2, -1], [3, -1], [0, -2], [1, -2], [0, -3], [1, -3], [2, -3], [3, -3]]
    for mov in lst:
        if mov[0] == l_mov[0]:
            continue
        n_status = status.move(mov)
        if abs(mov[0] - l_mov[0]) == 2:
            n_cost = cost - abs(l_mov[1]) + max(abs(l_mov[1]), abs(mov[1]))
        else:
            n_cost = cost + rot_cost + abs(mov[1])
        coidx = n_status.co2i()
        if co[coidx] <= n_cost:
            continue
        co[coidx] = n_cost
        que.append([n_status, n_cost, mov])
print('co done')

for i in range(24):
    if cp_co[i] != 4264:
        continue
    solved = Cube()
    solved.Cp = solved_cp[i]
    cp[solved.cp2i()] = 0
    que = deque([[solved, 0, [-10, -10]]])
    while que:
        status, cost, l_mov = que.popleft()
        lst = [[0, -1], [0, -3], [1, -2], [2, -1], [2, -3]]
        for mov in lst:
            if mov[0] == l_mov[0]:
                continue
            n_status = status.move(mov)
            if abs(mov[0] - l_mov[0]) == 2:
                n_cost = cost - abs(l_mov[1]) + max(abs(l_mov[1]), abs(mov[1]))
            else:
                n_cost = cost + rot_cost + abs(mov[1])
            cpidx = n_status.cp2i()
            #print(n_cost)
            if cp[cpidx] <= n_cost:
                continue
            cp[cpidx] = n_cost
            que.append([n_status, n_cost, mov])
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

for idx, d in enumerate(direction_arr):
    set_parts_color = [set(i) for i in parts_color]
    solved_color = [['' for _ in range(8)] for _ in range(6)]
    solved_color[5][2] = parts_color[d // 3][d % 3]
    solved_color[3][7] = parts_color[d // 3][(d % 3 + 1) % 3]
    solved_color[3][0] = parts_color[d // 3][(d % 3 + 2) % 3]
    solved_color[2][2] = j2color[(j2color.index(solved_color[3][7]) // 2) * 2 - j2color.index(solved_color[3][7]) % 2 + 1]
    solved_color[3][4] = j2color[(j2color.index(solved_color[3][0]) // 2) * 2 - j2color.index(solved_color[3][0]) % 2 + 1]
    solved_color[0][2] = j2color[(j2color.index(solved_color[5][2]) // 2) * 2 - j2color.index(solved_color[5][2]) % 2 + 1]
    for i in range(6):
        for j in range(8):
            if (1 < i < 4 or 1 < j < 4) and solved_color[i][j] == '':
                if i % 2 and j % 2:
                    dx = [0, -1, -1]
                    dy = [-1, -1, 0]
                elif i % 2 and (not j % 2):
                    dx = [0, 1, 1]
                    dy = [-1, -1, 0]
                elif (not i % 2) and j % 2:
                    dx = [-1, -1, 0]
                    dy = [0, 1, 1]
                elif (not i % 2) and (not j % 2):
                    dx = [1, 1, 0]
                    dy = [0, 1, 1]
                #print(i, j, dx, dy)
                for k in range(3):
                    if solved_color[i + dy[k]][j + dx[k]] != '':
                        solved_color[i][j] = solved_color[i + dy[k]][j + dx[k]]
    solved = Cube()
    for i in range(7):
        tmp = []
        for j in range(3):
            tmp.append(solved_color[parts_place[i][j][0]][parts_place[i][j][1]])
        tmp1 = 'w' if 'w' in tmp else 'y'
        solved.Co[i] = tmp.index(tmp1)
        solved.Cp[i] = set_parts_color.index(set(tmp))
    tmp2 = list(set(range(7)) - set(solved.Cp))
    if len(tmp2):
        tmp2 = tmp2[0]
        for i in range(7):
            if solved.Cp[i] > tmp2:
                solved.Cp[i] -= 1
    print('solved:')
    for i in range(6):
        print(solved_color[i])
    print(solved.Cp)
    print(solved.Co)
    print(idx)

    # 枝刈り用のco配列とcp配列
    inf = 100
    cp = [inf for _ in range(fac[7])]
    cp_solved = Cube()
    cp_solved.Cp = solved.Cp
    cp[cp_solved.cp2i()] = 0
    que = deque([cp_solved])
    while len(que):
        status = que.popleft()
        num = len(status.Moves)
        l_mov = status.Moves[-1] if num else -1
        t = (l_mov // 3) * 3
        lst = set(range(9)) - set([t, t + 1, t + 2])
        for mov in lst:
            n_status = status.move_cp(mov)
            n_idx = n_status.cp2i()
            if cp[n_idx] == inf:
                cp[n_idx] = len(n_status.Moves) #n_status.Movnum
                que.append(n_status)
    co = [inf for _ in range(3 ** 7)]
    co_solved = Cube()
    co_solved.Co = solved.Co
    co[co_solved.co2i()] = 0
    que = deque([co_solved])
    while len(que):
        status = que.popleft()
        num = len(status.Moves)
        l_mov = status.Moves[-1] if num else -1
        t = (l_mov // 3) * 3
        lst = set(range(9)) - set([t, t + 1, t + 2])
        for mov in lst:
            n_status = status.move_co(mov)
            n_idx = n_status.co2i()
            if co[n_idx] == inf:
                co[n_idx] = len(n_status.Moves) #n_status.Movnum
                que.append(n_status)
    
    with open('cp' + str(idx) + '.csv', mode='x') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(cp)
    with open('co' + str(idx) + '.csv', mode='x') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(co)
'''