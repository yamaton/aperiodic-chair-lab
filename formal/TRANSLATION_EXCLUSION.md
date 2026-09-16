# Translation periods halve and vanish

*16 September 2026. Completed and verified with Lean 4.34.0.*

## Result and exact scope

`Chair.LegalTiling.translation_period_zero` proves:

```text
LegalTiling T → TranslationPeriod T v → v = (0,0,0).
```

The vector `v` is an arbitrary integer vector. `TranslationPeriod T v`
means that translating any decorated placement by `v` preserves membership
in `T` in both directions. Its equivalence to equality of the translated
placement set with `T` is proved in `translationPeriod_iff_moveTiling`.
`translation_stabilizer_trivial` states the final result directly using that
set equality.

Thus every legal tiling in the existing proper integer-grid model has no
nonzero integer translation period. The statement remains conditional:
there is no new proof that a `LegalTiling` exists. Arbitrary Euclidean
placements, reflections and the full finite-symmetry conclusion are outside
this addition. The frozen construction and prior-art attribution are unchanged.

## Proof

1. **Centers inherit periods.** Center recognition uses occurrence of the
   six specified neighboring placements. Translation preserves their relative
   motions and their occurrence, so every period of `T` is also a period of
   its recognized group centers.
2. **A period is even.** Macro coverage supplies an actual center `c`.
   Its translated copy `c+v` is another center. Both origins belong to the
   same proved parity class; subtracting their coordinates gives `v=2w`
   for an integer vector `w`. No separate nonempty-center assumption is used.
3. **The period halves.** For any alignment origin `o`, inflating a coarse
   placement translated by `w` equals translating its inflated placement by
   `2w`. Consequently `w` is a period of the actual deflated tiling.
   `LegalTiling.period_halves` applies this to the existing chosen legal
   deflation operation.
4. **Descent excludes a nonzero period.** Define `P(v)` to mean that `v`
   is a period of some legal tiling. The previous step proves that every
   `P(v)` has a half `w` with `P(w)`. The norm
   `|v.x| + |v.y| + |v.z|` is a natural number and strictly decreases when
   a nonzero even vector is halved. Strong induction proves that only zero
   can satisfy `P`.

The tiling witnessing `P` may change at every step. This is essential because
deflation produces another legal tiling; no self-similarity assumption is
made about the starting tiling. The proof needs only closure under one legal
deflation, rather than any additional limiting or compactness argument.

## Sources and theorem map

| File | Main declarations |
|---|---|
| [Translations](Chair/Translations.lean) | `TranslationPeriod`, equivalence to translated-set equality, center transport and deflated period transport |
| [PeriodHalving](Chair/PeriodHalving.lean) | `LegalTiling.period_even`, `LegalTiling.period_halves` |
| [IntegerDescent](Chair/IntegerDescent.lean) | Coordinate-sum norm and generic `doubling_descent` |
| [TranslationExclusion](Chair/TranslationExclusion.lean) | `LegalTiling.translation_period_zero`, `LegalTiling.translation_stabilizer_trivial` |

## Verification and review

The full uv verifier passed all three deterministic regeneration checks,
the project build, independent contact-table comparison, and 52 theorem
axiom audits. The manifest records 40 Lean source hashes. Only the standard
`propext`, `Classical.choice`, and `Quot.sound` occur. The generic descent
uses only `propext` and `Quot.sound`. No admitted proof, custom axiom or
native-evaluation dependency was introduced. Earlier compiled proof artifacts
were reused; this was not a cold rebuild of the full dependency chain.

Two subagents implemented translation transport and arithmetic descent;
the coordinator implemented evenness, the combined halving theorem and
the final exclusion theorem. A third agent with no authorship role reviewed
all four new modules and traced the supporting grouping, assembly, parity
and deflation definitions. It found no material defect and requested no edit.
It independently ran `lake env lean Chair/TranslationExclusion.lean` and
`lake env lean Audit.lean`, both successfully. This is an AI review independent
of authorship of this addition, not external human validation or a fresh
independent review of the entire earlier construction.

From the repository root:

```sh
uv run --locked python formal/verify.py --lake /path/to/lean/bin/lake --write-report
```

This session used `/tmp/lean-4.34.0-linux/bin/lake`. The preceding grouping
and deflation work is committed as `7d84070`. This addition was subsequently
committed locally at the user's request; no push or outreach was performed.

## Next obligations

The next symmetry deduction in the grid model is that two symmetries with
the same proper frame differ by a translation. Translation exclusion should
then make the frame map injective, bounding the symmetry group by the
24 proper cubic frames. This has not yet been formalized here.

Initial tiling existence remains a separate necessary proof branch. Connecting
the discrete model to the exact curved solid and establishing its full
Euclidean finite-symmetry theorem also remain outside the completed result.
