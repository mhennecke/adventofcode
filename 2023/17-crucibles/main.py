import os
import heapq
import math
from copy import deepcopy

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[list[int]]:
    data = []
    with open(file_name, 'r') as f:
        data = [[int(b) for b in line] for line in f.read().splitlines()]
    return data


def print_steps(loss_map: list[list[str]], steps: list[tuple[int, int]]):
    m = deepcopy(loss_map)
    for x, y in steps:
        m[y][x] = '-'
    for row in m:
        print(''.join(map(str, row)))


def min_heat_loss(loss_map: list[list[str]], min_consecutive_steps: int = 4,  max_consecutive_steps: int = 10) -> int:
    # directions: r=0, u=1, l=2, d=3
    # x, y: pos
    # d: from direction
    # c: nr straight steps
    start_data = (0, 0, -1, 0)
    prio_q = []
    heapq.heappush(prio_q, (0, (*start_data, [(0, 0)])))

    width, height = (len(loss_map[0]), len(loss_map))
    min_loss = math.inf
    seen = set()
    seen.add(start_data)

    x_ = lambda d: (1 - d) * (d % 2 == 0)
    y_ = lambda d: (d - 2) * (d % 2 == 1)

    while prio_q:
        loss, data = heapq.heappop(prio_q)
        x, y, d, c, steps = data
        # print(x, y, loss, d, c)
        # print_steps(loss_map, steps)
        # print()
        if x == width - 1 and y == height - 1:
            # reached target
            min_loss = min(min_loss, loss)
            # print_steps(loss_map, steps)
            break

        for d_new in range(4):
            if (d_new + 2) % 4 != d:
                x_new = x + x_(d_new)
                y_new = y + y_(d_new)
                steps_new = steps + [(x_new, y_new)]
                c_new = c + 1 if d_new == d else 0

                if (x_new < 0 or x_new >= width or y_new < 0 or y_new >= height):
                    continue
                if c + 1 < min_consecutive_steps and d != d_new and d >= 0:
                    continue
                if c_new >= max_consecutive_steps:
                    continue

                if x_new == width - 1 and y_new == height - 1:
                    pass
                loss_new = loss + loss_map[y_new][x_new]
                if loss_new > min_loss:
                    continue

                data_new = (x_new, y_new, d_new, c_new)
                if data_new not in seen:
                    seen.add(data_new)
                    heapq.heappush(prio_q, (loss_new, (x_new, y_new, d_new, c_new, steps_new)))

    return min_loss


test_data = read_data(test_input_file)
assert min_heat_loss(test_data, min_consecutive_steps=0, max_consecutive_steps=3) == 102
assert min_heat_loss(test_data, min_consecutive_steps=4, max_consecutive_steps=10) == 94


data = read_data(input_file)
print(min_heat_loss(data, min_consecutive_steps=0, max_consecutive_steps=3))
print(min_heat_loss(data, min_consecutive_steps=4, max_consecutive_steps=10))
