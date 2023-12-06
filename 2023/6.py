import os
from functools import reduce
import operator
import math

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, f'{os.path.basename(__file__).split(".")[0]}.input')
test_input_file = os.path.join(script_dir, f'{os.path.basename(__file__).split(".")[0]}.test.input')


def read_data(file_name: str) -> list[tuple[int, int]]:
    with open(file_name, 'r') as f:
        times = f.readline().strip().split('Time:')[1].split(' ')
        times = [int(t.strip()) for t in times if t]
        distances = f.readline().strip().split('Distance:')[1].split(' ')
        distances = [int(d.strip()) for d in distances if d]
    return list(zip(times, distances))


def nr_winning_races(race):
    t_race, d_to_beat = race

    t_l = math.ceil(0.5 * (t_race - math.sqrt(t_race**2 - 4 * d_to_beat)))
    t_u = math.floor(0.5 * (math.sqrt(t_race**2 - 4 * d_to_beat) + t_race))

    return t_u - t_l + 1


test_data = read_data(test_input_file)
assert nr_winning_races(test_data[0]) == 4
assert nr_winning_races(test_data[1]) == 8

test_data = read_data(input_file)
print(reduce(operator.mul, map(nr_winning_races, test_data), 1))
