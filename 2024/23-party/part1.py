import os
import networkx as nx

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> nx.Graph:
    with open(file_name, 'r') as f:
        data = nx.parse_adjlist(f.readlines(), delimiter='-', nodetype=str)
    return data


def interconnected_computers(G: nx.Graph) -> int:
    triangles = [clique for clique in nx.enumerate_all_cliques(G) if len(clique) == 3]
    return sum([any(map(lambda v: v.startswith('t'), triangle)) for triangle in triangles])


assert interconnected_computers(read_data(test_input_files[0])) == 7

data = read_data(input_file)
print(interconnected_computers(data))
