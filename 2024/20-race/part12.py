import dataclasses
import heapq
import itertools
import math
import os
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]

adj = [1, 1j, -1, -1j]


# avoid sorting issue in heapq for equal priorities/distances
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().splitlines()


def in_maze(v: complex, maze: list[str]) -> bool:
    return 0 <= v.imag < len(maze) and 0 <= v.real < len(maze[0])


def is_wall(v: complex, maze: list[str]) -> bool:
    return maze[int(v.imag)][int(v.real)] == '#'


def neighbors(maze: list[str], v: tuple[complex]) -> list[tuple[complex, int]]:
    neighbors = []
    for d in adj:
        v_n = v + d
        if in_maze(v_n, maze) and not is_wall(v_n, maze):
            neighbors.append((v_n, 1))
    return neighbors


def dijkstra(maze: list[str], start: tuple[complex, int], end: complex) -> tuple[int, list[complex]]:
    # Initialize distances dictionary
    distances = {
        complex(v[0], v[1]): math.inf
        for v in itertools.product(range(len(maze[0])), range(len(maze)))
        if not is_wall(complex(v[0], v[1]), maze)
    }

    distances[start] = 0
    pq = [PrioritizedItem(0, start)]

    # Initialize previous node dictionary to store shortest path
    previous = {}
    while pq:
        current_distance, current_node = dataclasses.astuple(heapq.heappop(pq))
        # If we already found a shorter path to the current node, skip
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor, weight in neighbors(maze, current_node):
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, PrioritizedItem(distance, neighbor))

        # Stop if we reached the destination
        if current_node == end:
            end = current_node
            break

    # Reconstruct the shortest path
    path = []
    node = end
    while node != start:
        path.append(node)
        node = previous[node]
    path.append(start)
    path.reverse()

    return distances[end], path


def find_cell(maze: list[str], c: str) -> complex:
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == c:
                return complex(x, y)


def cheats(maze: list[str], d_max_save: int, cheat_duration: int) -> dict[int, set[tuple[complex, complex]]]:
    v_start = find_cell(maze, 'S')
    v_end = find_cell(maze, 'E')

    # shortest path without cheating
    _, p = dijkstra(maze, v_start, v_end)

    valid_steps = []
    for x in range(-cheat_duration, cheat_duration + 1):
        for y in range(-cheat_duration, cheat_duration + 1):
            v = complex(x, y)
            if abs(x) + abs(y) <= cheat_duration and v != 0:
                valid_steps.append(v)

    c = defaultdict(set)
    for i, v in enumerate(p):
        # print(f'{i}/{len(p)}')

        for d in valid_steps:
            v2 = v + d
            try:
                i_cheat = p.index(v2, i)
                if not is_wall(p[i_cheat], maze):
                    saved = i_cheat - i - (abs(d.real) + abs(d.imag))
                    if saved >= d_max_save:
                        c[int(saved)].add((v, p[i_cheat]))
            except ValueError:
                pass

    return c


def total_cheats(maze: list[str], d_max_save: int = 100, cheat_duration: int = 2) -> int:
    c = cheats(maze, d_max_save, cheat_duration)
    return sum(map(len, c.values()))


maze = read_data(test_input_files[0])
c = cheats(maze, 1, 2)
assert len(c[2]) == 14
assert len(c[4]) == 14
assert len(c[6]) == 2
assert len(c[8]) == 4
assert len(c[10]) == 2
assert len(c[12]) == 3
assert len(c[20]) == 1
assert len(c[36]) == 1
assert len(c[38]) == 1
assert len(c[40]) == 1
assert len(c[64]) == 1

d = total_cheats(read_data(input_file), 100, 2)
print(d)


c = cheats(maze, 1, 20)
assert len(c[50]) == 32
assert len(c[52]) == 31
assert len(c[54]) == 29
assert len(c[56]) == 39
assert len(c[58]) == 25
assert len(c[60]) == 23
assert len(c[62]) == 20
assert len(c[64]) == 19
assert len(c[66]) == 12
assert len(c[68]) == 14
assert len(c[70]) == 12
assert len(c[72]) == 22
assert len(c[74]) == 4
assert len(c[76]) == 3


d = total_cheats(read_data(input_file), 100, 20)
print(d)
