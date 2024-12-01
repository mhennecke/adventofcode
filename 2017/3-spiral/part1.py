import itertools


def manhattan_distance(square: int) -> int:
    def odd_square(i: int) -> int:
        return (i * 2 + 1)**2

    ring = next(ring for ring in itertools.count(1) if odd_square(ring) >= square)
    corners = [odd_square(ring) - 2 * ring * i for i in range(4)]
    dist = map(lambda c: abs(c - square), corners)
    return 2 * ring - min(dist)


assert manhattan_distance(1) == 0
assert manhattan_distance(12) == 3
assert manhattan_distance(23) == 2
assert manhattan_distance(1024) == 31

print(manhattan_distance(312051))
