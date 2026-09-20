"""Numerically explore the weight profile used in Sendov 1995, Lemma 4.12.

For a centre p_i, directions to the other centres are unoriented lines, hence
angles live in RP^1, represented by [0, pi).  Consecutive cyclic gaps are
normalised by pi and sum to one.  With t = u / 2, Sendov's exponent is

    k(i) = sum_j max(floor(t * phi(i,j)) - 1, 0).

This script is exploratory only; floor decisions near integers need exact
certificates before they can support a proof or counterexample.
"""

from __future__ import annotations

import argparse
import math
import random
import itertools


def cyclic_gaps(points: list[tuple[float, float]], i: int) -> list[float]:
    x0, y0 = points[i]
    dirs = []
    for j, (x, y) in enumerate(points):
        if i == j:
            continue
        a = math.atan2(y - y0, x - x0) % math.pi
        dirs.append(a / math.pi)
    dirs.sort()
    if len(dirs) == 1:
        return [1.0]
    return [
        (dirs[(j + 1) % len(dirs)] - dirs[j]) % 1.0
        for j in range(len(dirs))
    ]


def exponent(gaps: list[float], t: float, eps: float = 1e-10) -> int:
    return sum(max(math.floor(t * gap + eps) - 1, 0) for gap in gaps)


def profile(points: list[tuple[float, float]], t: float) -> tuple[int, ...]:
    return tuple(sorted((exponent(cyclic_gaps(points, i), t) for i in range(len(points))), reverse=True))


def angle(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    """Angle ABC in radians."""
    ux, uy = a[0] - b[0], a[1] - b[1]
    vx, vy = c[0] - b[0], c[1] - b[1]
    den = math.hypot(ux, uy) * math.hypot(vx, vy)
    if den == 0:
        return math.pi
    cosv = max(-1.0, min(1.0, (ux * vx + uy * vy) / den))
    return math.acos(cosv)


def capped(points: list[tuple[float, float]], t: float) -> bool:
    cap = math.pi * (1.0 - 1.0 / t)
    for i, j, k in itertools.combinations(range(len(points)), 3):
        if max(
            angle(points[j], points[i], points[k]),
            angle(points[i], points[j], points[k]),
            angle(points[i], points[k], points[j]),
        ) > cap + 1e-10:
            return False
    return True


def search(s: int, t: float, trials: int, seed: int) -> None:
    rng = random.Random(seed)
    best_weight = -1
    best = None
    seen: dict[tuple[int, ...], int] = {}
    accepted = 0
    for _ in range(trials):
        points = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(s)]
        if not capped(points, t):
            continue
        accepted += 1
        p = profile(points, t)
        weight = sum(2**k for k in p)
        seen[p] = seen.get(p, 0) + 1
        if weight > best_weight:
            best_weight, best = weight, points
            print(f"best weight={weight} profile={p} points={points}")
    print(f"accepted={accepted}/{trials}")
    print("top profiles:")
    for p, count in sorted(seen.items(), key=lambda kv: (-sum(2**k for k in kv[0]), -kv[1]))[:20]:
        print(sum(2**k for k in p), p, count)
    if best is not None:
        for i in range(s):
            print(i, cyclic_gaps(best, i))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--s", type=int, default=4)
    parser.add_argument("--t", type=float, default=3.75)
    parser.add_argument("--trials", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    search(args.s, args.t, args.trials, args.seed)
