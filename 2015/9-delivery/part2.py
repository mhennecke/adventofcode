import os
import parse
import networkx as nx

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')

format_string = '{:w} to {:w} = {:d}'

cities = nx.Graph()
with open(input_file, 'r') as f:
    for line in f:
        from_city, to_city, distance = parse.parse(format_string, line.strip())
        cities.add_edge(from_city, to_city, weight=distance)

max_path_length = 0
max_path = []
path = []


def dfs(v, weight=0):
    global max_path_length, max_path, path

    path.append(v)

    for w in cities.nodes():
        if w not in path:
            v_w_weight = cities.edges[v, w]['weight']
            dfs(w, weight + v_w_weight)

        # visited all?
        if len(path) == len(cities.nodes()):
            path_length = nx.path_weight(cities, path, 'weight')
            if (path_length > max_path_length):
                print(f'longer path: {path}, {path_length}')
                max_path = path
                max_path_length = path_length

    path.remove(v)


for city in cities.nodes():
    dfs(city)
