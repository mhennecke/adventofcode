import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[int]:
    with open(file_name, 'r') as f:
        return list(map(int, f.read().splitlines()))


def prng(s: int) -> int:
    PRUNE = (1 << 24) - 1
    s ^= (s << 6) & PRUNE
    s ^= (s >> 5)  # s gets smaller, no need to prune
    s ^= (s << 11) & PRUNE
    return s


def secret_number(seed: int, iterations: int) -> int:
    s = seed
    for _ in range(iterations):
        s = prng(s)
    return s


def sum_secret_numbers(initial_secret_numbers: list[int], iterations: int) -> int:
    return sum(map(lambda seed: secret_number(seed, iterations), initial_secret_numbers))


t = [123]
for i in range(1, 11):
    t.append(prng(t[-1]))
assert t == [
    123,
    15887950,
    16495136,
    527345,
    704524,
    1553684,
    12683156,
    11100544,
    12249484,
    7753432,
    5908254,
]

assert sum_secret_numbers(read_data(test_input_files[0]), 2000) == 37327623

c = sum_secret_numbers(read_data(input_file), 2000)
print(c)
