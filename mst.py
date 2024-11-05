import matplotlib.pyplot as plt
import networkx as nx

# Define a weighted undirected graph with 7 vertices and edges with weights
edges = [
    (1, 2, 4), (1, 3, 1), (2, 3, 3), (2, 4, 2), 
    (3, 5, 5), (4, 5, 1), (4, 6, 6), (5, 6, 2), 
    (5, 7, 7), (6, 7, 3)
]

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if len(self.heap) == 1:
            return self.heap.pop()
        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return min_item

    def _sift_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._sift_up(parent)

    def _sift_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._sift_down(smallest)

    def is_empty(self):
        return len(self.heap) == 0


def draw_graph(graph, pos, title):
    plt.figure(figsize=(10, 5))
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10)
    edge_labels = {(u, v): w for u, v, w in graph.edges(data="weight")}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.show()

# Prim's algorithm for MST
def prim_mst(vertices, edges):
    mst_edges = []
    visited = set()
    adj_list = {i: [] for i in range(1, vertices + 1)}

    for u, v, weight in edges:
        adj_list[u].append((weight, u, v))
        adj_list[v].append((weight, v, u))

    min_heap = MinHeap()
    for edge in adj_list[1]:
        min_heap.push(edge)
    visited.add(1)

    while not min_heap.is_empty() and len(visited) < vertices:
        weight, u, v = min_heap.pop()
        if v not in visited:
            visited.add(v)
            mst_edges.append((u, v, weight))
            for next_weight, _, next_vertex in adj_list[v]:
                if next_vertex not in visited:
                    min_heap.push((next_weight, v, next_vertex))
    return mst_edges

# Kruskal's algorithm for MST
def kruskal_mst(vertices, edges):
    parent = {i: i for i in range(1, vertices + 1)}

    def find(v):
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]

    def union(v1, v2):
        root1, root2 = find(v1), find(v2)
        if root1 != root2:
            parent[root2] = root1

    mst_edges = []
    edges = sorted(edges, key=lambda x: x[2])

    for u, v, weight in edges:
        if find(u) != find(v):
            union(u, v)
            mst_edges.append((u, v, weight))
            if len(mst_edges) == vertices - 1:
                break
    return mst_edges

# Borůvka's algorithm for MST
def boruvka_mst(vertices, edges):
    parent = {i: i for i in range(1, vertices + 1)}
    mst_edges = []

    def find(v):
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]

    def union(v1, v2):
        root1, root2 = find(v1), find(v2)
        if root1 != root2:
            parent[root2] = root1

    components = vertices
    while components > 1:
        min_edge = {}
        for u, v, weight in edges:
            u_root, v_root = find(u), find(v)
            if u_root != v_root:
                if u_root not in min_edge or min_edge[u_root][0] > weight:
                    min_edge[u_root] = (weight, u, v)
                if v_root not in min_edge or min_edge[v_root][0] > weight:
                    min_edge[v_root] = (weight, u, v)

        for weight, u, v in min_edge.values():
            u_root, v_root = find(u), find(v)
            if u_root != v_root:
                union(u, v)
                mst_edges.append((u, v, weight))
                components -= 1
    return mst_edges


def select_algorithm(algorithm, vertices, edges):
    if algorithm.lower() == '1':
        return prim_mst(vertices, edges)
    elif algorithm.lower() == '2':
        return kruskal_mst(vertices, edges)
    elif algorithm.lower() == '3':
        return boruvka_mst(vertices, edges)
    else:
        print("Invalid algorithm choice. Please select 'Prim', 'Kruskal', or 'Boruvka'.")
        return None


G = nx.Graph()
G.add_weighted_edges_from(edges)


pos = nx.spring_layout(G)
draw_graph(G, pos, "Original Graph")

while True:
    algorithm = input("Choose MST algorithm (1.Prim/2.Kruskal/3.Boruvka) or type '4.exit' to quit: ")
    if algorithm.lower() == '4':
        print("Exiting the program.")
        break

    mst_edges = select_algorithm(algorithm, 7, edges)
    if mst_edges:
        mst_graph = nx.Graph()
        mst_graph.add_weighted_edges_from(mst_edges)
        draw_graph(mst_graph, pos, f"Minimum Spanning Tree ({algorithm.capitalize()}'s Algorithm)")
