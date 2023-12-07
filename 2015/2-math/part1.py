import os
import parse

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')

area = 0

with open(input_file, 'r') as f:
    for line in f:
        dim = parse.parse('{:d}x{:d}x{:d}', line.strip())
        area += 2 * dim[0] * dim[1] + 2 * dim[1] * dim[2] + 2 * dim[2] * dim[0]
        dim_s = sorted(dim)
        area += dim_s[0] * dim_s[1]

print(area)
