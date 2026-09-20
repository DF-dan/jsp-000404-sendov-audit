# JSP-000404 / Erdős 504: exact direction-model audit

This repository records a reproducible audit of the missing general lower-bound step in the Sendov classification of Blumenthal's minimax-angle problem.

**Status:** research progress only. This repository does **not** claim a complete proof of JSP-000404 and is not yet an award submission.

## What is new here

- An exact QF_LRA transcription of the necessary direction model introduced in [TheJustinSunPrize/awards PR #100](https://github.com/TheJustinSunPrize/awards/pull/100).
- A rational SAT witness for the first unresolved boundary instance `Model 17 (9/2)`, checked against all 136 range constraints and 680 triangle disjunctions, then rechecked with the serialized values fixed.
- A transparent first-differing-bit construction for `Model 21 5`, checked against all 210 edges and 1,330 triples.
- A corrected implementation of the weight exponent in Sendov's 1995 Lemma 4.10: with `t = u/2`,

  ```text
  k(i) = sum_j max(floor(t * phi(i,j)) - 1, 0).
  ```

  The directions are unoriented lines in `RP¹`, and their normalized cyclic gaps sum to one.

The SAT witnesses are boundary sanity checks. They do not establish the missing universal cardinality inequalities, and an abstract direction-model witness need not be realizable by planar points.

## Reproduce

Requires Python 3.11+ and Z3:

```bash
python -m pip install -r requirements.txt

# Recheck the archived N=17 boundary orientation at a smaller parameter.
python scripts/recheck_orientation.py \
  --model results/model-N17-t9_2.json --t 449/100

# Recreate the explicit N=21, t=5 dyadic witness.
python scripts/explicit_dyadic_model.py \
  --n 21 --m 5 --out results/explicit-N21-t5-rebuilt.json

# Run a fresh exact model query (potentially expensive).
python scripts/model_audit.py --n 11 --t 399/100 --timeout-ms 120000
```

Expected results for the first two commands are `unsat` for the fixed `N=17` orientation at `449/100`, and `sat` for the explicit `N=21,t=5` construction.

## The remaining theorem

For the necessary direction model `Model N t`, a complete lower-bound proof would need parameterized results of the following form (with the strict endpoint details matched to the geometric transfer):

```text
floor(t) = n and t < n + 1/2  =>  N <= 2^n
floor(t) = n and t < n + 1    =>  N <= 2^n + 2^(n-2)
```

The existing Lean developments prove small cases and the strict power-of-two bound, but not these two half-step bounds in full generality. See [notes/status.md](notes/status.md).

## Sources and attribution

- Blagovest Sendov, *Обязательные конфигурации точек на плоскости* (1995), especially Lemmas 4.10–4.12 and Theorem 4.4: [MathNet record and PDF](https://www.mathnet.ru/php/archive.phtml?jrnid=fpm&option_lang=rus&paperid=81&wshow=paper).
- Prize problem and public history: [Erdős Problems #504](https://www.erdosproblems.com/504) and [JSP-000404](https://github.com/TheJustinSunPrize/awards).
- The direction-model interface was first published in [PR #100](https://github.com/TheJustinSunPrize/awards/pull/100). This repository's checker is an independent executable transcription and does not claim authorship of that interface.
- Existing scoped formalizations and the published-proof caveat are documented in [PR #300](https://github.com/TheJustinSunPrize/awards/pull/300). Upper constructions originate in [PR #42](https://github.com/TheJustinSunPrize/awards/pull/42).

The current Erdős Problems webpage omits the numerator `2` in the smaller-interval formula. Sendov's Theorem 4.4 gives the corrected value `π(1 - 2/(2n+1))`; the error is already visible at `N=5`, where the correct value is `3π/5`.

## Authorship

Repository owner: [DF-dan](https://github.com/DF-dan). Computational exploration and repository preparation used OpenAI Codex. Historical mathematics and prior formalization interfaces are credited above.

