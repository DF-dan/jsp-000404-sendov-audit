# Audit status

## Confirmed public landscape

As checked on 2026-09-20, the public JSP-000404 work covers:

- the two all-parameter upper constructions;
- exact values through `N=16` via finite certificates and special arguments;
- all dyadic endpoints;
- the transfer from capped planar configurations to a necessary real direction model.

The full non-dyadic lower bounds remain absent from the public Lean submissions reviewed here.

## Published-proof issue

Sendov reduces a perfect generalized configuration to a weighted capacity

```text
sum_i 2^k(i),
k(i) = sum_j max(floor(t * phi(i,j)) - 1, 0),
```

where the `phi(i,j)` are cyclic gaps between unoriented centre lines and sum to one at each centre. Lemma 4.12 states the final sharp capacity bounds but, from the four-centre case onward, asserts maximizing exponent profiles without deriving the induction step.

At `t=15/4`, admissible four-centre profiles of total weight `10` occur, while the profile asserted in the paper has weight `9`. This refutes that intermediate maximizer claim, but `10` is exactly the final bound `2^3 + 2^1`; it does not refute the classification itself.

## Exact model artifacts

`results/model-N17-t9_2.json` contains a rational assignment for the abstract necessary model at the first unresolved lower-branch boundary. The file records:

- 17 vertices;
- 136 edge variables;
- 680 triangle disjunctions;
- exact-assignment recheck: `sat`.

`results/explicit-N21-t5.json` contains the standard first-differing-bit assignment for 21 of the 32 five-bit words and checks all 1,330 triples.

These witnesses confirm that the threshold values themselves are feasible in the necessary model. A complete proof must exclude every model strictly below the relevant threshold, uniformly in the integer parameter.

## New branch certificate (2026-09-27)

The exact `N=17,t=9/2` witness has an orientation branch whose linear relaxation has minimum parameter exactly `9/2`. `scripts/branch_optimize.py` identifies ten active triangle constraints; the sum of their inequalities telescopes to `0 ≤ 2t-9`. `lean/Branch17Certificate.lean` checks this argument in Lean from the branch's ten order choices and the original triangle predicate. Its axiom printout contains only Lean's standard `propext`, `Classical.choice`, and `Quot.sound`.

This local certificate does not cover the other orientation branches. A fresh `N=17,t=449/100` query with a 180-second limit returned `unknown` (timeout), so it supplies neither a proof nor a counterexample for the full model bound.

## Submission status

No prize PR should cite this repository as a completed solution. It becomes submission-ready only after the two parameterized capacity bounds are proved in Lean, connected to the exact `SendovAnswer` statement, and passed through the prize repository's `lean-verify` workflow.

## Additional audit (2026-09-27)

An attempted general recurrence by two-coloring edges with direction value below `1` fails. Within each color class those edge values are at least `1`, but subtracting `1` from every direction does **not** preserve `Triangle` with parameter reduced from `t` to `t-1`: the upper-gap requirement also tightens by `1`. For example, at `t=249/100`, the forward triple `(a,b,c)=(1,17/10,12/5)` satisfies `Triangle t a b c`; after subtracting `1`, the gap `b-a=7/10` exceeds `(t-1)-1=49/100`. Thus the known three- and six-label base cases cannot be propagated by this shortcut.

Two independent bounded searches checked `Model 17 (449/100)`: cvc5 returned `unknown (TIMEOUT)` after 45 seconds, and a HiGHS mixed-integer formulation hit its 45-second limit without a primal witness. Neither result proves unsatisfiability. The exact public `Model 17 (9/2)` witness and its local branch certificate remain valid.

The separate English paper *Minimax of the angles in a plane configuration of points* (Acta Mathematica Hungarica 69, 27–46, 1995, DOI `10.1007/BF01874605`) was located; its full text requires journal access. No alternative proof of the missing all-parameter bound has been obtained from it.

