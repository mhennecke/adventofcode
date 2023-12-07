import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> tuple[list[int], dict[list[tuple[int, int, int]]]]:
    seeds = []
    maps = {}
    current_map = ''
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if not seeds:
                assert line.startswith('seeds: ')
                seeds = list(map(int, line.split(' ')[1:]))
            elif line.endswith(' map:'):
                current_map = line.split(' ')[0]
                maps[current_map] = []
            elif line == '':
                current_map = ''
            else:
                maps[current_map].append(list(map(int, line.split(' '))))

    return (seeds, maps)


def map_source_to_destination(source: int, mapping: list[tuple[int, int, int]]) -> int:
    destination = source
    for m in mapping:
        mapped_to_range = source - m[1]
        if mapped_to_range >= 0 and mapped_to_range < m[2]:
            destination = m[0] + source - m[1]
            break

    return destination


def map_seed_to_location(seed: int, maps: dict[list[tuple[int, int, int]]]) -> int:
    for mapping in maps.values():
        # assume ordered dict
        seed = map_source_to_destination(seed, mapping)
    return seed


def min_map_seed_to_location(seeds: list[int], maps: dict[list[tuple[int, int, int]]]) -> int:
    return min(map(lambda seed: map_seed_to_location(seed, maps), seeds))


test_seeds, test_map = read_data(test_input_file)
assert map_source_to_destination(98, test_map['seed-to-soil']) == 50
assert map_source_to_destination(99, test_map['seed-to-soil']) == 51
assert map_source_to_destination(53, test_map['seed-to-soil']) == 55
assert map_seed_to_location(test_seeds[0], test_map) == 82
assert min_map_seed_to_location(test_seeds, test_map) == 35

seeds, maps = read_data(input_file)
print(min_map_seed_to_location(seeds, maps))
