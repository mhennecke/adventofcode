import os
import networkx as nx

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def read_data(file_name: str) -> nx.Graph:
    with open(file_name, 'r') as f:
        data = nx.parse_adjlist(f.readlines(), delimiter='-', nodetype=str)
    return data


def lan_party_password(G: nx.Graph) -> str:
    max_clique = ','.join(sorted(max(nx.find_cliques(G), key=len)))
    return max_clique


assert lan_party_password(read_data(test_input_files[0])) == 'co,de,ka,ta'

data = read_data(input_file)
print(lan_party_password(data))
