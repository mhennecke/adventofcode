import os

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(2)]


def read_data(file_name: str) -> tuple[list[list[str]], str]:
    warehouse = []
    moves = ''
    with open(file_name, 'r') as f:
        for line in f:
            if line.startswith('#'):
                row = []
                for c in line.strip():
                    match c:
                        case '#':
                            row += ['#', '#']
                        case 'O':
                            row += ['[', ']']
                        case '.':
                            row += ['.', '.']
                        case '@':
                            row += ['@', '.']
                        case _:
                            raise ValueError(f'Invalid character: {c}')
                warehouse.append(row)
            elif line:
                moves += line.strip()
    return warehouse, moves


adj = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, -1),
    'v': (0, 1),
}


neighbour = {
    '[': (1, 0),
    ']': (-1, 0)
}


def print_warehouse(warehouse: list[list[str]]):
    for line in warehouse:
        print(''.join(line))


def box_other_side(warehouse: list[list[str]], x: int, y: int) -> tuple[int, int]:
    s = neighbour[warehouse[y][x]]
    return (x + s[0], y + s[1])


def sum_gps_coordinates(warehouse: list[list[str]], moves: str) -> int:
    x, y = next((x, y) for y, line in enumerate(warehouse) for x, c in enumerate(line) if c == '@')
    for i, m in enumerate(moves):
        dx, dy = adj[m]
        xn, yn = x + dx, y + dy

        def move_robot() -> tuple[int, int]:
            warehouse[y][x] = '.'
            warehouse[yn][xn] = '@'
            return xn, yn

        if warehouse[yn][xn] == '#':
            continue

        if warehouse[yn][xn] == '.':
            x, y = move_robot()
        elif m == '<' or m == '>':
            move_stack = []
            while warehouse[yn][xn] in '[]':
                move_stack.append(warehouse[yn][xn])
                xn, yn = xn + dx, yn + dy
            if warehouse[yn][xn] == '.':
                while move_stack:
                    warehouse[yn][xn] = move_stack.pop()
                    xn, yn = xn - dx, yn - dy
                x, y = move_robot()
        elif m == '^' or m == 'v':
            # box must be present
            assert warehouse[yn][xn] in '[]'
            move_stack = [set()]
            move_stack[-1].add((xn, yn))
            move_stack[-1].add(box_other_side(warehouse, xn, yn))
            free = []
            while True:
                blocked = [warehouse[ym + dy][xm + dx] == '#' for xm, ym in move_stack[-1]]
                if any(blocked):
                    break
                free = [warehouse[ym + dy][xm + dx] == '.' for xm, ym in move_stack[-1]]
                if all(free):
                    break
                # append all new boxes to move_stack
                boxes = set()
                for xm, ym in move_stack[-1]:
                    if warehouse[ym + dy][xm + dx] in '[]':
                        boxes.add((xm + dx, ym + dy))
                        boxes.add(box_other_side(warehouse, xm + dx, ym + dy))
                move_stack.append(boxes)

            if all(free or [False]):
                # move all boxes
                while move_stack:
                    for xm, ym in move_stack.pop():
                        warehouse[ym + dy][xm + dx] = warehouse[ym][xm]
                        warehouse[ym][xm] = '.'
                x, y = move_robot()

        # print(f'After Move {i + 1}: {m}')
        # print_warehouse(warehouse)

    gps = 0
    for y, _ in enumerate(warehouse):
        for x, c in enumerate(warehouse[y]):
            if c == '[':
                gps += x + 100 * y

    return gps


assert sum_gps_coordinates(*read_data(test_input_files[1])) == 9021

d = sum_gps_coordinates(*read_data(input_file))
print(d)
