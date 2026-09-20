#!/usr/bin/env python3
"""Independent SMT audit of PR #100's SendovDirectionModel.Model.

The constraints below are a literal transcription of
  submissions/jsp-000404-five-point/lean434/SendovDirectionModel.lean
and SendovFiveDirections.Triangle.

This script is an exploratory checker only.  SAT means an abstract Model N t
exists; it does not mean that the assignment is realizable by planar points.
"""

from __future__ import annotations

import argparse
import json
import time
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import z3


def q(value: Fraction) -> z3.RatNumRef:
    return z3.Q(value.numerator, value.denominator)


def triangle(t, a, b, c):
    # Exact definition from SendovFiveDirections.lean.
    forward = z3.And(
        a <= b,
        b <= c,
        1 <= c - a,
        b - a <= t - 1,
        c - b <= t - 1,
    )
    reverse = z3.And(
        c <= b,
        b <= a,
        1 <= a - c,
        a - b <= t - 1,
        b - c <= t - 1,
    )
    return z3.Or(forward, reverse)


def rat_string(v) -> str:
    if z3.is_rational_value(v):
        return str(v.numerator_as_long()) + "/" + str(v.denominator_as_long())
    return str(v)


def audit(n: int, t_value: Fraction, timeout_ms: int, out_dir: Path):
    t = q(t_value)
    edges = list(combinations(range(n), 2))
    x = {ij: z3.Real(f"x_{ij[0]}_{ij[1]}") for ij in edges}
    # Deliberately use Z3's default portfolio.  In this disjunctive LRA
    # problem it is dramatically faster than SolverFor("QF_LRA") on the
    # known N=11,t=3.99 UNSAT calibration.
    s = z3.Solver()
    s.set(timeout=timeout_ms)

    for ij in edges:
        s.add(0 <= x[ij], x[ij] < t)
    for i, j, k in combinations(range(n), 3):
        s.add(triangle(t, x[i, j], x[i, k], x[j, k]))

    started = time.monotonic()
    result = s.check()
    elapsed = time.monotonic() - started
    payload = {
        "n": n,
        "t": f"{t_value.numerator}/{t_value.denominator}",
        "z3_version": z3.get_version_string(),
        "logic": "QF_LRA (default z3.Solver portfolio)",
        "edge_variables": len(edges),
        "triangle_disjunctions": n * (n - 1) * (n - 2) // 6,
        "timeout_ms": timeout_ms,
        "elapsed_seconds": elapsed,
        "result": str(result),
        "reason_unknown": s.reason_unknown() if result == z3.unknown else None,
    }

    if result == z3.sat:
        model = s.model()
        assignment = {f"{i},{j}": rat_string(model.eval(x[i, j], model_completion=True))
                      for i, j in edges}
        payload["assignment"] = assignment
        # Recheck the exact rational assignment with a fresh solver.  This guards
        # against mistakes when serializing algebraic values.
        verify = z3.Solver()
        for ij in edges:
            verify.add(0 <= x[ij], x[ij] < t)
            verify.add(x[ij] == model.eval(x[ij], model_completion=True))
        for i, j, k in combinations(range(n), 3):
            verify.add(triangle(t, x[i, j], x[i, k], x[j, k]))
        payload["exact_assignment_recheck"] = str(verify.check())

    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"model-N{n}-t{t_value.numerator}_{t_value.denominator}.json"
    (out_dir / stem).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k != "assignment"}, indent=2))
    return 0 if result != z3.unknown else 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--t", type=Fraction, required=True,
                        help="exact rational, e.g. 9/2")
    parser.add_argument("--timeout-ms", type=int, default=300000)
    parser.add_argument("--out-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    raise SystemExit(audit(args.n, args.t, args.timeout_ms, args.out_dir))


if __name__ == "__main__":
    main()
