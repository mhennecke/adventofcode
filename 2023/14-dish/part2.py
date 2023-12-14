import os
import numpy as np

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> np.ndarray:
    data = []
    with open(file_name, 'r') as f:
        data = f.read().splitlines()
    return np.array([[c for c in row] for row in data])


def spin_cycle(platform: np.ndarray):
    # tilt four times to 'north' but rotate platform every time
    for _ in range(4):
        for c in range(platform.shape[1]):
            r_insert = 0
            for r in range(platform.shape[0]):
                state = platform[r, c]
                if state == '#':
                    r_insert = r + 1
                elif state == 'O':
                    if r_insert < r:
                        platform[r_insert, c] = 'O'
                        platform[r, c] = '.'
                    r_insert += 1
        platform = np.rot90(platform, 3)
    pass


def total_load(platform: np.ndarray, cycles: int = 1000000000):
    seen = dict()  # ordered keys!
    weights = np.arange(platform.shape[0], 0, -1)
    for cycle in range(cycles):
        spin_cycle(platform)
        h = hash(platform.tobytes())
        load = np.sum(weights @ (platform == 'O'))
        if h in seen:
            seq_start = list(seen.keys()).index(h)  # start of repeating sequence is iteration where h was seen the first time
            return list(seen.values())[seq_start + (cycles - seq_start - 1) % (cycle - seq_start)]  # use cycle length to get offset
        else:
            seen[h] = load


test_data = read_data(test_input_file)
assert total_load(test_data) == 64

data = read_data(input_file)
print(total_load(data))
