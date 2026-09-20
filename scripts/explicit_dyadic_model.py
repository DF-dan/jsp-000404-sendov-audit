#!/usr/bin/env python3
"""Construct and exactly verify the standard dyadic direction Model.

For binary ordered labels, theta(i,j) is the most-significant differing bit,
numbered from 0.  Restricting the 2^m construction to the first N labels gives
a Model N m.  This supplies a transparent exact-SAT witness for N=21,t=5.
"""

import argparse
import json
from itertools import combinations
from pathlib import Path

import z3

from model_audit import q, triangle


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if not (0 <= a.n <= 2 ** a.m):
        raise SystemExit("need 0 <= N <= 2^m")
    vals = {}
    s = z3.SolverFor("QF_LRA")
    t = q(a.m)
    x = {}
    for i, j in combinations(range(a.n), 2):
        # bit_length-1 numbers from the least-significant side; reverse it so
        # the most-significant differing bit has label 0.
        v = a.m - (i ^ j).bit_length()
        vals[f"{i},{j}"] = f"{v}/1"
        x[i, j] = z3.Real(f"x_{i}_{j}")
        s.add(x[i, j] == v, 0 <= x[i, j], x[i, j] < t)
    for i, j, k in combinations(range(a.n), 3):
        s.add(triangle(t, x[i, j], x[i, k], x[j, k]))
    result = s.check()
    payload = {
        "construction": "first differing bit on lexicographically ordered m-bit words",
        "n": a.n,
        "t": f"{a.m}/1",
        "result": str(result),
        "edge_variables": len(vals),
        "triangle_constraints": a.n * (a.n - 1) * (a.n - 2) // 6,
        "assignment": vals,
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k != "assignment"}, indent=2))


if __name__ == "__main__":
    main()
