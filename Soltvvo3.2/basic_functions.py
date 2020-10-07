# coding:utf-8
# 回転処理 CP
# Rotate CP
def move_cp(cp, arr):
    surface = [[3, 1, 5, 7], [1, 0, 7, 6], [0, 2, 6, 4], [2, 3, 4, 5]]
    replace = [[1, 3, 0, 2], [3, 2, 1, 0], [2, 0, 3, 1]]
    res = [i for i in cp]
    for i, j in zip(surface[arr[0]], replace[-arr[1] - 1]):
        res[i] = cp[surface[arr[0]][j]]
    return res

# 回転処理 CO
# Rotate CO
def move_co(co, arr):
    surface = [[3, 1, 5, 7], [1, 0, 7, 6], [0, 2, 6, 4], [2, 3, 4, 5]]
    replace = [[1, 3, 0, 2], [3, 2, 1, 0], [2, 0, 3, 1]]
    pls = [2, 1, 1, 2]
    res = [i for i in co]
    for i, j in zip(surface[arr[0]], replace[-arr[1] - 1]):
        res[i] = co[surface[arr[0]][j]]
    if arr[1] != -2:
        for i in range(4):
            res[surface[arr[0]][i]] += pls[i]
            res[surface[arr[0]][i]] %= 3
    return res

# cp配列から固有の番号を作成
# Return the number of CP
def cp2idx(cp):
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
    res = 0
    for i in co[:7]:
        res *= 3
        res += i
    return res

def idx2cp(cp_idx):
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

def idx2co(co_idx):
    res = [0 for _ in range(8)]
    for i in range(7):
        res[6 - i] = co_idx % 3
        co_idx //= 3
    res[7] = (3 - sum(res) % 3) % 3
    return res

fac = [1]
for i in range(1, 9):
    fac.append(fac[-1] * i)

grip_cost = 1
