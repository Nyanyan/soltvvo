# coding:utf-8
'''
Soltvvo3.2 Basic Functions
Soltvvo3.2 基本関数
Copyright 2020 Nyanyan
'''

''' キューブを回転させる関数 '''
''' Functions for twisting cube '''

# 回転処理 CP
# Rotate CP
def move_cp(cp, arr):
    # surfaceとreplace配列を使ってパーツを置換
    surface = [[3, 1, 7, 5], [1, 0, 6, 7], [0, 2, 4, 6], [2, 3, 5, 4]]
    replace = [[3, 0, 1, 2], [2, 3, 0, 1], [1, 2, 3, 0]]
    res = [i for i in cp]
    for i, j in zip(surface[arr[0]], replace[-(arr[1] + 1)]):
        res[surface[arr[0]][j]] = cp[i]
    return res

# 回転処理 CO
# Rotate CO
def move_co(co, arr):
    # surfaceとreplace配列を使ってパーツを置換した後pls配列を使って90度回転時のCOの変化を再現
    surface = [[3, 1, 7, 5], [1, 0, 6, 7], [0, 2, 4, 6], [2, 3, 5, 4]]
    replace = [[3, 0, 1, 2], [2, 3, 0, 1], [1, 2, 3, 0]]
    pls = [2, 1, 2, 1]
    res = [i for i in co]
    for i, j in zip(surface[arr[0]], replace[-(arr[1] + 1)]):
        res[surface[arr[0]][j]] = co[i]
    if arr[1] != -2:
        for i in range(4):
            res[surface[arr[0]][i]] += pls[i]
            res[surface[arr[0]][i]] %= 3
    return res


''' 配列のインデックス化 '''
''' Indexing'''

# cp配列から固有の番号を作成
# Return the number of CP
def cp2idx(cp):
    # 階乗進数でインデックス化
    res = 0
    for i in range(8):
        cnt = cp[i]
        for j in cp[:i]:
            if j < cp[i]:
                cnt -= 1
        res += fac[7 - i] * cnt
    return res

# co配列から固有の番号を作成
# Return the number of CO
def co2idx(co):
    # 3進数でインデックス化。7つのパーツを見れば状態が一意に定まる
    res = 0
    for i in co[:7]:
        res *= 3
        res += i
    return res

# 固有の番号からcp配列を作成
# Return the array of CP
def idx2cp(cp_idx):
    # 階乗進数から配列への変換
    res = [-1 for _ in range(8)]
    for i in range(8):
        candidate = cp_idx // fac[7 - i]
        marked = [True for _ in range(i)]
        for _ in range(8):
            for j, k in enumerate(res[:i]):
                if k <= candidate and marked[j]:
                    candidate += 1
                    marked[j] = False
        res[i] = candidate
        cp_idx %= fac[7 - i]
    return res

# 固有の番号からco配列を作成
# Return the array of CO
def idx2co(co_idx):
    # 3進数から配列への変換
    res = [0 for _ in range(8)]
    for i in range(7):
        res[6 - i] = co_idx % 3
        co_idx //= 3
    res[7] = (3 - sum(res) % 3) % 3
    return res

''' 定数 '''
''' Constants '''

# 階乗の値
fac = [1]
for i in range(1, 9):
    fac.append(fac[-1] * i)

# よく使う値と配列
grip_cost = 1
j2color = ['g', 'b', 'r', 'o', 'y', 'w']
dic = {'w':'white', 'g':'green', 'r':'red', 'b':'blue', 'o':'magenta', 'y':'yellow'}
parts_color = [['w', 'o', 'b'], ['w', 'b', 'r'], ['w', 'g', 'o'], ['w', 'r', 'g'], ['y', 'o', 'g'], ['y', 'g', 'r'], ['y', 'b', 'o'], ['y', 'r', 'b']]
parts_place = [[[0, 2], [2, 0], [2, 7]], [[0, 3], [2, 6], [2, 5]], [[1, 2], [2, 2], [2, 1]], [[1, 3], [2, 4], [2, 3]], [[4, 2], [3, 1], [3, 2]], [[4, 3], [3, 3], [3, 4]], [[5, 2], [3, 7], [3, 0]], [[5, 3], [3, 5], [3, 6]]]
twist_lst = [[[0, -1]], [[0, -2]], [[2, -1]], [[0, -1], [2, -1]], [[0, -2], [2, -1]], [[0, -1], [2, -2]], [[1, -1]], [[1, -2]], [[3, -1]], [[1, -1], [3, -1]], [[1, -2], [3, -1]], [[1, -1], [3, -2]]]
cost_lst = [1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 2, 2]
solved_cp = [[0, 1, 2, 3, 4, 5, 6, 7], [2, 3, 4, 5, 6, 7, 0, 1], [4, 5, 6, 7, 0, 1, 2, 3], [6, 7, 0, 1, 2, 3, 4, 5], [1, 7, 3, 5, 2, 4, 0, 6], [3, 5, 2, 4, 0, 6, 1, 7], [2, 4, 0, 6, 1, 7, 3, 5], [0, 6, 1, 7, 3, 5, 2, 4], [7, 6, 5, 4, 3, 2, 1, 0], [5, 4, 3, 2, 1, 0, 7, 6], [3, 2, 1, 0, 7, 6, 5, 4], [1, 0, 7, 6, 5, 4, 3, 2], [6, 0, 4, 2, 5, 3, 7, 1], [4, 2, 5, 3, 7, 1, 6, 0], [5, 3, 7, 1, 6, 0, 4, 2], [7, 1, 6, 0, 4, 2, 5, 3], [2, 0, 3, 1, 5, 7, 4, 6], [3, 1, 5, 7, 4, 6, 2, 0], [5, 7, 4, 6, 2, 0, 3, 1], [4, 6, 2, 0, 3, 1, 5, 7], [6, 4, 7, 5, 1, 3, 0, 2], [7, 5, 1, 3, 0, 2, 6, 4], [1, 3, 0, 2, 6, 4, 7, 5], [0, 2, 6, 4, 7, 5, 1, 3]]
solved_co = [[0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [1, 2, 2, 1, 1, 2, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [1, 2, 2, 1, 1, 2, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0], [2, 1, 1, 2, 2, 1, 1, 2]]
neary_solved_depth = 15

print('basic functions initialized')
