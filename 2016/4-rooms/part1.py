import os
from itertools import islice, groupby
from operator import itemgetter

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            data.append((line[:-12], int(line[-11:-8]), line[-7:-2]))
    return data


def sum_sector_ids(rooms: list[tuple]) -> int:
    sum_ids = 0
    for name, id, checksum in rooms:
        occurences = [(k, len(list(g))) for k, g in groupby(sorted(name.replace('-', '')))]
        top5_chars = str.join('', [c for c, _ in islice(sorted(occurences, key=itemgetter(1), reverse=True), 5)])

        sum_ids += id * (checksum == top5_chars)
    return sum_ids

assert sum_sector_ids(read_data(test_input_file)) == 1514

print(sum_sector_ids(read_data(input_file)))
