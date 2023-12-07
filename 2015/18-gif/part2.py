import os
from itertools import pairwise


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test2.input{i}') for i in range(1, 7)]


def read_data(file_name: str) -> list[int]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            # add padding to simplify analysis
            if not data:
                data.append('.' * (len(line) + 2))
                data.append(f'.#{line[1:-1]}#.')
            else:
                data.append(f'.{line}.')

        data[-1] = f'.#{data[-1][2:-2]}#.'
        data.append('.' * (len(data[0])))
    return data


def new_light_state(grid, x, y) -> str:
    state = grid[y][x]
    neighbours = [
        (x - 1, y - 1),  # 1
        (x, y - 1),      # 2
        (x + 1, y - 1),  # 3
        (x + 1, y),      # 4
        (x + 1, y + 1),  # 5
        (x, y + 1),      # 6
        (x - 1, y + 1),  # 7
        (x - 1, y)       # 8
    ]

    neighbours_on = 0
    for n in neighbours:
        neighbours_on += 1 if grid[n[1]][n[0]] == '#' else 0

    if (x == 1 and y == 1) or \
            (x == 1 and y == len(grid) - 2) or\
            (x == len(grid[0]) - 2 and y == 1) or \
            (x == len(grid[0]) - 2 and y == len(grid) - 2):
        return '#'
    elif state == '#':
        if neighbours_on == 2 or neighbours_on == 3:
            return '#'
        else:
            return '.'
    else:
        if neighbours_on == 3:
            return '#'
        else:
            return '.'


def animate(grid) -> list[list[str]]:
    new_grid = ['.' * len(grid[0])] * len(grid)
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            new_grid[y] = new_grid[y][:x] + new_light_state(grid, x, y) + new_grid[y][x + 1:]
    return new_grid


test_data = [read_data(f) for f in test_input_files]
for d1, d2 in pairwise(test_data):
    a = animate(d1)
    assert a == d2

lights = read_data(input_file)
for i in range(100):
    lights = animate(lights)

nr_lights_on = sum([sum([light == '#' for light in row]) for row in lights])
print(lights)
print(nr_lights_on)
