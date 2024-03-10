import os
import re
from collections import defaultdict
from operator import mul
from functools import reduce

script_dir = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(script_dir, 'input')
test_input_file = os.path.join(script_dir, 'test.input')


def read_data(file_name: str) -> tuple[dict, dict]:
    pattern_value = re.compile(r"value (\d+) goes to bot (\d+)")
    pattern_bot = re.compile(r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)")

    values = dict()
    bots = dict()

    with open(file_name, 'r') as f:
        for line in f:
            match_value = pattern_value.match(line)
            match_bot = pattern_bot.match(line)

            if match_value:
                value, bot_id = map(int, match_value.groups())
                values[value] = bot_id
            elif match_bot:
                bot_id, low_type, low_id, high_type, high_id = match_bot.groups()
                low_id = int(low_id)
                high_id = int(high_id)
                low_id = -(low_id + 1) if low_type == 'output' else low_id
                high_id = -(high_id + 1) if high_type == 'output' else high_id
                bots[int(bot_id)] = [low_id, high_id]

    return values, bots


def outputs(values, bot_instructions):
    bot_values = defaultdict(list)
    for v, b in values.items():
        bot_values[b].append(v)

    full_bots = True
    while full_bots:
        full_bots = [b for b, v in bot_values.items() if len(v) == 2]
        for b in full_bots:
            low_bot, high_bot = bot_instructions[b]
            low, high = sorted(bot_values[b])
            bot_values[low_bot].append(low)
            bot_values[high_bot].append(high)
            bot_values[b] = []
    return [bot_values[b][0] for b in sorted(bot_values.keys(), reverse=True) if b < 0]


# What do you get if you multiply together the values of one chip in each of outputs 0, 1, and 2?
values, bot_instructions = read_data(input_file)
print(reduce(mul, outputs(values, bot_instructions)[0:3]))
