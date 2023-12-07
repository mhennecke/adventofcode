import os
import numpy as np
import parse

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')

lights = np.zeros((1000, 1000), dtype=np.int8)

cmd_format = '{} {:d},{:d} through {:d},{:d}'


def action(command):
    act, x1, y1, x2, y2 = parse.parse(cmd_format, command)
    if act == 'toggle':
        lights[x1:(x2+1), y1:(y2+1)] += 2
    elif act == 'turn on':
        lights[x1:(x2+1), y1:(y2+1)] += 1
    elif act == 'turn off':
        lights[x1:(x2+1), y1:(y2+1)] = np.maximum(lights[x1:(x2+1), y1:(y2+1)] - 1, 0)


lights = np.zeros((1000, 1000), dtype=np.int8)
action('turn on 0,0 through 999,999')
action('turn on 0,0 through 999,999')
assert np.sum(lights) == 2000000

lights = np.zeros((1000, 1000), dtype=np.int8)
action('turn on 0,0 through 999,999')
action('turn off 0,0 through 999,999')
action('turn off 0,0 through 999,999')
assert np.sum(lights) == 0

lights = np.zeros((1000, 1000), dtype=np.int8)
action('toggle 0,0 through 999,0')
assert np.sum(lights) == 2000

lights = np.zeros((1000, 1000), dtype=np.int8)
action('turn on 0,0 through 999,999')
action('turn on 499,499 through 500,500')
assert np.sum(lights) == 1000004


lights = np.zeros((1000, 1000), dtype=np.int8)
with open(input_file, 'r') as f:
    for line in f:
        action(line.strip())


print(np.sum(lights))
