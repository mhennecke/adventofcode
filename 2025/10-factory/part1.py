import os
from functools import reduce
from operator import or_
import networkx as nx


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(1)]


def button_to_int(button: str, length: int) -> int:
    wiring = button[1:-1].split(',')
    return reduce(or_, (1 << int(wire) for wire in wiring), 0)


def light_state_to_str(lights: int, length: int) -> str:
    return '[' + ''.join(['#', '.'][(lights & (1 << i) == 0)] for i in range(length)) + ']'


def read_data(file_name: str) -> list[tuple[str, list[str], str]]:
    def read_line(line: str) -> tuple[str, list[str], str]:
        fields = line.split(' ')
        return fields[0], fields[1:-1], fields[-1]

    with open(file_name, 'r') as f:
        return [read_line(line) for line in f.read().splitlines()]


def fewest_button_presses(machines: list[tuple[str, list[str], str]]) -> int:
    fewest = 0
    for target, buttons, _ in machines:
        G = nx.Graph()
        nr_lights = len(target[1:-1])
        nr_vertices = 1 << nr_lights

        for v_i in range(nr_vertices):
            for button in buttons:
                v = light_state_to_str(v_i, nr_lights)
                u = light_state_to_str(v_i ^ button_to_int(button, nr_lights), nr_lights)
                G.add_edge(v, u, wiring=button)
        path = nx.shortest_path(G, source=light_state_to_str(0, nr_lights), target=target)
        fewest += len(path) - 1
    return fewest


assert fewest_button_presses(read_data(test_input_files[0])) == 7

data = read_data(input_file)
print(fewest_button_presses(data))
