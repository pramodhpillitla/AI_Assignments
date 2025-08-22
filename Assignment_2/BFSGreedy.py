import heapq
import math

def heuristic(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def get_neighbors(node, n, grid):
    directions = [(1,0), (-1,0), (0,1), (0,-1),
                  (1,1), (1,-1), (-1,1), (-1,-1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = node[0]+dx, node[1]+dy
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

def reconstruct_path(parent, current):
    path = []
    while current in parent:
        path.append(current)
        current = parent[current]
    path.append((0,0))
    return path[::-1]

def best_first_search(grid):
    n = len(grid)
    start, goal = (0,0), (n-1, n-1)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1, []

    pq = [(heuristic(start, goal), start)]
    visited = set()
    parent = {}

    while pq:
        _, current = heapq.heappop(pq)
        if current == goal:
            path = reconstruct_path(parent, current)
            return len(path), path

        visited.add(current)
        for neighbor in get_neighbors(current, n, grid):
            if neighbor not in visited:
                parent[neighbor] = current
                heapq.heappush(pq, (heuristic(neighbor, goal), neighbor))

    return -1, []

if __name__ == "__main__":
    test_cases = [
        [[0,1],[1,0]],
        [[0,0,0],[1,1,0],[1,1,0]],
        [[1,0,0],[1,1,0],[1,1,0]]
    ]

    for i, grid in enumerate(test_cases, 1):
        bfs_len, bfs_path = best_first_search(grid)
        print(f"\nExample {i}:")
        print(f"Best First Search -> Path length: {bfs_len}, Path: {bfs_path}")
