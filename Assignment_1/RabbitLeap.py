from collections import deque

class State:
    def __init__(self, config, parent=None):
        self.config = config
        self.parent = parent

    def goal_test(self):
        return self.config == "WWW_EEE"

    def get_children(self):
        children = []
        s = self.config
        idx = s.index('_')

        # Move 'E' to the right
        if idx > 0 and s[idx - 1] == 'E':
            new_config = list(s)
            new_config[idx], new_config[idx - 1] = new_config[idx - 1], new_config[idx]
            children.append(State(''.join(new_config), self))
        if idx > 1 and s[idx - 2] == 'E' and s[idx - 1] in 'W':
            new_config = list(s)
            new_config[idx], new_config[idx - 2] = new_config[idx - 2], new_config[idx]
            children.append(State(''.join(new_config), self))

        # Move 'W' to the left
        if idx < 6 and s[idx + 1] == 'W':
            new_config = list(s)
            new_config[idx], new_config[idx + 1] = new_config[idx + 1], new_config[idx]
            children.append(State(''.join(new_config), self))
        if idx < 5 and s[idx + 2] == 'W' and s[idx + 1] in 'E':
            new_config = list(s)
            new_config[idx], new_config[idx + 2] = new_config[idx + 2], new_config[idx]
            children.append(State(''.join(new_config), self))

        return children

    def path(self):
        node, p = self, []
        while node:
            p.append(node.config)
            node = node.parent
        return p[::-1]


# Breadth-First Search
def bfs(start_config):
    start = State(start_config)
    queue = deque([start])
    visited = set([start_config])

    while queue:
        current = queue.popleft()
        if current.goal_test():
            return current.path()

        for child in current.get_children():
            if child.config not in visited:
                visited.add(child.config)
                queue.append(child)

    return None


# Depth-First Search (recursive)
def dfs(start_config, visited=None):
    if visited is None:
        visited = set()

    start = State(start_config)
    return dfs_helper(start, visited)


def dfs_helper(state, visited):
    if state.config in visited:
        return None
    visited.add(state.config)

    if state.goal_test():
        return state.path()

    for child in state.get_children():
        result = dfs_helper(child, visited)
        if result:
            return result

    return None


# Run both BFS and DFS
start = "EEE_WWW"

print("Using BFS:")
bfs_path = bfs(start)
if bfs_path:
    for step in bfs_path:
        print(step)
else:
    print("No solution found using BFS.")

print("\nUsing DFS:")
dfs_path = dfs(start)
if dfs_path:
    for step in dfs_path:
        print(step)
else:
    print("No solution found using DFS.")
