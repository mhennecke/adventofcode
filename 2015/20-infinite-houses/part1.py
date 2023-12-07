from itertools import chain
from math import sqrt


def divisors(n):
    return set(chain.from_iterable((i, n // i) for i in range(1, int(sqrt(n))+1) if n % i == 0))


def presents_at_house(house_nr: int) -> int:
    presents = 0
    for d in divisors(house_nr):
        presents += d * 10
    return presents


target_presents = 34000000

house_i = 1
while True:
    p_i = presents_at_house(house_i)
    print(f'house_i: {house_i}, p_i: {p_i}')
    if p_i >= target_presents:
        break
    house_i += 1
