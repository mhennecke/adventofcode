import os
import numpy as np

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> np.ndarray:
    with open(file_name, 'r') as f:
        data = np.fromstring(f.read().replace('~', ',').replace('\n', ','), sep=',', dtype=int).reshape(-1, 2, 3)
    return data


def sum_falling(snapshot: np.ndarray) -> tuple[int, int]:
    max_x = max(snapshot[:, 1, 0])
    max_y = max(snapshot[:, 1, 1])
    nr_bricks = snapshot.shape[0]

    zbuffer = np.zeros((max_x + 1, max_y + 1), dtype=int)
    zbricks = -np.ones((max_x + 1, max_y + 1), dtype=int)

    # sort by z
    snapshot = snapshot[np.argsort(snapshot[:, -1, -1])]

    # scan through z and build graph of brick supports
    support_graph = {i: set() for i in range(-1, nr_bricks)}
    support_graph_inv = {i: set() for i in range(-1, nr_bricks)}
    for i in range(nr_bricks):
        brick = snapshot[i]
        brick_h = brick[1, 2] - brick[0, 2] + 1
        brick_xy = brick[:, 0:2]
        xy_slice = np.s_[brick_xy[0, 0]:(brick_xy[1, 0] + 1), brick_xy[0, 1]:(brick_xy[1, 1] + 1)]

        max_in_slice = np.max(zbuffer[xy_slice])

        for supporting_brick in set(zbricks[xy_slice][zbuffer[xy_slice] == max_in_slice]):
            support_graph[supporting_brick].add(i)
            support_graph_inv[i].add(supporting_brick)
        zbricks[xy_slice] = i
        zbuffer[xy_slice] = max_in_slice + brick_h

    # brick can be removed if supported bricks are supported by at least one other brick
    safely_disintegable_bricks = []
    for i in range(nr_bricks):
        if all([len(support_graph_inv[k]) > 1 for k in support_graph[i]]):
            safely_disintegable_bricks.append(i)

    # post order traversal, find set of supported bricks per brick
    visited = [False for i in range(-1, nr_bricks)]
    supported_bricks = {i: set() for i in range(-1, nr_bricks)}

    def postorder(node) -> set:
        n = set()
        if visited[node]:
            n = supported_bricks[node]
        else:
            for k in support_graph[node]:
                n.add(k)
                r = postorder(k)
                n.update(r)
            supported_bricks[node] = n
            visited[node] = True
        return n

    postorder(-1)

    sum_falling = 0
    for i in range(nr_bricks):
        falling_bricks_i = supported_bricks[i].copy()
        for s in supported_bricks[i]:
            # not already removed?
            if s in falling_bricks_i:
                has_other_support = len(support_graph_inv[s] - supported_bricks[i].union({i})) > 0
                if has_other_support:
                    # remove s as well as all other bricks supported by s
                    falling_bricks_i -= supported_bricks[s].union({s})
        sum_falling += len(falling_bricks_i)

    return len(safely_disintegable_bricks), sum_falling


test_data = read_data(test_input_file)
assert sum_falling(test_data) == (5, 7)

data = read_data(input_file)
print(sum_falling(data))
