import os
import itertools

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[tuple[int, int, int]]:
    with open(file_name, 'r') as f:
        return [tuple(map(int, line.split(','))) for line in f.read().splitlines()]


def last_boxes_x(points: list[tuple[int, int, int]]) -> tuple[int, int]:
    pairs = itertools.combinations(range(len(points)), 2)
    distances = sorted([[sum((a - b)**2 for a, b in zip(points[p1], points[p2])), p1, p2] for p1, p2 in pairs])
    circuits = [set([i]) for i in range(len(points))]

    for _, p1, p2 in distances:
        circuits[p1].update(circuits[p2])
        for p in circuits[p2]:
            circuits[p] = circuits[p1]
        if len({id(c): len(c) for c in circuits}.values()) == 1:
            return points[p1][0] * points[p2][0]


assert last_boxes_x(read_data(test_input_files[0])) == 25272

data = read_data(input_file)
print(last_boxes_x(data))
