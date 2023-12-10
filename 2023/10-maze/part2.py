import os


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input2_file = os.path.join(script_dir, 'test.input2')
test_input3_file = os.path.join(script_dir, 'test.input3')
test_input4_file = os.path.join(script_dir, 'test.input4')


def read_data(file_name: str) -> list[str]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if not data:
                data.append('.' * (2 + len(line)))
            data.append(f'.{line}.')
        else:
            data.append('.' * (2 + len(line)))
    return data


def print_maze(maze: list[str]):
    for line in maze:
        line = line.replace('|', '│')
        line = line.replace('-', '─')
        line = line.replace('L', '└')
        line = line.replace('J', '┘')
        line = line.replace('7', '┐')
        line = line.replace('F', '┌')
        print(line)


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


def str_replace_index(s: str, i: int, c: str) -> str:
    return s[:i] + c + s[i + 1:]


def nr_enclosed(maze: list[str]) -> int:
    v_start = start(maze)
    loop = dfs(v_start, maze)

    # maze with loop only
    maze_l = ['.' * len(maze[0])] * len(maze)
    for j, i in loop:
        v_t = maze[j][i]
        if v_t == 'S':
            v_t = start_to_pipe((j, i), maze)
        maze_l[j] = str_replace_index(maze_l[j], i, v_t)

    # double-sized maze
    maze_expanded = []
    for line in maze_l:
        line_expanded_i = ''
        for v_t in line:
            line_expanded_i += v_t
            line_expanded_i += '-' if v_t in '-FL' else '.'
        maze_expanded.append(line_expanded_i)
        maze_expanded.append(''.join(['|' if v_t in '|F7' else '.' for v_t in line_expanded_i]))

    # flood-fill
    s = (0, 0)
    stack = [s]
    while stack:
        j, i = stack.pop()
        maze_expanded[j] = str_replace_index(maze_expanded[j], i, 'O')
        for j_adj, i_adj in [(j + 1, i), (j - 1, i), (j, i + 1), (j, i - 1)]:
            if 0 > j_adj or j_adj >= len(maze_expanded):
                continue
            if 0 > i_adj or i_adj >= len(maze_expanded[0]):
                continue
            if maze_expanded[j_adj][i_adj] == '.':
                stack.append((j_adj, i_adj))

    # dots from shrinked maze
    dots = sum([sum([1 if v_t == '.' else 0 for v_t in line[::2]]) for line in maze_expanded[::2]])
    return dots


test_maze = read_data(test_input2_file)
assert nr_enclosed(test_maze) == 4

test_maze = read_data(test_input3_file)
assert nr_enclosed(test_maze) == 8

test_maze = read_data(test_input4_file)
assert nr_enclosed(test_maze) == 10

maze = read_data(input_file)
print(nr_enclosed(maze))
