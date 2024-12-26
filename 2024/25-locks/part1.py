from functools import reduce
from itertools import product, starmap
from operator import add
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> tuple[list[list[int]], list[list[int]]]:
    keys = []
    locks = []
    with open(file_name, 'r') as f:
        for block in f.read().split('\n\n'):
            b = block.split('\n')
            if b[0][0] == '#':  # lock
                lock = []
                for pin in range(len(b[0])):
                    for h in range(len(b)):
                        if b[h][pin] == '.':
                            lock.append(h - 1)
                            break
                locks.append(lock)
            else:  # key
                key = []
                for pin in range(len(b[0])):
                    for h in range(len(b)):
                        if b[h][pin] == '#':
                            key.append(6 - h)
                            break
                keys.append(key)
    return keys, locks


def matching_keys(keys: list[list[int]], locks: list[list[int]]) -> int:
    return reduce(add, map(lambda kl: all(map(lambda p: p <= 5, starmap(add, zip(*kl)))), product(keys, locks)))


assert matching_keys(*read_data(test_input_files[0])) == 3

data = read_data(input_file)
print(matching_keys(*data))
