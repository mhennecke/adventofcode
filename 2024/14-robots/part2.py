import os
from parse import parse

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[complex, complex]]:
    robots = []
    with open(file_name, 'r') as f:
        for line in f:
            p_x, p_y, v_x, v_y = parse('p={:d},{:d} v={:d},{:d}', line.strip())
            robots.append((p_x + p_y * 1j, v_x + v_y * 1j))
    return robots


def safety_factor(robots: list[tuple[complex, complex]], height: int = 103, width: int = 101) -> int:
    # observed pattern every 101 iterations
    # manual check showed that pattern emerges if all positions
    # contain no more than 1 robot
    s = 95
    s_jump = 101
    while True:
        p_robots = [[0] * width for _ in range(height)]
        for r in robots:
            p, v = r
            t = (p + v * s)
            x, y = (int(t.real % width), int(t.imag % height)) 
            p_robots[y][x] += 1

        if all(all(cell <= 1 for cell in row) for row in p_robots):
            for y in range(height):
                for x in range(width):
                    print(p_robots[y][x] or ' ', end='')
                print()

            return s
        s += s_jump


d = safety_factor(read_data(input_file))
print(d)
