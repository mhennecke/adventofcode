import os
import numpy as np
from functools import cache

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> np.ndarray:
    with open(file_name, 'r') as f:
        data = np.asarray(list(map(list, f.read().splitlines())))
    return data


def longest_hike(trails: np.ndarray, start=(0, 1), end=(-1, -2)) -> int:
    end = np.array(trails.shape) + end
    assert trails[*start] == '.'
    assert trails[*end] == '.'
    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    downhill = ['>', '^', '<', 'v']
    G = {start: []}

    visited = set()
    stack = [(start, start, 0)]
    while stack:
        pos, parent, distance = stack.pop()
        if all(pos == end):
            G[parent].append((pos, distance))
            continue

        new_positions = np.array(pos) + directions
        is_junction = sum(trails[*(new_positions).T] != '#') > 2
        if is_junction:
            # new node
            G[parent].append((pos, distance))
            G[pos] = G.get(pos, [])
            parent = pos
            distance = 0

        if pos not in visited:
            if trails[*pos] in downhill:
                stack.append((tuple(new_positions[downhill.index(trails[*pos])]), parent, distance + 1))
            else:
                for new_pos, slope in zip(new_positions, downhill):
                    new_pos = tuple(new_pos)
                    try:
                        if trails[*new_pos] in ['.', slope]:
                            stack.append((new_pos, parent, distance + 1))
                    except IndexError:
                        pass
        visited.add(pos)

    @cache
    def max_distance(node):
        distances = {}
        for v, w in G[node]:
            if v in G:
                distances[v] = max_distance(v) + w
            else:
                distances[v] = w
        return max(distances.values())

    return max_distance(start)


test_data = read_data(test_input_file)
assert longest_hike(test_data) == 94


data = read_data(input_file)
print(longest_hike(data))
