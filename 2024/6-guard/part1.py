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


def guard_positions(lab: list[str]) -> int:
    for y in range(len(lab)):
        if lab[y].find('^') != -1:
            x = lab[y].find('^')
            break

    visited = set()
    d = 0
    try:
        while True:
            visited.add((y, x))
            y_n = y + directions[d][0]
            x_n = x + directions[d][1]
            if x_n < 0 or y_n < 0:
                raise IndexError
            if lab[y_n][x_n] == '#':
                d = (d + 1) % 4
            else:
                visited.add((y_n, x_n))
                y, x = y_n, x_n
    except IndexError:
        pass

    return len(visited)


assert guard_positions(read_data(test_input_file)) == 41

d = guard_positions(read_data(input_file))
print(d)
