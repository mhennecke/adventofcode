import os
import parse

from functools import lru_cache


script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')

wires = {}


@lru_cache()
def get_value(wire):
    if wire.isnumeric():
        return int(wire)
    else:
        cmd = wires[wire]
        if cmd.startswith('NOT'):
            return ~get_value(cmd.split(' ')[1])
        else:
            if ' ' not in cmd:
                return get_value(cmd)
            else:
                l, op, r = parse.parse('{:w} {:w} {:w}', cmd)
                if op == 'AND':
                    return get_value(l) & get_value(r)
                elif op == 'OR':
                    return get_value(l) | get_value(r)
                elif op == 'LSHIFT':
                    return get_value(l) << get_value(r)
                elif op == 'RSHIFT':
                    return get_value(l) >> get_value(r)
                else:
                    print("Unknown op: ", op)
                    exit(1)


with open(input_file, 'r') as f:
    for line in f:
        line = line.strip()
        # b OR n -> o
        op, wire = line.split(' -> ')
        wires[wire] = op

print(get_value('a'))
