import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')

location = (0, 0)
visited = set()
visited.add(location)

with open(input_file, 'r') as f:
    line = f.readline()
    for direction in line.strip():
        if direction == '^':
            location = (location[0], location[1] + 1)
        elif direction == 'v':
            location = (location[0], location[1] - 1)
        elif direction == '>':
            location = (location[0] + 1, location[1])
        elif direction == '<':
            location = (location[0] - 1, location[1])
        visited.add(location)

print(len(visited))
