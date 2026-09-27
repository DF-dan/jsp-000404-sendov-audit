"""Exact certificate against the maximizing profile asserted in Sendov 1995.

The public 1995 English paper, Lemma 4.1(c.2), says that for four first-rank
centres and 1/2 <= delta < 1 the maximal profile is (n-1,n-2,n-2,n-3).
At t=u/2=15/4, n=3, delta=3/4, that profile has weight 9.  The points below
have the valid profile (2,2,0,0) of weight 10.  This does not refute the lemma's
final upper bound, which is also 10 in this case.

All decisive comparisons below use rational arithmetic.  Angle intervals come
from the alternating Taylor series for arctan on [0,1], with an exact one-term
remainder, and the Machin identity pi=16 atan(1/5)-4 atan(1/239).
"""

from fractions import Fraction as Q
from itertools import combinations
from math import factorial


POINTS = ((7, -7), (6, -6), (11, 15), (-16, -13))
T = Q(15, 4)
TERMS = 200


def atan_interval(z: Q):
    assert 0 <= z <= 1
    s = Q(0)
    for k in range(TERMS):
        term = z ** (2 * k + 1) / (2 * k + 1)
        s += term if k % 2 == 0 else -term
    next_term = z ** (2 * TERMS + 1) / (2 * TERMS + 1)
    signed = next_term if TERMS % 2 == 0 else -next_term
    return min(s, s + signed), max(s, s + signed)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[1], a[1] - b[0]


def mul_positive(c, a):
    assert c >= 0
    return c * a[0], c * a[1]


pi = sub(mul_positive(16, atan_interval(Q(1, 5))),
         mul_positive(4, atan_interval(Q(1, 239))))
assert 3 < pi[0] <= pi[1] < Q(22, 7)


def cos_interval(x, terms=16):
    """Rational Taylor enclosure valid for 0 <= x <= pi."""
    assert 0 <= x[0] <= x[1] <= pi[1]
    lo = hi = Q(0)
    for k in range(terms):
        a = x[0] ** (2 * k) / factorial(2 * k)
        b = x[1] ** (2 * k) / factorial(2 * k)
        if k % 2 == 0:
            lo += a
            hi += b
        else:
            lo -= b
            hi -= a
    remainder = x[1] ** (2 * terms) / factorial(2 * terms)
    return lo - remainder, hi + remainder


# At alpha=(1-1/t)pi=11pi/15, cos(alpha)<-3/5. Thus any angle
# whose cosine exceeds -3/5 is strictly below the allowed cap.
assert cos_interval(mul_positive(Q(11, 15), pi))[1] < -Q(3, 5)


def atan_nonnegative(z: Q):
    assert z >= 0
    if z <= 1:
        return atan_interval(z)
    return sub(mul_positive(Q(1, 2), pi), atan_interval(1 / z))


def line_angle(dx: int, dy: int):
    """A certified interval for the unoriented line angle in [0,pi)."""
    assert dx or dy
    if dy < 0 or (dy == 0 and dx < 0):
        dx, dy = -dx, -dy
    if dy == 0:
        return Q(0), Q(0)
    if dx == 0:
        return mul_positive(Q(1, 2), pi)
    if dx > 0:
        return atan_nonnegative(Q(dy, dx))
    return sub(pi, atan_nonnegative(Q(dy, -dx)))


def centre_exponent(i: int):
    x, y = POINTS[i]
    rays = sorted(line_angle(xx - x, yy - y)
                  for j, (xx, yy) in enumerate(POINTS) if j != i)
    assert all(rays[j][1] < rays[j + 1][0] for j in range(2))
    gaps = [sub(rays[j + 1], rays[j]) for j in range(2)]
    gaps.append(add(pi, sub(rays[0], rays[2])))
    floors = []
    for low, high in gaps:
        assert 0 <= low <= high
        scaled_low, scaled_high = T * low / pi[1], T * high / pi[0]
        floor_low, floor_high = scaled_low.numerator // scaled_low.denominator, \
            scaled_high.numerator // scaled_high.denominator
        assert floor_low == floor_high, (i, floor_low, floor_high)
        floors.append(floor_low)
    return sum(max(floor_value - 1, 0) for floor_value in floors), floors


def capped_angles():
    """Check all centre angles have cosine > -3/5 > cos(11pi/15)."""
    for a, b, c in combinations(range(4), 3):
        for i, j, k in ((a, b, c), (b, a, c), (c, a, b)):
            x, y = POINTS[i]
            ux, uy = POINTS[j][0] - x, POINTS[j][1] - y
            vx, vy = POINTS[k][0] - x, POINTS[k][1] - y
            dot = ux * vx + uy * vy
            if dot < 0:
                # dot/(|u||v|) > -3/5, exactly equivalent for dot<0.
                assert 25 * dot * dot < 9 * (ux * ux + uy * uy) * (vx * vx + vy * vy)


if __name__ == "__main__":
    capped_angles()
    details = [centre_exponent(i) for i in range(4)]
    profile = tuple(sorted((k for k, _ in details), reverse=True))
    assert profile == (2, 2, 0, 0), details
    assert sum(2 ** k for k in profile) == 10
    print("PASS: four integer-coordinate centres; all angles < 11pi/15")
    print("profile", profile, "weight", sum(2 ** k for k in profile))
    print("gap floors by centre", [floors for _, floors in details])
