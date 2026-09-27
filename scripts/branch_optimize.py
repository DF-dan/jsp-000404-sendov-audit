"""Optimize the angle parameter for a fixed exact direction-model branch.

This is an exploratory LP.  Its branch is read from a verified rational
assignment; it does not establish a theorem about every possible branch.
"""

import json
import sys
from fractions import Fraction
from itertools import combinations

import numpy as np
from scipy.optimize import linprog


def main(path):
    data = json.load(open(path, encoding="utf-8"))
    n = data["n"]
    edges = list(combinations(range(n), 2))
    idx = {edge: p for p, edge in enumerate(edges)}
    old = {tuple(map(int, key.split(","))): Fraction(value)
           for key, value in data["assignment"].items()}
    t_idx = len(edges)
    rows, bounds, labels = [], [], []

    def add(terms, limit, label):
        row = np.zeros(t_idx + 1)
        for edge, coeff in terms:
            row[t_idx if edge is None else idx[edge]] += coeff
        rows.append(row)
        bounds.append(limit)
        labels.append(label)

    for edge in edges:
        add([(edge, 1), (None, -1)], 0, ("range", edge))  # x_ij <= t
    for i, j, k in combinations(range(n), 3):
        e1, e2, e3 = (i, j), (i, k), (j, k)
        if old[e1] <= old[e2] <= old[e3]:
            lo, mid, hi = e1, e2, e3
        elif old[e3] <= old[e2] <= old[e1]:
            lo, mid, hi = e3, e2, e1
        else:
            raise ValueError((i, j, k, "invalid triangle branch"))
        triple = (i, j, k)
        add([(lo, 1), (mid, -1)], 0, ("lo<=mid", triple))
        add([(mid, 1), (hi, -1)], 0, ("mid<=hi", triple))
        add([(hi, -1), (lo, 1)], -1, ("hi-lo>=1", triple))
        add([(mid, 1), (lo, -1), (None, -1)], -1, ("mid-lo<=t-1", triple))
        add([(hi, 1), (mid, -1), (None, -1)], -1, ("hi-mid<=t-1", triple))

    c = np.zeros(t_idx + 1)
    c[t_idx] = 1
    result = linprog(c, A_ub=np.array(rows), b_ub=np.array(bounds),
                     bounds=[(0, None)] * (t_idx + 1), method="highs")
    print({"status": result.message, "branch_min_t": result.fun,
           "original_t": data["t"], "n": n,
           "constraints": len(rows)})
    if result.success:
        support = [(str(Fraction(float(v)).limit_denominator(1000)), labels[i])
                   for i, v in enumerate(result.ineqlin.marginals)
                   if abs(v) > 1e-8]
        support += [(str(Fraction(float(v)).limit_denominator(1000)),
                     ("nonnegative", edges[i] if i < t_idx else "t"))
                    for i, v in enumerate(result.lower.marginals)
                    if abs(v) > 1e-8]
        print("dual_support:")
        for item in support:
            print(item)


if __name__ == "__main__":
    main(sys.argv[1])
