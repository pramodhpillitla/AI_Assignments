from collections import deque
from typing import List, Set, Tuple

class Person:
    def __init__(self, name: str, time: int):
        self.name = name
        self.time = time

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

class State:
    def __init__(self, left: Set[Person], right: Set[Person], umbrella_side: str, time: int, parent=None):
        self.left = frozenset(left)
        self.right = frozenset(right)
        self.umbrella_side = umbrella_side  # 'L' or 'R'
        self.time = time
        self.parent = parent

    def is_goal(self):
        return len(self.left) == 0 and self.umbrella_side == 'R' and self.time <= 60

    def __hash__(self):
        return hash((self.left, self.right, self.umbrella_side, self.time))

    def __eq__(self, other):
        return (self.left == other.left and self.right == other.right
                and self.umbrella_side == other.umbrella_side and self.time == other.time)

    def get_path(self):
        path = []
        state = self
        while state:
            path.append(state)
            state = state.parent
        return list(reversed(path))

    def __repr__(self):
        return f"Left: {[p.name for p in self.left]}, Right: {[p.name for p in self.right]}, Umbrella: {self.umbrella_side}, Time: {self.time}"

class BridgeProblem:
    def __init__(self):
        self.people = [
            Person("Amogh", 5),
            Person("Ameya", 10),
            Person("Grandmother", 20),
            Person("Grandfather", 25)
        ]
        self.initial_state = State(set(self.people), set(), 'L', 0)

    def generate_children(self, state: State) -> List[State]:
        children = []
        if state.umbrella_side == 'L':
            # Send 1 or 2 people from left to right
            left_people = list(state.left)
            for i in range(len(left_people)):
                for j in range(i, len(left_people)):
                    crossing = {left_people[i]} if i == j else {left_people[i], left_people[j]}
                    new_left = set(state.left) - crossing
                    new_right = set(state.right) | crossing
                    crossing_time = max(p.time for p in crossing)
                    new_time = state.time + crossing_time
                    child = State(new_left, new_right, 'R', new_time, state)
                    children.append(child)
        else:
            # Send one person back from right to left
            for p in state.right:
                crossing = {p}
                new_right = set(state.right) - crossing
                new_left = set(state.left) | crossing
                crossing_time = p.time
                new_time = state.time + crossing_time
                child = State(new_left, new_right, 'L', new_time, state)
                children.append(child)

        return [c for c in children if c.time <= 60]

    def bfs(self) -> List[State]:
        queue = deque([self.initial_state])
        visited = set()
        visited.add(self.initial_state)

        while queue:
            current = queue.popleft()
            if current.is_goal():
                return current.get_path()

            for child in self.generate_children(current):
                if child not in visited:
                    visited.add(child)
                    queue.append(child)
        return []

# Run the problem
problem = BridgeProblem()
solution_path = problem.bfs()

# Display the solution
if solution_path:
    print("Solution found within 60 minutes:\n")
    for step in solution_path:
        print(step)
    print(f"\nTotal time: {solution_path[-1].time} minutes")
else:
    print("No solution found within 60 minutes.")
