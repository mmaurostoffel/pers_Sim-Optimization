import heapq

def dijkstra(graph, start, end):
    num_nodes = len(graph)
    distances = {node: float('inf') for node in range(num_nodes)}
    distances[start] = 0
    priority_queue = [(0, start)]
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

def getWaypoints(graph, start, end):
    path, distance = dijkstra(graph, start, end)
    return path, distance