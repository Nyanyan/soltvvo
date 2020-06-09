import csv
from collections import deque

class Cube:
    def __init__(self):
        self.Co = [0, 0, 0, 0, 0, 0, 0]
        self.Cp = [0, 1, 2, 3, 4, 5, 6]
        self.Moves = []
        self.Movnum = 0

    # 回転処理 CP
    def move_cp(self, num):
        surface = [[0, 1, 2, 3], [2, 3, 4, 5], [3, 1, 5, 6]]
        replace = [[2, 0, 3, 1], [3, 2, 1, 0], [1, 3, 0, 2]]
        idx = num // 3
        res = Cube()
        res.Cp = [i for i in self.Cp]
        for i, j in zip(surface[idx], replace[num % 3]):
            res.Cp[i] = self.Cp[surface[idx][j]]
        res.Moves = [i for i in self.Moves]
        res.Moves.append(num)
        res.Movnum = self.Movnum + 1
        res.Movnum += 1 if len(self.Moves) >= 2 and num // 3 != self.Moves[-1] // 3 and num // 3 != self.Moves[-2] // 3 else 0
        res.Movnum += 1 if len(self.Moves) < 2 and num // 3 == 1 else 0
        return res

    # 回転処理 CO
    def move_co(self, num):
        surface = [[0, 1, 2, 3], [2, 3, 4, 5], [3, 1, 5, 6]]
        replace = [[2, 0, 3, 1], [3, 2, 1, 0], [1, 3, 0, 2]]
        pls = [2, 1, 1, 2]
        idx = num // 3
        res = Cube()
        res.Co = [i for i in self.Co]
        for i, j in zip(surface[idx], replace[num % 3]):
            res.Co[i] = self.Co[surface[idx][j]]
        if num // 3 != 0 and num % 3 != 1:
            for i in range(4):
                res.Co[surface[idx][i]] += pls[i]
                res.Co[surface[idx][i]] %= 3
        res.Moves = [i for i in self.Moves]
        res.Moves.append(num)
        res.Movnum = self.Movnum + 1
        res.Movnum += 1 if len(self.Moves) >= 2 and num // 3 != self.Moves[-1] // 3 and num // 3 != self.Moves[-2] // 3 else 0
        res.Movnum += 1 if len(self.Moves) < 2 and num // 3 == 1 else 0
        return res

    # 回転番号に則って実際にパズルの状態配列を変化させる
    def move(self, num):
        res = Cube()
        res = self.move_co(num)
        res.Cp = self.move_cp(num).Cp
        return res

    # cp配列から固有の番号を作成
    def cp2i(self):
        res = 0
        marked = set([])
        for i in range(7):
            res += fac[6 - i] * len(set(range(self.Cp[i])) - marked)
            marked.add(self.Cp[i])
        return res
    
    # co配列から固有の番号を作成
    def co2i(self):
        res = 0
        for i in self.Co:
            res *= 3
            res += i
        return res


parts_place = [[[0, 2], [2, 0], [2, 7]], [[0, 3], [2, 6], [2, 5]], [[1, 2], [2, 2], [2, 1]], [[1, 3], [2, 4], [2, 3]], [[4, 2], [3, 1], [3, 2]], [[4, 3], [3, 3], [3, 4]], [[5, 3], [3, 5], [3, 6]], [[5, 2], [3, 7], [3, 0]]]
parts_color = [['w', 'o', 'b'], ['w', 'b', 'r'], ['w', 'g', 'o'], ['w', 'r', 'g'], ['y', 'o', 'g'], ['y', 'g', 'r'], ['y', 'r', 'b'], ['y', 'b', 'o']]
j2color = ['g', 'b', 'r', 'o', 'y', 'w']
direction_arr = [21, 12, 15, 18, 2, 22, 20, 4, 8, 13, 23, 1, 6, 0, 3, 9, 11, 16, 14, 7, 5, 19, 17, 10]


fac = [1]
for i in range(1, 8):
    fac.append(fac[-1] * i)



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
                cp[n_idx] = status.Movnum
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
                co[n_idx] = status.Movnum
                que.append(n_status)
    
    with open('cp' + str(idx) + '.csv', mode='x') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(cp)
    with open('co' + str(idx) + '.csv', mode='x') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(co)