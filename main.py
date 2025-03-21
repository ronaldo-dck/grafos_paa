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

import matplotlib.pyplot as plt
import networkx as nx

def plot_graph(n, mst):
    """
    Desenha o gráfico a partir de uma Árvore Geradora Mínima (AGM).
    
    :param n: Número de vértices.
    :param mst: Lista de arestas da AGM no formato (u, v, peso).
    """
    G = nx.Graph()
    
    # Adiciona os vértices
    G.add_nodes_from(range(n))
    
    # Adiciona as arestas com os pesos
    for u, v, weight in mst:
        G.add_edge(u, v, weight=weight)
    
    # Define a posição dos nós para o layout
    pos = nx.spring_layout(G, seed=42)  # Layout para melhor visualização
    
    # Desenha os nós e arestas
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    
    # Adiciona os pesos das arestas
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    # Exibe o gráfico
    plt.title("Árvore Geradora Mínima")
    plt.show()

# Exemplo de uso
# plot_graph(n, mst_kruskal)  # Para desenhar a AGM gerada pelo Kruskal
# plot_graph(n, mst_prim)     # Para desenhar a AGM gerada pelo Prim

import sys 
algorithm = sys.argv[1]
filename = sys.argv[2]  
n, edges, adj = read_graph_from_file(filename)

if algorithm == 'kruskal':
    mst, cost = kruskal(n, edges)
elif algorithm == 'prim':
    mst, cost = prim(n, adj)

# print(n,',',algorithm,',', cost,',', f'"{mst}"')
print(cost)
