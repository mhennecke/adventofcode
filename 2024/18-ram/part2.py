import dataclasses
import heapq
import itertools
import math
import os
from dataclasses import dataclass, field
from typing import Any

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(2)]

adj = [1, 1j, -1, -1j]


# avoid sorting issue in heapq for equal priorities/distances
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


def read_data(file_name: str) -> list[complex]:
    with open(file_name, 'r') as f:
        return list(map(lambda line: complex(*map(int, line.split(','))), f.read().splitlines()))


def neighbors(corrupted_bytes: list[complex], mem_size: tuple[int, int], v: complex) -> list[tuple[complex, int]]:
    neighbors = []
    for d in adj:
        v_n = v + d
        if v_n not in corrupted_bytes and 0 <= v_n.real < mem_size[0] and 0 <= v_n.imag < mem_size[1]:
            neighbors.append((v_n, 1))
    return neighbors


def dijkstra(corrupted_bytes: list[complex], mem_size: tuple[int, int], start: complex, end: complex) -> tuple[int, list[complex]]:
    # Initialize distances dictionary
    distances = {complex(v[0], v[1]): math.inf for v in itertools.product(range(int(mem_size[0])), range(int(mem_size[1])))}

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
        for neighbor, weight in neighbors(corrupted_bytes, mem_size, current_node):
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
        try:
            node = previous[node]
        except KeyError:
            return math.inf, []
    path.append(start)
    path.reverse()

    return distances[end], path


def min_score_path(corrupted_bytes: list[complex], mem_size: tuple[int, int]) -> int:
    v_start = complex(0, 0)
    v_end = complex(mem_size[0] - 1, mem_size[1] - 1)

    d, _ = dijkstra(corrupted_bytes, mem_size, v_start, v_end)

    return d


def first_blocker(corrupted_bytes: list[complex], mem_size: tuple[int, int]) -> complex:
    left, right = 0, len(corrupted_bytes) - 1
    while left < right:
        mid = (left + right) // 2
        d = min_score_path(corrupted_bytes[:mid], mem_size)
        if d == math.inf:
            right = mid
        else:
            left = mid + 1
    return corrupted_bytes[mid]


assert first_blocker(read_data(test_input_files[0]), (7, 7)) == complex(6, 1)


b = first_blocker(read_data(input_file), (71, 71))
print(f'{int(b.real)},{int(b.imag)}')
