import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(2)]


def read_data(file_name: str) -> tuple[list[list[str]], str]:
    warehouse = []
    moves = ''
    with open(file_name, 'r') as f:
        for line in f:
            if line.startswith('#'):
                warehouse.append([c for c in line.strip()])
            elif line:
                moves += line.strip()
    return warehouse, moves


adj = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, -1),
    'v': (0, 1),
}


def print_warehouse(warehouse: list[list[str]]):
    for line in warehouse:
        print(''.join(line))


def sum_gps_coordinates(warehouse: list[list[str]], moves: str) -> int:
    x, y = next((x, y) for y, line in enumerate(warehouse) for x, c in enumerate(line) if c == '@')
    for i, m in enumerate(moves):
        dx, dy = adj[m]
        xn, yn = x + dx, y + dy
        if warehouse[yn][xn] == '.':
            warehouse[y][x] = '.'
            x, y = x + dx, y + dy
            warehouse[y][x] = '@'
        elif warehouse[yn][xn] == '#':
            pass
        else:
            while warehouse[yn][xn] == 'O':
                xn, yn = xn + dx, yn + dy
            if warehouse[yn][xn] == '.':
                warehouse[yn][xn] = 'O'
                warehouse[y][x] = '.'
                y, x = y + dy, x + dx
                warehouse[y][x] = '@'
        # print(f'After Move {i + 1}: {m}')
        # print_warehouse(warehouse)

    gps = 0
    for y, _ in enumerate(warehouse):
        for x, c in enumerate(warehouse[y]):
            if c == 'O':
                gps += x + 100 * y

    return gps


assert sum_gps_coordinates(*read_data(test_input_files[0])) == 2028
assert sum_gps_coordinates(*read_data(test_input_files[1])) == 10092

d = sum_gps_coordinates(*read_data(input_file))
print(d)
