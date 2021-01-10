#!/usr/bin/env python
from itertools import permutations

for a, b, c, d, e in permutations((2, 3, 5, 7, 9), 5):
    if a + b * c ** 2 + d ** 3 - e == 399:
        print(a, b, c, d, e)
