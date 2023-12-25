import os
import networkx as nx
from operator import mul
from functools import reduce

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> nx.Graph:
    with open(file_name, 'r') as f:
        data = nx.parse_adjlist(f.read().replace(':', '').splitlines(), nodetype=str)
    return data


def min_separator(G: nx.Graph) -> int:
    ec = nx.minimum_edge_cut(G)
    assert len(ec) == 3
    G.remove_edges_from(ec)
    return reduce(mul, map(len, nx.connected_components(G)), 1)


test_data = read_data(test_input_file)
assert min_separator(test_data) == 54


data = read_data(input_file)
print(min_separator(data))
