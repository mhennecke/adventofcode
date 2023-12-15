import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[str, list[int]]]:
    data = []
    with open(file_name, 'r') as f:
        data = f.read().splitlines()[0].split(',')
    return data


def seq_hash(sequence: str, seed: int = 0) -> int:
    h = seed
    for c in sequence:
        h = (h + ord(c)) * 17 % 256
    return h


def total_seq_hashes(sequences: list[str]) -> int:
    return sum(map(seq_hash, sequences))


assert seq_hash('HASH') == 52
test_data = read_data(test_input_file)
assert total_seq_hashes(test_data) == 1320


data = read_data(input_file)
print(total_seq_hashes(data))
