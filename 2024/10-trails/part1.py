import os
from termcolor import cprint

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().splitlines()


directions = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
]


def print_topo(topo: list[str], y_c: int, x_c: int, visited: set[tuple[int, int]], tops: set[tuple[int, int]]):
    for y, line in enumerate(topo):
        for x, c in enumerate(line):
            if x == x_c and y == y_c:
                cprint(c, 'blue', end='')
            elif (y, x) in visited:
                cprint(c, 'green', end='')
            elif (y, x) in tops:
                cprint(c, 'red', end='')
            else:
                print(c, end='')
        print()
    print()


def is_on_topo(topo: list[str], y: int, x: int) -> bool:
    return 0 <= y < len(topo) and 0 <= x < len(topo[y])


def trail(topo: list[str], y: int, x: int, visited: set[tuple[int, int]], tops: set[tuple[int, int]]):
    visited.add((y, x))
    c = int(topo[y][x])
    # print_topo(topo, y, x, visited, tops)
    for d in directions:
        y_n, x_n = y + d[0], x + d[1]
        if not is_on_topo(topo, y_n, x_n):
            continue
        elif (y_n, x_n) in visited:
            continue

        if int(topo[y_n][x_n]) == c + 1:
            if int(topo[y_n][x_n]) == 9:
                tops.add((y_n, x_n))
            else:
                trail(topo, y_n, x_n, visited, tops)


def sum_scores(topo: list[str]) -> int:
    score = 0
    for y in range(len(topo)):
        for x in range(len(topo[y])):
            if topo[y][x] == '0':
                tops = set()
                visited = set()
                trail(topo, y, x, visited, tops)
                score += len(tops)
                # print_topo(topo, y, x, visited, tops)
    return score


assert sum_scores(read_data(test_input_file)) == 36

d = sum_scores(read_data(input_file))
print(d)
