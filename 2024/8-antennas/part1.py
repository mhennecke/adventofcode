import os
import itertools

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().splitlines()


directions = [
    (-1, 1),
    (1, 1),
    (1, -1),
    (-1, -1),
]


def pairs(a: tuple[int, int], antennas: set[tuple[int, int]], size: tuple[int, int]) -> set[tuple[int, int]]:
    y, x = a
    p = set()
    for d in directions:
        found = False
        for y_s in range(y, 0 if d[0] < 0 else size[0], d[0]):
            for x_s in range(x, 0 if d[1] < 0 else size[1], d[1]):
                if (y_s, x_s) in antennas:
                    p.add((a, (y_s, x_s)))
                    found = True
                    break
            if found:
                break
    return p


def is_on_roof(a: tuple[int, int], size: tuple[int, int]) -> bool:
    return 0 <= a[0] < size[0] and 0 <= a[1] < size[1]


def nr_antinodes(roof: list[str]) -> int:
    antennas = {}
    antinodes = set()
    size = (len(roof), len(roof[0]))
    for y, line in enumerate(roof):
        for x, c in enumerate(line):
            if c != '.':
                antennas.setdefault(c, set()).add((y, x))

    for positions in antennas.values():
        for p1, p2 in itertools.combinations(positions, 2):
            v_y, v_x = p2[0] - p1[0], p2[1] - p1[1]
            a_1 = (p1[0] - v_y, p1[1] - v_x)
            a_2 = (p2[0] + v_y, p2[1] + v_x)
            if is_on_roof(a_1, size):
                antinodes.add(a_1)
            if is_on_roof(a_2, size):
                antinodes.add(a_2)

    return len(antinodes)


assert nr_antinodes(read_data(test_input_file)) == 14

d = nr_antinodes(read_data(input_file))
print(d)
