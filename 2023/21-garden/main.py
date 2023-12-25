import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> dict[complex, str]:
    data = {}
    with open(file_name, 'r') as f:
        for y, row in enumerate(f.read().splitlines()):
            for x, c in enumerate(row):
                if c in '.S':
                    data[x + y*1j] = c
    return data


def reached_plots(garden: dict[complex, str]) -> int:
    positions = {start for start in garden if garden[start] == 'S'}
    w = 131
    steps = 26501365
    tiles = []
    tile_mod = lambda x: complex(x.real % 131, x.imag % 131)
    for i in range(int(2.5 * 131) + 1):
        if i == 64:
            # part 1
            print(len(positions))
        if i % w == w // 2:
            tiles.append(len(positions))

        positions = {p + d for d in {1, -1, 1j, -1j}
                     for p in positions if tile_mod(p+d) in garden}

    # number of tiles is a quadratic function for multiples of garden width
    assert (steps - w // 2) % w == 0
    # tiles -> steps at 65, 65 + 131 and 65 + 2 * 131
    # f(0) = y0, f(1) = y1, f(2) = y2
    # f(x) = a * x^2 + b * x + c
    y0, y1, y2 = tiles
    a = 0.5 * y0 - y1 + 0.5 * y2
    b = - 1.5 * y0 + 2 * y1 - 0.5 * y2
    c = y0
    f = lambda x: a * x**2 + b * x + c
    return int(f((steps - w // 2) / w))


data = read_data(input_file)
print(reached_plots(data))
