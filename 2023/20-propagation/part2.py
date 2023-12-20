import os
import math
import numpy as np

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')
test_input2_file = os.path.join(script_dir, 'test.input2')


def read_data(file_name: str) -> dict[str, tuple[str, list[str]]]:
    modules = {}
    with open(file_name, 'r') as f:
        for m in f.read().splitlines():
            ty = m[0]
            name = m[1:m.find(' ')] if ty != 'b' else 'broadcaster'
            targets = m[m.find('>') + 2:].split(', ')
            modules[name] = (ty, targets)

    return modules


def min_button_low(modules: dict[str, tuple[str, list[str]]], at_module: str) -> int:
    buttons_pressed = 0
    total_pulses = [0, 0]

    module_state = {m_name: False if m_op[0] in ['%', 'b'] else {} for m_name, m_op in modules.items()}
    # init conjunction modules
    for m in module_state:
        # check all targets if input for conjunction modules
        _, targets = modules[m]
        for t in targets:
            if t in modules and modules[t][0] == '&':
                module_state[t][m] = False

    m_prev = next(item[0] for item in modules.items() if at_module in item[1][1])
    prev_min_button_presses = {m: math.inf for m in module_state[m_prev]}

    while True:
        buttons_pressed += 1
        total_pulses[0] += 1

        queue = []
        queue = [('broadcaster', target, False) for target in modules['broadcaster'][1]]
        while queue:
            source_state, cur_state, pulse = queue.pop(0)
            total_pulses[pulse] += 1
            op, targets = modules.get(cur_state, ('_', []))
            # print(f'{source_state} -{"high" if pulse else "low"}-> {cur_state}')
            if op == '%' and not pulse:
                # received low pulse -> flip
                module_state[cur_state] = not module_state[cur_state]
                # If it was off, it turns on and sends a high pulse.
                # If it was on, it turns off and sends a low pulse.
                for t in targets:
                    queue.append((cur_state, t, module_state[cur_state]))
            elif op == '&':
                module_state[cur_state][source_state] = pulse
                send_high_pulse = not all(module_state[cur_state].values())
                for t in targets:
                    queue.append((cur_state, t, send_high_pulse))
            elif op == 'broadcaster':
                module_state[cur_state] = pulse
                for t in targets:
                    queue.append((cur_state, t, module_state[cur_state]))
            elif op == '_':
                module_state[cur_state] = pulse
                if cur_state == at_module and not pulse:
                    return buttons_pressed

            for m_name, m_state in module_state[m_prev].items():
                if m_state:
                    prev_min_button_presses[m_name] = min(buttons_pressed, prev_min_button_presses[m_name])
            if all([p < math.inf for p in prev_min_button_presses.values()]):
                return np.lcm.reduce(list(prev_min_button_presses.values()))


test_data = read_data(test_input2_file)
assert min_button_low(test_data, 'output') == 1

data = read_data(input_file)
print(min_button_low(data, 'rx'))
