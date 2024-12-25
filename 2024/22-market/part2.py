import os
from collections import defaultdict

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(2)]


def read_data(file_name: str) -> list[int]:
    with open(file_name, 'r') as f:
        return list(map(int, f.read().splitlines()))


def prng(s: int) -> int:
    PRUNE = (1 << 24) - 1
    s ^= (s << 6) & PRUNE
    s ^= (s >> 5)  # s gets smaller, no need to prune
    s ^= (s << 11) & PRUNE
    return s


def max_bananas(initial_secret_numbers: list[int], iterations: int) -> int:
    MASK = (1 << 5 * 4) - 1  # 4 price changes * 5 bits for each change (0 to 18)
    counts = defaultdict(int)
    for seed in initial_secret_numbers:
        sold = set()

        sequence = 0
        prev_price = seed % 10
        s = seed
        for i in range(iterations):
            s = prng(s)
            price = s % 10
            diff = price - prev_price + 9  # avoid negative numbers: 0-18, max 5 bits
            sequence = (sequence << 5 | diff) & MASK
            prev_price = price

            if i > 3 and sequence not in sold:
                sold.add(sequence)
                counts[sequence] += price
    return max(counts.values())


assert max_bananas(read_data(test_input_files[1]), 2000) == 23

c = max_bananas(read_data(input_file), 2000)
print(c)
