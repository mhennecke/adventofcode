import os
import re

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


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


def matching_nrs(card: tuple[set[int], set[int]]) -> int:
    nrs_win = card[0]
    nrs_have = card[1]
    nrs_both = nrs_win.intersection(nrs_have)
    return nrs_both


def scratchcards_total(cards: list[tuple[set[int], set[int]]]) -> list[int]:
    cards_total = [1] * len(cards)
    for i, card in enumerate(cards):
        m = len(matching_nrs(card))
        for k in range(1, m + 1):
            if i + k > len(cards_total):
                break
            cards_total[i + k] += cards_total[i]

    return cards_total


test_cards = read_data(test_input_file)
assert sum(scratchcards_total(test_cards)) == 30

cards = read_data(input_file)
print(sum(scratchcards_total(cards)))
