import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, f'{os.path.basename(__file__).split(".")[0]}.input')
test_input_file = os.path.join(script_dir, f'{os.path.basename(__file__).split(".")[0]}.test.input')


def read_data(file_name: str) -> list[tuple[set[int], set[int]]]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            nrs = line.split(': ')[1].split(' | ')

            nrs_win = set(map(int, re.split(r'\s+', nrs[0].strip())))
            nrs_have = set(map(int, re.split(r'\s+', nrs[1].strip())))
            data.append((nrs_win, nrs_have))

    return data


def points_scratchcards(cards: list[tuple[set[int], set[int]]]) -> list[int]:
    points = []
    for card in cards:
        nrs_win = card[0]
        nrs_have = card[1]
        nrs_both = nrs_win.intersection(nrs_have)
        points.append(2**(len(nrs_both) - 1) if nrs_both else 0)
    return points


test_cards = read_data(test_input_file)
assert sum(points_scratchcards(test_cards)) == 13

cards = read_data(input_file)
print(sum(points_scratchcards(cards)))
