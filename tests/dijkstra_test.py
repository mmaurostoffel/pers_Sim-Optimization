import pandas as pd
import tkinter as tk
from tkinter import filedialog

import heapq


def selectInputFile():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    return file_path

def readInputList(file):
    input = pd.read_csv(file)
    input = input.replace(to_replace='x', value=0, regex=True)

    input = input.map(pd.to_numeric, errors='coerce')

    return input





# imported from chatGPT


def dijkstra(graph, start, end):
    num_nodes = len(graph)
    distances = {node: float('inf') for node in range(num_nodes)}
    distances[start] = 0
    priority_queue = [(0, start)]  # (distance, node)
    previous_nodes = {node: None for node in range(num_nodes)}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break  # Stop if we reached the destination

        for neighbor, weight in enumerate(graph[current_node]):
            if weight > 0:  # Only consider existing edges
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruct shortest path
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous_nodes[node]
    path.reverse()

    return path, distances[end] if distances[end] != float('inf') else ([], float('inf'))



file = selectInputFile()
graph = readInputList(file).to_numpy()


# Example: Find shortest path from node 0 to node 8
start_node = 4
end_node = 8
path, distance = dijkstra(graph, start_node, end_node)
print(f"Shortest path from {start_node} to {end_node}: {path} with distance {distance}")