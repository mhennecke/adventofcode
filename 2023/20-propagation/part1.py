import os
import math

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


def mul_total_low_high(modules: dict[str, tuple[str, list[str]]]) -> int:
    target_button_presses = 1000
    buttons_pressed = 0
    total_pulses = [0, 0]

    module_state = {m_name: False if m_op[0] in ['%', 'b'] else {} for m_name, m_op in modules.items()}
    for m in module_state:
        # check all targets if input for conjunction modules
        _, targets = modules[m]
        for t in targets:
            if t in modules and modules[t][0] == '&':
                module_state[t][m] = False

    while buttons_pressed < target_button_presses:
        buttons_pressed += 1
        total_pulses[0] += 1

        queue = []
        queue = [('broadcaster', target, False) for target in modules['broadcaster'][1]]
        while queue:
            source_state, cur_state, pulse = queue.pop(0)
            total_pulses[pulse] += 1
            op, targets = modules.get(cur_state, ('_', []))
            print(f'{source_state} -{"high" if pulse else "low"}-> {cur_state}')
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

        cycle_complete = all([not all([s] if isinstance(s, bool) else s.values()) for s in module_state.values()])
        if cycle_complete:
            remaining_button_presses = target_button_presses - buttons_pressed
            # advance as far as possible
            total_pulses = [p * (1 + remaining_button_presses // buttons_pressed) for p in total_pulses]
            buttons_pressed += buttons_pressed * remaining_button_presses // buttons_pressed

    return math.prod(total_pulses)


test_data = read_data(test_input_file)
assert mul_total_low_high(test_data) == 32000000
test_data = read_data(test_input2_file)
assert mul_total_low_high(test_data) == 11687500

data = read_data(input_file)
print(mul_total_low_high(data))
