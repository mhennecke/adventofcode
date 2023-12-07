import os
import parse

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')

ribbon = 0

with open(input_file, 'r') as f:
    for line in f:
        dim = parse.parse('{:d}x{:d}x{:d}', line.strip())
        dim_s = sorted(dim)
        ribbon += dim_s[0] * 2 + dim_s[1] * 2
        ribbon += dim[0] * dim[1] * dim[2]

print(ribbon)
