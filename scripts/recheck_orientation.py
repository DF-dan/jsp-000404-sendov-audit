#!/usr/bin/env python3
"""Recheck one SAT model's triangle orientation pattern at another t."""

import argparse
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import z3

from model_audit import q, rat_string


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=Path, required=True)
    ap.add_argument("--t", type=Fraction, required=True)
    a = ap.parse_args()
    old = json.loads(a.model.read_text(encoding="utf-8"))
    n = int(old["n"])
    vals = {tuple(map(int, k.split(","))): Fraction(v)
            for k, v in old["assignment"].items()}
    x = {e: z3.Real(f"x_{e[0]}_{e[1]}") for e in combinations(range(n), 2)}
    tq = q(a.t)
    s = z3.SolverFor("QF_LRA")
    for e in x:
        s.add(0 <= x[e], x[e] < tq)
    for i, j, k in combinations(range(n), 3):
        aa, bb, cc = vals[i, j], vals[i, k], vals[j, k]
        A, B, C = x[i, j], x[i, k], x[j, k]
        if aa <= bb <= cc and cc-aa >= 1:
            s.add(A <= B, B <= C, 1 <= C-A,
                  B-A <= tq-1, C-B <= tq-1)
        elif cc <= bb <= aa and aa-cc >= 1:
            s.add(C <= B, B <= A, 1 <= A-C,
                  A-B <= tq-1, B-C <= tq-1)
        else:
            raise RuntimeError(f"source is not a model at {(i,j,k)}")
    result = s.check()
    print(json.dumps({
        "source": str(a.model), "n": n,
        "new_t": f"{a.t.numerator}/{a.t.denominator}",
        "fixed_orientation_result": str(result),
        "reason_unknown": s.reason_unknown() if result == z3.unknown else None,
    }, indent=2))


if __name__ == "__main__":
    main()
