import os

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


def is_on_topo(topo: list[str], y: int, x: int) -> bool:
    return 0 <= y < len(topo) and 0 <= x < len(topo[y])


def trail(topo: list[str], y: int, x: int) -> int:
    c = int(topo[y][x])
    # print_topo(topo, y, x, visited, tops)
    trails = 0
    for d in directions:
        y_n, x_n = y + d[0], x + d[1]
        if not is_on_topo(topo, y_n, x_n):
            continue

        if int(topo[y_n][x_n]) == c + 1:
            if int(topo[y_n][x_n]) == 9:
                trails += 1
            else:
                trails += trail(topo, y_n, x_n)
    return trails


def sum_scores(topo: list[str]) -> int:
    score = 0
    for y in range(len(topo)):
        for x in range(len(topo[y])):
            if topo[y][x] == '0':
                score += trail(topo, y, x)

    return score


assert sum_scores(read_data(test_input_file)) == 81

d = sum_scores(read_data(input_file))
print(d)
