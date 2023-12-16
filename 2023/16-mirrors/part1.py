import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> list[tuple[str, list[int]]]:
    data = []
    with open(file_name, 'r') as f:
        data = f.read().splitlines()
    return data


def print_mirrors(mirrors: list[list[str]], seen: list[list[list[int]]]):
    for y_j, row in enumerate(seen):
        p = ['#' if any(m) else mirrors[y_j][x_i] for x_i, m in enumerate(row)]
        print(''.join(p))
    print('---')


def energy(mirrors: list[list[str]], start_beam: tuple[int, int, int] = (0, 0, 0)) -> int:
    # beam directions: r=0, u=1, l=2, d=3
    beam_stack = [start_beam]
    width, height = (len(mirrors[0]), len(mirrors))
    seen = [[[0, 0, 0, 0] for _ in range(width)] for _ in range(height)]
    x_ = lambda d: (1 - d) * (d % 2 == 0)
    y_ = lambda d: (d - 2) * (d % 2 == 1)
    while beam_stack:
        x, y, d = beam_stack.pop()
        if (x < 0 or x >= width or y < 0 or y >= height) or seen[y][x][d]:
            continue

        seen[y][x][d] = 1
        mirror = mirrors[y][x]
        up_or_down = d % 2 == 1
        left_or_right = not up_or_down
        if mirror == '.' or (mirror == '-' and left_or_right) or (mirror == '|' and up_or_down):
            beam_stack.append((x + x_(d), y + y_(d), d))
        elif mirror == '-' and up_or_down:
            # split
            beam_stack.append((x + 1, y, 0))
            beam_stack.append((x - 1, y, 2))
        elif mirror == '|' and left_or_right:
            # split
            beam_stack.append((x, y + 1, 3))
            beam_stack.append((x, y - 1, 1))
        elif mirror == '/':
            # reflect: d=0->1, d=1->0, d=2->3, d=3->2
            d_ = (1 - d) % 4
            beam_stack.append((x + x_(d_), y + y_(d_), d_))
        elif mirror == '\\':
            # reflect: d=0->3, d=1->2, d=2->1, d=3->0
            d_ = (3 - d) % 4
            beam_stack.append((x + x_(d_), y + y_(d_), d_))
        else:
            raise AttributeError()
        # print_mirrors(mirrors, seen)

    return sum([sum([any(m) for m in row]) for row in seen])


test_data = read_data(test_input_file)
assert energy(test_data) == 46


data = read_data(input_file)
print(energy(data))
