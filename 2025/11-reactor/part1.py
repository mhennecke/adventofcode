import functools
import os
import networkx as nx


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> list[str]:
    with open(file_name, 'r') as f:
        return [line.replace(':', '') for line in f.read().splitlines()]


@functools.cache
def paths(G, s, t) -> int:
    if s == t:
        return 1
    total = 0
    for n in G[s]:
        total += paths(G, n, t)
    return total


def all_paths(adj_list: list[str]) -> int:
    G = nx.parse_adjlist(adj_list, delimiter=' ', create_using=nx.DiGraph, nodetype=str)
    return paths(G, 'you', 'out')


assert all_paths(read_data(test_input_files[0])) == 5

data = read_data(input_file)
print(all_paths(data))
