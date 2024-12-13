from collections import defaultdict
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(5)]


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().splitlines()


adj = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
]


def is_in_garden(y: int, x: int, garden: list[str]) -> bool:
    return 0 <= y < len(garden) and 0 <= x < len(garden[y])


def total_price(garden: list[str]) -> int:
    fences = []
    for y, line in enumerate(garden):
        fences.append([0] * len(line))
        for x, c in enumerate(line):
            for d in adj:
                y_adj, x_adj = y + d[0], x + d[1]
                if is_in_garden(y_adj, x_adj, garden):
                    fences[y][x] += garden[y_adj][x_adj] != garden[y][x]
                else:
                    fences[y][x] += 1

    # flood fill
    visited = set()
    plants = defaultdict(set)

    for y in range(len(garden)):
        for x in range(len(garden[y])):
            if (y, x) in visited:
                continue

            # start new plant group
            g = len(plants)
            visited.add((y, x))
            plants[g].add((y, x))
            q = [(y, x)]
            while q:
                y_c, x_c = q.pop()
                for d in adj:
                    y_adj, x_adj = y_c + d[0], x_c + d[1]
                    if is_in_garden(y_adj, x_adj, garden) \
                            and (y_adj, x_adj) not in visited \
                            and garden[y_adj][x_adj] == garden[y][x]:
                        visited.add((y_adj, x_adj))
                        plants[g].add((y_adj, x_adj))
                        q.append((y_adj, x_adj))

    price = 0
    for p in plants.values():
        price += len(p) * sum([fences[y][x] for y, x in p])

    return price


assert total_price(read_data(test_input_files[0])) == 140
assert total_price(read_data(test_input_files[1])) == 772
assert total_price(read_data(test_input_files[2])) == 1930

d = total_price(read_data(input_file))
print(d)
