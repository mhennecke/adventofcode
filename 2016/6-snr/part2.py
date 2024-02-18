import os
from itertools import groupby
from operator import itemgetter

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[str]:
    return open(file_name, 'r').read().splitlines()


def error_corrected_message(message: list[str]) -> str:
    transposed = zip(*message)
    occurrences = map(lambda c_i: [(k, len(list(g))) for k, g in groupby(sorted(c_i))], transposed)
    message = map(lambda c_i: sorted(c_i, key=itemgetter(1), reverse=False)[0][0], occurrences)
    return str.join('', message)
    

assert error_corrected_message(read_data(test_input_file)) == 'advent'

print(error_corrected_message(read_data(input_file)))
