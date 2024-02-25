import os
import numpy as np

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[str, int, int]]:
    commands = []
    for l in open(file_name, 'r').read().splitlines():
        c = l.split()
        if c[0] == 'rect':
            commands.append((c[0][0], *map(int, c[1].split('x'))))
        else:
            commands.append((c[2][0], int(c[2][2:]), int(c[4])))
    return commands


def nr_pixels(commands: list[tuple[str, int, int]], width: int, height: int):
    display = np.empty((height, width), bool)

    for command, x, y in commands:    
        if command == 'r':
            display[:y,:x] = True
        elif command == 'x':
            display[:, x] = np.roll(display[:, x], y)
        elif command == 'y':
            display[x, :] = np.roll(display[x, :], y)
        [print(''.join(['#' if p else '.' for p in row])) for row in display]
        print()

    return sum(sum(display))


assert nr_pixels(read_data(test_input_file), 7, 3) == 6

print(nr_pixels(read_data(input_file), 50, 6))
