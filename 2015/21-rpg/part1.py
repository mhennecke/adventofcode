from itertools import combinations
import math

weapons = {
    'Dagger': [8, 4, 0],
    'Shortsword': [10, 5, 0],
    'Warhammer': [25, 6, 0],
    'Longsword': [40, 7, 0],
    'Greataxe': [74, 8, 0],
}
armor = {
    'No Armor': [0, 0, 0],
    'Leather': [13, 0, 1],
    'Chainmail': [31, 0, 2],
    'Splintmail': [53, 0, 3],
    'Bandedmail': [75, 0, 4],
    'Platemail': [102, 0, 5],
}
rings = {
    'Damage +1': [25, 1, 0],
    'Damage +2': [50, 2, 0],
    'Damage +3': [100, 3, 0],
    'Defense +1': [20, 0, 1],
    'Defense +2': [40, 0, 2],
    'Defense +3': [80, 0, 3],
}

boss_hit_points = 104
boss_damage = 8
boss_armor = 1


def game(h1: int, d1: int, a1: int, h2: int, d2: int, a2: int) -> int:
    while True:
        h2 -= max(1, d1 - a2)
        if h2 <= 0:
            return 1
        h1 -= max(1, d2 - a1)
        if h1 <= 0:
            return 2


assert game(8, 5, 5, 12, 7, 2) == 1

ring_combos = list(combinations(rings.values(), 1)) + list(combinations(rings.values(), 2))

min_cost = math.inf
for w in weapons.values():
    for a in armor.values():
        for r_combo in ring_combos:
            cost = w[0] + a[0] + sum([r[0] for r in r_combo])
            d1 = w[1] + a[1] + sum([r[1] for r in r_combo])
            a1 = w[2] + a[2] + sum([r[2] for r in r_combo])
            if game(100, d1, a1, boss_hit_points, boss_damage, boss_armor) == 1:
                min_cost = min(min_cost, cost)

print(min_cost)
