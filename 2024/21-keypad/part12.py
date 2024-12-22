import functools
import itertools
import os
from collections import defaultdict

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return f.read().splitlines()


class Keypad:
    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+
    # | 4 | 5 | 6 |
    # +---+---+---+
    # | 1 | 2 | 3 |
    # +---+---+---+
    #     | 0 | A |
    #     +---+---+
    keypad_numeric = [
        "789",
        "456",
        "123",
        "#0A"
    ]
    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+
    keypad_directional = [
        "#^A",
        "<v>"
    ]

    def __init__(self):
        self.keypads = [
            self.all_keypad_moves(self.keypad_directional),
            self.all_keypad_moves(self.keypad_numeric)
        ]

    def keypad_moves(self, start: str, end: str, key_pos: list[tuple[int, int]]) -> list[str]:
        if start == end or start == '#' or end == '#':
            return []

        dirsx = {
            1: '>',
            -1: '<',
        }
        dirsy = {
            1: 'v',
            -1: '^',
        }

        moves = []
        xh, yh = key_pos['#']
        x1, y1 = key_pos[start]
        x2, y2 = key_pos[end]
        dx, dy = x2 - x1, y2 - y1
        nx, ny = dx // abs(dx) if dx != 0 else 0, dy // abs(dy) if dy != 0 else 0

        if x1 == x2:
            moves.append(dirsy[ny] * abs(dy) + "A")
        elif y1 == y2:
            moves.append(dirsx[nx] * abs(dx) + "A")
        else:
            if x1 != xh or y2 != yh:
                moves.append(dirsy[ny] * abs(dy) + dirsx[nx] * abs(dx) + "A")
            if y1 != yh or x2 != xh:
                moves.append(dirsx[nx] * abs(dx) + dirsy[ny] * abs(dy) + "A")
        return moves

    def all_keypad_moves(self, keypad: list[str]) -> dict[tuple[str, str], str]:
        moves = defaultdict(list)
        key_pos = {keypad[y][x]: (x, y) for x, y in itertools.product(range(len(keypad[0])), range(len(keypad)))}
        for s, e in itertools.permutations(''.join(keypad).replace('#', ''), 2):
            moves[(s, e)] = self.keypad_moves(s, e, key_pos)
        return moves

    @functools.cache
    def indirect_keypad_moves(self, code: str, depth: int) -> int:
        # all possible combinations of moves
        moves = list(itertools.product(*[self.keypads[code[0].isnumeric()].get((a, b), 'A') for a, b in itertools.pairwise('A' + code)]))
        # print(f'{code=}, {depth=}, {moves=}')
        if depth == 0:
            return min(map(lambda m: sum(map(len, m)), moves))
        else:
            return min(map(lambda m: sum(map(lambda c: self.indirect_keypad_moves(c, depth - 1), m)), moves))

    def complexity(self, code: str, directional_keypads_robots: int) -> int:
        min_len = self.indirect_keypad_moves(code, directional_keypads_robots)
        return min_len * int(code[:-1])

    def sum_complexities(self, codes: list[str], directional_keypads_robots: int) -> int:
        r = list(map(lambda c: self.complexity(c, directional_keypads_robots), codes))
        return sum(r)


k = Keypad()
assert k.sum_complexities(read_data(test_input_files[0]), 2) == 126384

c = k.sum_complexities(read_data(input_file), 25)
print(c)
