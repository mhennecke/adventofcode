import os
import math

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> tuple[list[tuple[int, int]], dict[list[tuple[int, int, int]]]]:
    maps = {}
    current_map = ''
    seed_pairs = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if not seed_pairs:
                assert line.startswith('seeds: ')
                seeds = list(map(int, line.split(' ')[1:]))
                seed_pairs = []
                for i in range(0, len(seeds), 2):
                    seed_pairs.append((seeds[i], seeds[i + 1] + seeds[i]))
            elif line.endswith(' map:'):
                current_map = line.split(' ')[0]
                maps[current_map] = []
            elif line == '':
                current_map = ''
            else:
                maps[current_map].append(list(map(int, line.split(' '))))

    return (seed_pairs, maps)


def map_source_ranges_to_destination_ranges(source_ranges: list[tuple[int, int]], mapping: dict[list[tuple[int, int, int]]]) -> list[tuple[int, int]]:

    results = []
    for m in mapping.values():
        while source_ranges:
            source_range_start, source_range_end = source_ranges.pop()
            for target_start, m_start, r in m:
                m_end = m_start + r
                offset = target_start - m_start
                if m_end <= source_range_start or source_range_end <= m_start:
                    # completely outside
                    continue
                if source_range_start < m_start:
                    # partly in mapping range (left), add left part
                    source_ranges.append((source_range_start, m_start))
                    source_range_start = m_start
                if m_end < source_range_end:
                    # partly in mapping range (right), add right part
                    source_ranges.append((m_end, source_range_end))
                    source_range_end = m_end
                results.append((source_range_start + offset, source_range_end + offset))
                break
            else:
                # always add the remaining range
                results.append((source_range_start, source_range_end))
        source_ranges = results
        results = []
    return source_ranges


def map_seed_ranges_to_min_location(seed_ranges: list[tuple[int, int]], maps: dict[list[tuple[int, int, int]]]) -> int:
    min_seed = math.inf

    for i, seed_range in enumerate(seed_ranges):
        locations = map_source_ranges_to_destination_ranges([seed_range], maps)
        min_m = min(locations, key=lambda r: r[0])
        min_seed = min(min_m[0], min_seed)

    return min_seed


test_seed_ranges, test_map = read_data(test_input_file)
assert map_seed_ranges_to_min_location(test_seed_ranges, test_map) == 46

seed_ranges, maps = read_data(input_file)
print(map_seed_ranges_to_min_location(seed_ranges, maps))
