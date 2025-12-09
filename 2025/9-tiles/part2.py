import math
import os
import itertools


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[tuple[int, int]]:
    with open(file_name, 'r') as f:
        return [tuple(map(int, line.split(','))) for line in f.read().splitlines()]


def cross_product(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def segments_cross(p1, p2, p3, p4):
    return (cross_product(p1, p2, p3) * cross_product(p1, p2, p4) < 0 and
            cross_product(p3, p4, p1) * cross_product(p3, p4, p2) < 0)


def is_point_on_segment(p, a, b, eps=1e-9):
    # Check if point p lies exactly on the segment (a) -> (b).

    # Check collinearity using cross product
    if abs(cross_product(p, a, b)) > eps:
        return False

    # Check if within bounding box
    dot = (p[0] - a[0]) * (p[0] - b[0]) + (p[1] - a[1]) * (p[1] - b[1])
    return dot <= eps


def winding_number(p, polygon):
    assert polygon[0] == polygon[-1]
    wn = 0
    # for i in range(len(polygon) - 1):
    for a, b in itertools.pairwise(polygon):
        # Check if point is exactly on an edge
        if is_point_on_segment(p, a, b):
            return None  # On boundary
        # Upward crossing
        if a[1] <= p[1] < b[1]:
            if (b[0] - a[0]) * (p[1] - a[1]) - (p[0] - a[0]) * (b[1] - a[1]) > 0:
                wn += 1
        # Downward crossing
        elif b[1] <= p[1] < a[1]:
            if (b[0] - a[0]) * (p[1] - a[1]) - (p[0] - a[0]) * (b[1] - a[1]) < 0:
                wn -= 1
    return wn


def largest_tile(tiles: list[tuple[int, int]]) -> int:
    tiles = tiles + [tiles[0]]
    pairs = itertools.combinations(tiles, 2)
    areas = sorted((math.prod([abs(a-b)+1 for a, b in list(zip(p1, p2))]), p1, p2) for p1, p2 in pairs)
    segment_lengths = sorted(([p1, p2] for p1, p2 in itertools.pairwise(tiles + [tiles[0]])), key=lambda p: sum(abs(a-b) for a, b in zip(*p)), reverse=True)

    for area, p1, p2 in areas[::-1]:
        p3 = [p1[0], p2[1]]
        p4 = [p2[0], p1[1]]

        if all(wn is None or wn != 0 for wn in [winding_number(p3, tiles), winding_number(p4, tiles)]):
            is_valid = True
            for seg_p1, seg_p2 in segment_lengths:
                if any(map(lambda p: segments_cross(*p, seg_p1, seg_p2), itertools.pairwise([p1, p3, p2, p4, p1]))):
                    is_valid = False
                    break

            if is_valid:
                return area
    return None


assert largest_tile(read_data(test_input_files[0])) == 24

data = read_data(input_file)
print(largest_tile(data))
