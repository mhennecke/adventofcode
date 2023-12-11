import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[str]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            data.append(line)
    return data


def pairwise_distances(galaxy: list[str], expansion: int) -> list[int]:
    empty_rows = [j for j, row in enumerate(galaxy) if '#' not in row]
    empty_columns = [i for i in range(len(galaxy[0])) if '#' not in [galaxy[j][i] for j in range(len(galaxy))]]

    stars = []
    for j in range(len(galaxy)):
        for i in range(len(galaxy[0])):
            if galaxy[j][i] == '#':
                stars.append((j, i))

    d = []
    for m in range(len(stars)):
        ds_mn = []
        for n in range(m + 1, len(stars)):
            s_m = stars[m]
            s_n = stars[n]
            nr_empty_rows = sum([r in empty_rows for r in range(min(s_n[0], s_m[0]) + 1, max(s_n[0], s_m[0]))])
            nr_empty_columns = sum([c in empty_columns for c in range(min(s_n[1], s_m[1]) + 1, max(s_n[1], s_m[1]))])
            d_mn = abs(s_m[0] - s_n[0]) + abs(s_m[1] - s_n[1]) + (nr_empty_rows + nr_empty_columns) * (expansion - 1)
            ds_mn.append(d_mn)
        else:
            d.append(ds_mn)
    return d


def sum_shortest_distances(galaxy: list[str], expansion: int = 2) -> int:
    return sum([sum(d) for d in pairwise_distances(galaxy, expansion)])


test_galaxy = read_data(test_input_file)
assert sum_shortest_distances(test_galaxy, 2) == 374
assert sum_shortest_distances(test_galaxy, 10) == 1030
assert sum_shortest_distances(test_galaxy, 100) == 8410


galaxy = read_data(input_file)
print(sum_shortest_distances(galaxy, 10**6))
