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

## Submission status

No prize PR should cite this repository as a completed solution. It becomes submission-ready only after the two parameterized capacity bounds are proved in Lean, connected to the exact `SendovAnswer` statement, and passed through the prize repository's `lean-verify` workflow.

