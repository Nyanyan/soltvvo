def distance(cp_idx, co_idx):
    return max(cp_cost[cp_idx], co_cost[co_idx])

with open('cp_cost.csv', mode='r') as f:
    cp_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('co_cost.csv', mode='r') as f:
    co_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('cp_trans.csv', mode='r') as f:
    cp_trans = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('co_trans.csv', mode='r') as f:
    co_trans = [int(i) for i in f.readline().replace('\n', '').split(',')]
