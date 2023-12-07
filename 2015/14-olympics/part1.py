import os
import parse

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')


def read_data(file_name: str) -> dict:
    format_string = '{:w} can fly {:d} km/s for {:d} seconds, but then must rest for {:d} seconds.'

    data = {}
    with open(file_name, 'r') as f:
        for line in f:
            reindeer, speed, fly_duration, rest_duration = parse.parse(format_string, line.strip())
            data[reindeer] = (speed, fly_duration, rest_duration)
    return data


def travelled(speed: int, fly_duration: int, rest_duration: int, travel_duration: int) -> int:
    v = [speed, 0]
    d_t = [fly_duration, rest_duration]
    mode = 0
    duration = 0
    distance = 0
    while duration + d_t[mode] <= travel_duration:
        distance += v[mode] * d_t[mode]
        duration += d_t[mode]
        mode = (mode + 1) % 2

    distance += v[mode] * (travel_duration - duration)
    return distance


assert travelled(14, 10, 127, 1000) == 1120
assert travelled(16, 11, 162, 1000) == 1056

data = read_data(input_file)
for name, d in data.items():
    print(f'{name}: {travelled(d[0], d[1], d[2], 2503)}')
