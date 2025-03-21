import heapq

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, v):
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])  
        return self.parent[v]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

def kruskal(n, edges):
    edges.sort(key=lambda edge: edge[2])  
    uf = UnionFind(n)
    mst = []
    total_cost = 0

    for u, v, weight in edges:
        if uf.find(u) != uf.find(v):  
            uf.union(u, v)
            mst.append((u, v, weight))
            total_cost += weight

    return mst, total_cost

def prim(n, adj):
    visited = [False] * n
    mst = []
    pq = [(0, 0, -1)]  
    total_cost = 0

    while pq:
        weight, u, prev = heapq.heappop(pq)
        if not visited[u]:
            visited[u] = True
            if prev != -1:
                mst.append((prev, u, weight))
                total_cost += weight

            for v, w in adj[u]:  
                if not visited[v]:
                    heapq.heappush(pq, (w, v, u))

    return mst, total_cost

# 1️⃣ LER O GRAFO A PARTIR DE UM ARQUIVO
def read_graph_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    n = int(lines[0].strip())  # Número de vértices
    matrix = [list(map(int, line.split())) for line in lines[1:n+1]]
    
    edges = []
    adj = {i: [] for i in range(n)}
    
    for i in range(n):
        for j in range(i + 1, n):  
            if matrix[i][j] > 0:  
                edges.append((i, j, matrix[i][j]))
                adj[i].append((j, matrix[i][j]))
                adj[j].append((i, matrix[i][j]))  

    return n, edges, adj

# 2️⃣ EXECUTAR OS ALGORITMOS
import sys 
filename = sys.argv[1]  
n, edges, adj = read_graph_from_file(filename)

mst_kruskal, cost_kruskal = kruskal(n, edges)
mst_prim, cost_prim = prim(n, adj)

print("Árvore Geradora Mínima - Kruskal:", mst_kruskal)
print("Custo Total - Kruskal:", cost_kruskal)

print("Árvore Geradora Mínima - Prim:", mst_prim)
print("Custo Total - Prim:", cost_prim)
