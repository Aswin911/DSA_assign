import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import heapq

def create_graph():
    # Create a directed graph
    G = nx.DiGraph()

    # Add edges along with their weights
    edges = [
        ('A', 'B', 1),
        ('A', 'C', 4),
        ('B', 'C', 2),
        ('B', 'D', 5),
        ('C', 'D', 1),
        ('D', 'E', 3),
        ('C', 'E', 6),
    ]
    
    G.add_weighted_edges_from(edges)
    return G

def display_graph(G, highlighted_path=None):
    pos = nx.spring_layout(G)  # positions for all nodes
    weights = nx.get_edge_attributes(G, 'weight')
    
    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=16, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
    
    # Highlight the shortest path if provided
    if highlighted_path:
        path_edges = list(zip(highlighted_path, highlighted_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2)
    
    plt.title("Directed Weighted Graph")
    plt.show()

def dijkstra(G, start):
    distances = {node: float('infinity') for node in G.nodes}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in G[current_node].items():
            distance = current_distance + weight['weight']

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

def floyd_warshall(G, start):
    nodes = list(G.nodes)
    n = len(nodes)
    dist = np.full((n, n), np.inf)

    for i in range(n):
        dist[i][i] = 0  # Distance from a node to itself is 0
        for j in range(n):
            if (nodes[i], nodes[j]) in G.edges:
                dist[i][j] = G[nodes[i]][nodes[j]]['weight']

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # Collect results for distances from the starting node
    start_index = nodes.index(start)
    distances_from_start = {nodes[i]: dist[start_index][i] for i in range(n)}

    return distances_from_start

def bellman_ford(G, start):
    distances = {node: float('infinity') for node in G.nodes}
    distances[start] = 0

    for _ in range(len(G.nodes) - 1):
        for u, v, weight in G.edges(data='weight'):
            if distances[u] != float('infinity') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight

    return distances

def main():
    G = create_graph()
    display_graph(G)
    
    while True:
        print("\nChoose an algorithm to execute:")
        print("1. Dijkstra's Algorithm")
        print("2. Floyd-Warshall Algorithm")
        print("3. Bellman-Ford Algorithm")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice in ['1', '2', '3']:
            start = input("Enter the starting vertex (A, B, C, D, E): ")
            if start not in G.nodes:
                print("Invalid starting vertex.")
                continue

            if choice == '1':
                dijkstra_result = dijkstra(G, start)
                print(f"Dijkstra's shortest paths from {start}:", dijkstra_result)
            
            elif choice == '2':
                floyd_warshall_result = floyd_warshall(G, start)
                print(f"Floyd-Warshall shortest paths from {start}:", floyd_warshall_result)
            
            elif choice == '3':
                bellman_ford_result = bellman_ford(G, start)
                print(f"Bellman-Ford shortest paths from {start}:", bellman_ford_result)
        
        elif choice == '4':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

main()
