import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')

locs = [(0, 0)] * 2

visited = set()
visited.add((0, 0))

with open(input_file, 'r') as f:
    line = f.readline()
    for i, direction in enumerate(line.strip()):
        if direction == '^':
            locs[i % 2] = (locs[i % 2][0], locs[i % 2][1] + 1)
        elif direction == 'v':
            locs[i % 2] = (locs[i % 2][0], locs[i % 2][1] - 1)
        elif direction == '>':
            locs[i % 2] = (locs[i % 2][0] + 1, locs[i % 2][1])
        elif direction == '<':
            locs[i % 2] = (locs[i % 2][0] - 1, locs[i % 2][1])

        visited.add(locs[i % 2])

print(len(visited))
