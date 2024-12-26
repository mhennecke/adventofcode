import os
from operator import xor, and_, or_
from typing import Callable

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_files = [os.path.join(script_dir, f'test.input{i}') for i in range(2)]


def read_data(file_name: str) -> tuple[int, int, dict[str, tuple[str, str, Callable]]]:
    gates = {}
    x = 0
    y = 0
    ops = {'AND': and_, 'OR': or_, 'XOR': xor}
    with open(file_name, 'r') as f:
        for line in f:
            match line.split():
                case [var, value]:
                    bit = int(var[1:3])
                    if var.startswith('x'):
                        x |= int(value) << bit
                    elif var.startswith('y'):
                        y |= int(value) << bit
                case [a, op, b, '->', c]:
                    a, b = sorted([a, b])
                    gates[c] = (a, b, ops[op])
    return gates, x, y


class Circuit():
    def __init__(self, gates: dict[str, tuple[str, str, Callable]]) -> None:
        self.gates = gates
        self._x = None
        self._y = None
        self._bits = int(max(gates.keys())[1:]) + 1

    def _to_input(self, a: str) -> int:
        if a.startswith('x'):
            a = (self._x >> int(a[1:3])) & 1
        elif a.startswith('y'):
            a = (self._y >> int(a[1:3])) & 1
        return a

    def _eval(self, a: str, b: str, op: Callable) -> int:
        a = self._to_input(a)
        b = self._to_input(b)
        return op(
            self._eval(*self.gates[a]) if a in self.gates else a,
            self._eval(*self.gates[b]) if b in self.gates else b
        )

    @property
    def bits(self) -> int:
        return self._bits

    def z(self, x: int, y: int) -> int:
        self._x, self._y = x, y
        out = 0
        for b in range(self.bits):
            out |= self._eval(*self.gates[f'z{b:02}']) << b
        self._x, self._y = None, None
        return out

    def gate_to_output(self, a: str, b: str, op: Callable) -> str | None:
        out = [wire for wire, (a_, b_, op_) in self.gates.items() if set([a, b]) == set([a_, b_]) and op == op_]
        return out[0] if len(out) == 1 else None

    def swap(self, a: str, b: str) -> None:
        self.gates[a], self.gates[b] = self.gates[b], self.gates[a]


def fix_ripple_carry_adder(circuit: Circuit) -> list[str]:
    swapped = []
    c = None
    for i in range(circuit.bits - 1):
        x = f'x{i:02}'
        y = f'y{i:02}'
        z = f'z{i:02}'

        xxy = circuit.gate_to_output(x, y, xor)
        xay = circuit.gate_to_output(x, y, and_)
        if i == 0:
            # half adder
            c = xay
        else:
            # full adder
            s = circuit.gate_to_output(xxy, c, xor)
            if not s:  # required gate not found
                w = set(circuit.gates[z][:2]) ^ {xxy, c}  # find swapped wires
                circuit.swap(*w)
                swapped += w
            elif s != z:  # 'sum' output is not connected to z bit
                circuit.swap(s, z)
                swapped += [s, z]
            xxy = circuit.gate_to_output(x, y, xor)
            xay = circuit.gate_to_output(x, y, and_)
            c = circuit.gate_to_output(xxy, c, and_)
            c = circuit.gate_to_output(c, xay, or_)
    return sorted(swapped)


gates, x, y = read_data(test_input_files[0])
circuit = Circuit(gates)
assert circuit.z(x, y) == 4

gates, x, y = read_data(test_input_files[1])
circuit = Circuit(gates)
assert circuit.z(x, y) == 2024

gates, x, y = read_data(input_file)
circuit = Circuit(gates)
print(circuit.z(x, y))

# 45 bit ripple carry adder
# 1 half adder, 44 full adders, 1 carry out
# full adder: 2 XOR, 2 AND, 1 OR
# half adder: 1 XOR, 1 AND
print(','.join(fix_ripple_carry_adder(circuit)))
