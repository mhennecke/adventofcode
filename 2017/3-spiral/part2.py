import itertools

grid = dict()
dir_spiral = [(0, 1), (-1, 0), (0, -1), (1, 0)]
dir_square = set(itertools.product([1, 0, -1], repeat=2))


def sum_square(x, y):
    return sum(grid.get((x + dx, y + dy), 0) for dx, dy in dir_square)


x, y = 0, 0
grid[(x, y)] = 1
for ring in itertools.count(1):
    x += 1
    grid[(x, y)] = sum_square(x, y)
    for i in range(4):
        dx, dy = dir_spiral[i]
        for _ in range(2 * ring - 1 if i == 0 else 2 * ring):
            x, y = x + dx, y + dy
            grid[(x, y)] = sum_square(x, y)
            if grid[(x, y)] > 312051:
                print(grid[(x, y)])
                exit()
