import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[str]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if not data:
                data.append('.' * len(line))
            data.append(f'.{line}.')
        else:
            data.append('.' * len(line))
    return data


def start_to_pipe(v_start: tuple[int, int], maze: list[str]) -> str:
    j, i = v_start
    assert maze[j][i] == 'S'

    directions = {
        # (n, w, s, e)
        (0, 0, 1, 1): 'F',
        (0, 1, 0, 1): '-',
        (1, 0, 0, 1): 'L',
        (0, 1, 1, 0): '7',
        (1, 0, 1, 0): '|',
        (1, 1, 0, 0): 'J',
    }

    to_dir = [
        maze[j - 1][i] in '|7F',  # north
        maze[j][i - 1] in '-FL',  # west
        maze[j + 1][i] in '|LJ',  # south
        maze[j][i + 1] in '-J7',  # east
    ]
    assert sum(to_dir) == 2

    return directions[tuple(to_dir)]


def adj(v: tuple[int, int], maze: list[str]) -> list[tuple[int, int]]:
    j, i = v
    mapping = {
        '|': [(j - 1, i), (j + 1, i)],
        '-': [(j, i + 1), (j, i - 1)],
        'L': [(j - 1, i), (j, i + 1)],
        'J': [(j - 1, i), (j, i - 1)],
        '7': [(j + 1, i), (j, i - 1)],
        'F': [(j + 1, i), (j, i + 1)],
        '.': [],
    }
    v_t = maze[j][i]
    if v_t == 'S':
        v_t = start_to_pipe(v, maze)
    return mapping[v_t]


def start(maze: list[str]) -> tuple[int, int]:
    for j, line in enumerate(maze):
        for i, s in enumerate(line):
            if s == 'S':
                return (j, i)


def dfs(v_start: tuple[int, int], maze: list[str]) -> list[tuple[int, int]]:
    visited = set()

    stack = []
    stack.append(v_start)

    v = v_start
    path = []
    while stack:
        v_prev = v
        v = stack.pop()
        if (v not in visited):
            path.append(v)
            visited.add(v)
            for v_adj in adj(v, maze):
                if v_adj != v_prev:
                    if v_adj == v_start and path:
                        return path
                    if v_adj not in visited:
                        stack.append(v_adj)


def farthest(maze: list[str]) -> int:
    v_start = start(maze)
    loop = dfs(v_start, maze)
    return len(loop) // 2


test_maze = read_data(test_input_file)
assert farthest(test_maze) == 8


maze = read_data(input_file)
print(farthest(maze))
