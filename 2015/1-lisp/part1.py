import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')

floor = 0

with open(input_file, 'r') as f:
    data = f.read()
    for (i, c) in enumerate(data):
        if c == '(':
            floor += 1
        elif c == ')':
            floor -= 1

print(floor)
