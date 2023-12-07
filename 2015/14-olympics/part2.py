import os
import parse
from collections import defaultdict

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


def points(d: dict[tuple[int, int, int]], travel_duration: int) -> dict[int]:
    # points
    p = defaultdict(lambda: 0)
    # 0: flying, 1: resting
    state = defaultdict(lambda: 0)
    distance = defaultdict(lambda: 0)
    # initial state: flying
    t_keep_states = {r: v[1] for r, v in d.items()}
    for t in range(1, travel_duration + 1):
        for r, t_keep_state in t_keep_states.items():
            # travel
            if state[r] == 0:
                distance[r] += d[r][0]
            if t_keep_state > 1:
                t_keep_states[r] -= 1
            else:
                # switch state
                state[r] = (state[r] + 1) % 2
                # take new fly (_, fly, _) or rest (_, _, rest) duration based on state
                t_keep_states[r] = d[r][state[r] + 1]

        # points for furthest distance
        max_d = max(distance.values())
        for r in d.keys():
            if distance[r] == max_d:
                p[r] += 1

        print(f'{t:>4d} distance: {dict(distance)}, state: {dict(state)}, keep_states: {t_keep_states}, points: {dict(p)}')
        pass

    return p


test_data = {
    'C': (14, 10, 127),
    'D': (16, 11, 162)
}
# assert points(test_data, 1000) == {'C': 312, 'D': 689}


data = read_data(input_file)
p = points(data, 2503)
print(dict(p))
print(max(p.values()))
