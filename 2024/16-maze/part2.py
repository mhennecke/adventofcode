from collections import defaultdict
from dataclasses import dataclass, field
import dataclasses
from typing import Any
import heapq
import math
import os


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(2)]

adj = [1, 1j, -1, -1j]


# avoid sorting issue in heapq for equal priorities/distances
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().splitlines()


def is_wall(v: complex, maze: list[str]) -> bool:
    return maze[int(v.imag)][int(v.real)] == '#'


def print_maze_path(maze: list[str], path: list[complex]):
    maze = [list(row) for row in maze]
    for v in path:
        maze[int(v.imag)][int(v.real)] = 'X'
    for row in maze:
        print(''.join(row))


def neighbors(maze: list[str], v: tuple[complex, complex]) -> list[tuple[tuple[complex, complex], int]]:
    neighbors = []
    v_center, head = v
    for v_n, h_n, w_n in [
        (v_center + head, head, 1),  # straight ahead
        (v_center + head * 1j, head * 1j, 1001),  # right
        (v_center - head * 1j, -head * 1j, 1001),  # left
    ]:
        if not is_wall(v_n, maze):
            neighbors.append(((v_n, h_n), w_n))
    return neighbors


def dijkstra(maze: list[str], start: tuple[complex, complex], end: list[tuple[complex, complex]]) -> tuple[int, list[complex]]:
    ends = []
    # Initialize distances dictionary
    distances = {}
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell != '#':
                # four nodes per cell: one for each direction, unless it's a wall
                for h in adj:
                    v = (complex(x, y), h)
                    if not is_wall(v[0], maze):
                        distances[v] = math.inf

    distances[start] = 0
    pq = [PrioritizedItem(0, start)]

    # Initialize previous node dictionary to store shortest path
    previous = defaultdict(set)
    while pq:
        current_distance, current_node = dataclasses.astuple(heapq.heappop(pq))
        # If we already found a shorter path to the current node, skip
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor, weight in neighbors(maze, current_node):
            distance = current_distance + weight
            if distance <= distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor].add(current_node)
                heapq.heappush(pq, PrioritizedItem(distance, neighbor))

        # Stop if we reached the destination
        if current_node in end:
            ends.append(current_node)
            break

    # all visited nodes of all shortest paths
    visited = set()
    q = list(ends)
    while q:
        node = q.pop()
        visited.add(node[0])
        for p in previous[node]:
            if p not in visited:
                q.append(p)

    return distances[ends[0]], visited


def best_paths_tiles(maze: list[str]) -> int:
    v_start = complex(1, len(maze) - 2)
    v_end = complex(len(maze[0]) - 2, 1)

    # start in east direction
    _, visited = dijkstra(maze, (v_start, adj[0]), [(v_end, h) for h in adj])

    # print_maze_path(maze, p)

    return len(visited)


assert best_paths_tiles(read_data(test_input_files[0])) == 45
assert best_paths_tiles(read_data(test_input_files[1])) == 64

d = best_paths_tiles(read_data(input_file))
print(d)
