from collections import deque

def find_closest_waypoint(matrix, start, waypoints):
    rows, cols = len(matrix), len(matrix[0])
    visited = set()
    queue = deque([start])
    visited.add(start)
    waypoints_set = set(waypoints)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    while queue:
        x, y = queue.popleft()

        if (x, y) in waypoints_set:
            return (x, y)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and matrix[nx][ny] == 1:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

    return None
