from itertools import chain
import math


def divisors(n):
    return set(chain.from_iterable((i, n // i) for i in range(1, int(math.sqrt(n))+1) if n % i == 0))


target_presents = 34000000
i = 1
while True:
    p_i = 10 * sum([d for d in divisors(i)])
    if p_i >= target_presents:
        break
    i += 1

print(i)
