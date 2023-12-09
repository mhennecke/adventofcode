import os
from itertools import pairwise

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[list[int]]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            data.append([int(m) for m in line.strip().split(' ')])
    return data


def oasis_extrapolate_front(measurement: list[int]) -> int:
    triag = [measurement]

    for i in range(len(measurement) - 1):
        triag.append([m2 - m1 for m1, m2 in pairwise(triag[-1])])
        if all([t == 0 for t in triag[-1]]):
            break
    e = 0
    for i in range(len(triag) - 2, -1, -1):
        e = triag[i][0] - e
    return e


def sum_oasis_extrapolation_front(measuremenmts: list[list[int]]):
    return sum(map(oasis_extrapolate_front, measuremenmts))


test_data = read_data(test_input_file)
assert oasis_extrapolate_front(test_data[0]) == -3
assert oasis_extrapolate_front(test_data[1]) == 0
assert oasis_extrapolate_front(test_data[2]) == 5
assert sum_oasis_extrapolation_front(test_data) == 2


data = read_data(input_file)
print(sum_oasis_extrapolation_front(data))
