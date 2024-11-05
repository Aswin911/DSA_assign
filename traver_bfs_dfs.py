import matplotlib.pyplot as plt
import networkx as nx

class Graph:
    def __init__(self):
        self.vertices = []
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices.append(vertex)
            self.graph[vertex] = []
        else:
            print(f"Vertex '{vertex}' already exists!")

    def add_edge(self, src, dest):
        if src in self.graph and dest in self.graph:
            if dest not in self.graph[src]:
                self.graph[src].append(dest)
        else:
            print(f"Invalid edge: ({src}, {dest}). Both vertices must exist.")

    def dfs_iterative(self, start_node):
        if start_node not in self.vertices:
            print(f"Invalid starting node: {start_node}.")
            return []

        visited = set()
        stack = [start_node]
        dfs_path = []

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                dfs_path.append(node)
                stack.extend(reversed(self.graph[node]))  # Reverse to maintain order

        print("DFS Traversal Order:", dfs_path)
        return dfs_path

    def bfs(self, start_node):
        if start_node not in self.vertices:
            print(f"Invalid starting node: {start_node}.")
            return []

        visited = set([start_node])
        queue = [start_node]
        bfs_path = []

        while queue:
            node = queue.pop(0)  # Dequeue a vertex
            bfs_path.append(node)  # Visit the vertex
            for neighbor in self.graph[node]:  # Check all neighbors
                if neighbor not in visited:  # If not visited, mark and enqueue
                    visited.add(neighbor)
                    queue.append(neighbor)

        print("BFS Traversal Order:", bfs_path)
        return bfs_path

    def plot_graph(self, path, title):
        G = nx.DiGraph()
        for node, neighbors in self.graph.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        pos = nx.circular_layout(G)
        nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="gray", 
                node_size=700, font_size=12, arrowsize=20, arrowstyle='-|>')
        edges_in_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color="red", width=2.5)
        plt.title(title)
        plt.show()

def main():
    try:
        graph = Graph()
        num_vertices = int(input("Enter the number of vertices: "))
        print("Enter the names of the vertices:")
        for _ in range(num_vertices):
            vertex = input("Vertex: ")
            graph.add_vertex(vertex)
        num_edges = int(input("Enter the number of edges: "))
        print("Enter the edges in the format 'source destination':")
        for _ in range(num_edges):
            src, dest = input().split()
            graph.add_edge(src, dest)

        while True:
            print("\nMenu:")
            print("1. Perform DFS")
            print("2. Perform BFS")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ")

            if choice == '1':
                start_node = input("Enter the starting node for DFS: ")
                dfs_path = graph.dfs_iterative(start_node)
                graph.plot_graph(dfs_path, "Directed Graph with DFS Traversal")
            elif choice == '2':
                start_node_bfs = input("Enter the starting node for BFS: ")
                bfs_path = graph.bfs(start_node_bfs)
                graph.plot_graph(bfs_path, "Directed Graph with BFS Traversal")
            elif choice == '3':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice! Please select 1, 2, or 3.")

    except ValueError:
        print("Invalid input! Please enter valid integers.")

if __name__ == "__main__":
    main()
