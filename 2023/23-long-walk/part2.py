import os
import numpy as np

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
    G = {start: {}}

    visited = set()
    stack = [(start, start, 0)]
    while stack:
        pos, parent, distance = stack.pop()
        if all(pos == end):
            G[parent][pos] = distance
            continue

        new_positions = np.array(pos) + directions
        is_junction = sum(trails[*(new_positions).T] != '#') > 2
        if is_junction:
            if pos == parent:
                continue
            # new node
            G[parent][pos] = distance
            G[pos] = G.get(pos, {})
            parent = pos
            distance = 0

        if pos not in visited:
            for new_pos in new_positions:
                new_pos = tuple(new_pos)
                try:
                    if trails[*new_pos] in downhill + ['.']:
                        stack.append((new_pos, parent, distance + 1))
                except IndexError:
                    pass
        visited.add(pos)

    # G to undirected
    Gu = {v: {} for v in G}
    Gu[tuple(end)] = {}
    for v, edges in G.items():
        Gu[v].update(edges)
        for v_, w in edges.items():
            if v_ != tuple(end):
                Gu[v_][v] = w

    visited = set()
    distances = {v: 0 for v in Gu}

    # longest path to all nodes in undirected cyclic graph
    def longest_path(node, curr_d):
        if node in visited:
            return
        visited.add(node)
        distances[node] = max(distances[node], curr_d)
        for v, w in Gu[node].items():
            longest_path(v, curr_d + w)
        else:
            visited.remove(node)

    # all longest distances from start
    longest_path(start, 0)

    return distances[tuple(end)]


test_data = read_data(test_input_file)
assert longest_hike(test_data) == 154


data = read_data(input_file)
print(longest_hike(data))
