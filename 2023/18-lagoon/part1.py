import os
import numpy as np

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[str, list[int]]]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            d, s, c = line.strip().split(' ')
            data.append((d, int(s), c[1:-1]))
    return data


def print_lagoon(lagoon: np.ndarray):
    for row in lagoon:
        print(''.join(row))


def lagoon_extent(dig_map: list[tuple[str, int, str]]) -> tuple[int, int, int, int]:
    max_w = 0
    max_h = 0
    min_w = 0
    min_h = 0
    x = 0
    y = 0
    for d, s, _ in dig_map:
        if d == 'R':
            x += s
        if d == 'L':
            x -= s
        if d == 'D':
            y += s
        if d == 'U':
            y -= s
        max_w = max(x, max_w)
        min_w = min(x, min_w)
        max_h = max(y, max_h)
        min_h = min(y, min_h)
    return max_w - min_w + 1, max_h - min_h + 1, min_w, min_h


def lagoon_size(dig_map: list[tuple[str, int, str]]) -> int:
    directions = {
        'R': np.array([1, 0]),
        'U': np.array([0, -1]),
        'L': np.array([-1, 0]),
        'D': np.array([0, 1]),
    }
    width, height, x_offset, y_offset = lagoon_extent(dig_map)

    lagoon = np.empty(shape=(height, width), dtype=str)
    lagoon.fill('.')
    p = np.array([-x_offset, -y_offset])
    for d, s, _ in dig_map:
        p_ = p + s * directions[d]
        if d == 'R':
            lagoon[p[1], p[0]:(p_[0] + 1)] = '#'
        elif d == 'L':
            lagoon[p[1], p_[0]:(p[0] + 1)] = '#'
        elif d == 'D':
            lagoon[p[1]:(p_[1] + 1), p[0]] = '#'
        elif d == 'U':
            lagoon[p_[1]:(p[1] + 1), p[0]] = '#'
        p = p_
    # print_lagoon(lagoon)

    # flood-fill
    s = (-x_offset + 1, -y_offset + 1)
    stack = [s]
    while stack:
        x, y = stack.pop()
        lagoon[y][x] = '#'
        for y_adj, x_adj in [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]:
            if 0 > y_adj or y_adj >= height:
                continue
            if 0 > x_adj or x_adj >= width:
                continue
            if lagoon[y_adj][x_adj] == '.':
                stack.append((x_adj, y_adj))

    # print_lagoon(lagoon)
    return np.sum(lagoon == '#')


test_data = read_data(test_input_file)
assert lagoon_size(test_data) == 62


data = read_data(input_file)
print(lagoon_size(data))
