import os
import math

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> dict[str, list]:
    workflows = {}
    with open(file_name, 'r') as f:
        for w in f.read().split('\n\n')[0].splitlines():
            w_name = w[:w.find('{')]
            w_steps = w[w.find('{') + 1:-1]
            workflows[w_name] = [w_step.split(':') for w_step in w_steps.split(',')]

    return workflows


def all_possible_distinct_combinations(workflows: dict[str, str]) -> int:
    total_combinations = 0
    stack = [('in', {category: [1, 4000] for category in 'xmas'})]
    while stack:
        state, ranges = stack.pop()
        if state == 'R':
            continue
        if state == 'A':
            total_combinations += math.prod([r_u - r_l + 1 for r_l, r_u in ranges.values()])
        else:
            for step in workflows[state]:
                if len(step) == 1:
                    stack.append((step[0], ranges))
                else:
                    condition, target_state = step
                    r = dict(ranges)
                    if '<' in condition:
                        c, value = condition.split('<')
                        r[c] = [r[c][0], int(value) - 1]
                        ranges[c] = [int(value), ranges[c][1]]
                    elif '>' in condition:
                        c, value = condition.split('>')
                        r[c] = [int(value) + 1, r[c][1]]
                        ranges[c] = [ranges[c][0], int(value)]
                    stack.append((target_state, r))

    return total_combinations


test_data = read_data(test_input_file)
assert all_possible_distinct_combinations(test_data) == 167409079868000


data = read_data(input_file)
print(all_possible_distinct_combinations(data))
