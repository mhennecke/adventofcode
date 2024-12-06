import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().splitlines()


directions = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


def add_obstacle(lab: list[str], obstacle: tuple[int, int]) -> list[str]:
    lab = lab.copy()
    y, x = obstacle
    lab[y] = lab[y][:x] + '#' + lab[y][x + 1:]
    return lab


def is_loop(lab: list[str]) -> bool:
    for y in range(len(lab)):
        if lab[y].find('^') != -1:
            x = lab[y].find('^')
            break

    visited = set()
    d = 0
    try:
        while True:
            visited.add((y, x, d))
            y_n = y + directions[d][0]
            x_n = x + directions[d][1]
            if x_n < 0 or y_n < 0:
                raise IndexError
            if (y_n, x_n, d) in visited:
                return True
            if lab[y_n][x_n] == '#':
                d = (d + 1) % 4
            else:
                visited.add((y_n, x_n, d))
                y, x = y_n, x_n
    except IndexError:
        return False


def loops(lab: list[str]) -> int:
    obstacles = 0
    for y in range(len(lab)):
        for x in range(len(lab[y])):
            if lab[y][x] == '.' and is_loop(add_obstacle(lab, (y, x))):
                obstacles += 1
    return obstacles


assert loops(read_data(test_input_file)) == 6

d = loops(read_data(input_file))
print(d)
