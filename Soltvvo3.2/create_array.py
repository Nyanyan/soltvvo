# coding:utf-8
'''
Soltvvo3.2 Pre-calculation
Soltvvo3.2 事前計算
Copyright 2020 Nyanyan
'''

from collections import deque
import csv

from basic_functions import *


''' 状態の遷移テーブルを作る '''
''' Create state transition tables '''

def create_cp_trans():
    # CPの遷移配列
    # 8!個の状態それぞれに対して12種類の回転でどう遷移するかを記述
    cp_trans = [[-1 for _ in range(12)] for _ in range(fac[8])]
    # 遷移前の状態を表す番号idxを回す
    for idx in range(fac[8]):
        if idx % 1000 == 0:
            print(idx / fac[8])
        # idxからCP配列を作り、実際に回す
        cp = idx2cp(idx)
        for i, twist in enumerate(twist_lst):
            twisted_cp = [j for j in cp]
            for each_twist in twist:
                twisted_cp = move_cp(twisted_cp, each_twist)
            # CP配列を固有の番号に変換
            twisted_idx = cp2idx(twisted_cp)
            cp_trans[idx][i] = twisted_idx
    # CSVファイルに保存
    with open('cp_trans.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in cp_trans:
            writer.writerow(line)
    print('cp trans done')

def create_co_trans():
    # 処理の内容はcreate_cp_transのCPがCOになったのみ
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


''' 枝刈り用配列を作る '''
''' Create prunning tables '''

def create_cp_cost():
    # 状態の遷移配列を読み込む
    cp_trans = []
    with open('cp_trans.csv', mode='r') as f:
        for line in map(str.strip, f):
            cp_trans.append([int(i) for i in line.replace('\n', '').split(',')])
    # 8!個の各状態に対してコストを計算する
    cp_cost = [1000 for _ in range(fac[8])]
    # 幅優先探索をするのでキューに最初の(揃っている)状態を入れておく
    solved_cp_idx = [cp2idx(i) for i in solved_cp]
    que = deque([[i, 0] for i in solved_cp_idx])
    for i in solved_cp_idx:
        cp_cost[i] = 0
    cnt = 0
    # 幅優先探索
    while que:
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt, len(que))
        # キューから状態を取得
        cp, cost = que.popleft()
        twists = range(12)
        # 回転させ、コストを計算する
        for twist, cost_pls in zip(twists, cost_lst):
            twisted_idx = cp_trans[cp][twist]
            n_cost = cost + grip_cost + cost_pls
            # コストの更新があったら配列を更新し、キューに追加
            if cp_cost[twisted_idx] > n_cost:
                cp_cost[twisted_idx] = n_cost
                que.append([twisted_idx, n_cost])
    # CSVファイルに保存
    with open('cp_cost.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(cp_cost)
    print('cp cost done')

def create_co_cost():
    # 処理の内容はcreate_cp_transのCPがCOになったのみ
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


''' 逆手順を回した際の状態遷移配列を作る '''
''' Create state transition tables for reverse twists'''

def create_cp_trans_rev():
    # 基本的な処理はcreate_cp_transと同じ
    cp_trans_rev = [[-1 for _ in range(12)] for _ in range(fac[8])]
    for idx in range(fac[8]):
        if idx % 1000 == 0:
            print(idx / fac[8])
        cp = idx2cp(idx)
        for i, twist in enumerate(twist_lst):
            twisted_cp = [j for j in cp]
            for each_twist in twist:
                twisted_cp = move_cp(twisted_cp, each_twist)
            twisted_idx = cp2idx(twisted_cp)
            # create_cp_transと違いcp_trans_rev[twisted_idx][i]を更新する
            cp_trans_rev[twisted_idx][i] = idx
    with open('cp_trans_rev.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in cp_trans_rev:
            writer.writerow(line)
    print('cp trans rev done')

def create_co_trans_rev():
    # 基本的な処理はcreate_co_transと同じ
    co_trans_rev = [[-1 for _ in range(12)] for _ in range(3 ** 7)]
    for idx in range(3 ** 7):
        if idx % 1000 == 0:
            print(idx / 3 ** 7)
        co = idx2co(idx)
        for i, twist in enumerate(twist_lst):
            twisted_co = [j for j in co]
            for each_twist in twist:
                twisted_co = move_co(twisted_co, each_twist)
            twisted_idx = co2idx(twisted_co)
            # create_co_transと違いco_trans_rev[twisted_idx][i]を更新する
            co_trans_rev[twisted_idx][i] = idx
    with open('co_trans_rev.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in co_trans_rev:
            writer.writerow(line)
    print('co trans rev done')


''' あと少しで揃う状態を列挙する '''
''' Create array of states that can be solved soon '''

def create_neary_solved():
    # 逆手順の遷移配列を読み込む
    cp_trans_rev = []
    with open('cp_trans_rev.csv', mode='r') as f:
        for line in map(str.strip, f):
            cp_trans_rev.append([int(i) for i in line.replace('\n', '').split(',')])
    co_trans_rev = []
    with open('co_trans_rev.csv', mode='r') as f:
        for line in map(str.strip, f):
            co_trans_rev.append([int(i) for i in line.replace('\n', '').split(',')])
    # neary_solved配列を更新していくが、計算を高速にするため他の配列も用意する
    neary_solved = []
    neary_solved_idx = set()
    neary_solved_cost_dic = {}
    neary_solved_idx_dic = {}
    # 幅優先探索のキューを作る
    solved_cp_idx = [cp2idx(i) for i in solved_cp]
    solved_co_idx = [co2idx(i) for i in solved_co]
    que = deque([])
    for i in range(24):
        twisted_idx = solved_cp_idx[i] * 2187 + solved_co_idx[i]
        neary_solved_idx.add(twisted_idx)
        neary_solved_cost_dic[twisted_idx] = 0
        neary_solved_idx_dic[twisted_idx] = len(neary_solved)
        neary_solved.append([twisted_idx, 0, []])
        que.append([solved_cp_idx[i], solved_co_idx[i], 0, [], 2])
    twists = [range(6, 12), range(6), range(12)]
    cnt = 0
    while que:
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt, len(que))
        # キューから状態を取得
        cp_idx, co_idx, cost, move, mode = que.popleft()
        for twist in twists[mode]:
            # 回転後の状態とコストを取得、手順リストを更新
            cost_pls = cost_lst[twist]
            twisted_cp_idx = cp_trans_rev[cp_idx][twist]
            twisted_co_idx = co_trans_rev[co_idx][twist]
            twisted_idx = twisted_cp_idx * 2187 + twisted_co_idx
            n_cost = cost + grip_cost + cost_pls
            n_mode = twist // 6
            n_move = [i for i in move]
            n_move.append(twist)
            if neary_solved_depth >= n_cost and not twisted_idx in neary_solved_idx:
                # 新しく見た状態だった場合
                neary_solved_idx.add(twisted_idx)
                neary_solved_cost_dic[twisted_idx] = n_cost
                neary_solved_idx_dic[twisted_idx] = len(neary_solved)
                neary_solved.append([twisted_idx, n_cost, list(reversed(n_move))])
                que.append([twisted_cp_idx, twisted_co_idx, n_cost, n_move, n_mode])
            elif neary_solved_depth >= n_cost and neary_solved_cost_dic[twisted_idx] > n_cost:
                # すでに見た状態だがその時よりも低いコストでその状態に到達できた場合
                neary_solved_cost_dic[twisted_idx] = n_cost
                neary_solved[neary_solved_idx_dic[twisted_idx]] = [twisted_idx, n_cost, list(reversed(n_move))]
                que.append([twisted_cp_idx, twisted_co_idx, n_cost, n_move, n_mode])
    # solverパートでは2分探索を用いるため、予めインデックスでソートしておく
    neary_solved.sort()
    # インデックスとコストをCSVに配列を保存
    with open('neary_solved_idx.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in [i[:2] for i in neary_solved]:
            writer.writerow(line)
    # 手順をCSV配列に保存
    with open('neary_solved_solution.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for line in [i[2] for i in neary_solved]:
            writer.writerow(line)
    print('neary solved done')

create_cp_trans()
create_co_trans()
create_cp_cost()
create_co_cost()
create_cp_trans_rev()
create_co_trans_rev()
create_neary_solved()