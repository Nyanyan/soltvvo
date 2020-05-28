import heapq  # heapqライブラリのimport

a = [[1, 6], [2, 5]]
heapq.heapify(a)  # リストを優先度付きキューへ
print(a)
print(heapq.heappop(a))