# Chair44 pinned build reproduction

*16 September 2026. Proof build and fresh axiom audit reproduced. The release
control suite has one packaging failure, detailed below.*

## Result

**The pinned release compiles without proof-source changes.** The cold
Chair44 source build took **1,120.40 seconds (18 minutes 40 seconds)** using
cached pinned Mathlib dependencies. `lake build R44Discharge` then passed,
and a separate fresh elaboration of `R44/Axioms.lean` passed.

All **169 lines** of the newly generated axiom log are byte-for-byte equal
to the shipped log. The unconditional final theorem `R44.r44_einstein`
depends on `propext`, `Classical.choice`, `Quot.sound` and **21 named
`native_decide` hooks**. No `sorryAx` appears in the reproduced report.
All 83 source/configuration input hashes remained unchanged and match the
pinned release. This materially advances the previous source-only review.

The mathematical scope is the inspected statement: existence of a tiling
of real Euclidean three-space by the literal square-pyramid solid, and for
every such tiling, no nonzero translation period and full symmetry-group
cardinality at most 24. The statement allows arbitrary affine isometries.
This is a reproduction of their formal proof with its disclosed compiler
trust boundary. It is not a proof of the corresponding physical claim for
our different curved-cap solid, nor an independent human mathematical review.

## Exact target and environment

- Release: `137e46b15d36266c37879478cfc62af6e4469147`.
- Disposable build copy: `/tmp/chair44-build/release`.
- Project: `/tmp/chair44-build/release/lean/R44`.
- Compiler: Lean 4.31.0, commit
  `68218e876d2a38b1985b8590fff244a83c321783`.
- Official Linux compiler archive SHA-256:
  `07a633cc8d9151cbc08825ea4cdda50d4b02a2c9cb852c0131b13046f49cad7f`;
  matched GitHub release metadata before extraction.
- Mathlib: `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, tag `v4.31.0`.
  All nine dependency commits are checked against the released manifest.
- Mathlib's precompiled cache was fetched from its official cache service.
  Chair44's own Lean modules are built from source. This is not a rebuild
  of the Lean compiler or all Mathlib proofs from source.

`strong/audit/build_chair44_release.py` records every proof-source hash,
compiler version, dependency commit, command, phase result and log hash.
It moves aside the shipped `build_axioms.log` before building. A successful
receipt therefore requires a newly generated final-theorem axiom line,
not the release's pre-existing log.

## Bootstrap issues and recovery

These were environment failures before Chair44 proof compilation:

1. Sandboxed Git and cache-host DNS failed. Authorized dependency fetches
   succeeded outside that network sandbox.
2. Mathlib's cache tool invokes `lean` through `PATH`; supplying only an
   absolute `lake` path was insufficient. Added the pinned compiler's `bin`.
3. The cache utility needs its process working directory to be the Lean
   project root. `lake -d` alone did not change that utility's working directory.
4. The filesystem initially had about 8.6 GB free. The compiler plus full
   Mathlib cache exhausted it during extraction. Only newly downloaded,
   reproducible cache archives were cleared. With authorization, the
   Mathlib library cache was moved to `/dev/shm/chair44-mathlib-lib`, with
   its old path replaced by a symlink. `cache get!` successfully fetched
   and re-extracted all 8,542 cache files, replacing potentially truncated
   outputs. The proof sources were not edited.

The RAM-backed library is visible to unsandboxed processes; this environment's
sandbox presents a different `/dev/shm`. Reusing the temporary setup therefore
requires the same execution permissions. These paths are temporary, not a
portable installation requirement. A machine with sufficient disk can keep
the dependency cache at its normal path.

## Commands and current evidence

The build driver is invoked from our repository root:

```sh
UV_CACHE_DIR=/tmp/aperiodic-uv-cache uv run --locked --offline python \
  strong/audit/build_chair44_release.py \
  --release-root /tmp/chair44-build/release \
  --lake /tmp/lean-4.31.0-linux/bin/lake \
  --logs-root /tmp/chair44-build/reproduction-1
```

It runs `lake build`, `lake build R44Discharge`, and a fresh elaboration of
`R44/Axioms.lean`, in that order. Logs and an incrementally written
`build_receipt.json` are in the requested logs directory. A failed earlier
phase prevents the later success claims.

The inspected release generator also passed under `uv`:

```sh
uv run --locked python /tmp/chair44-build/release/lean/R44/gen/extract.py --check
```

Output: `generated literals and SHA256 manifest: PASS`.

Separately, our [independent companion replay](CHAIR44_COMPANION_REPLAY.md)
passed the complete off-grid candidate/collision stage, including all 299,975
boxes and three corruption controls. That result does not depend on success
of this Lean build.

## Release controls: one genuine packaging failure

We ran the unmodified `scripts/controls.sh` through `uv`. It returned exit 1:

| Check | Result |
|---|---|
| Default proof build | PASS |
| Promoted proof-library build | PASS |
| Admission/import-closure checks | PASS; 80 local modules in import closure |
| Four diagnostic-checked negative controls | PASS, 4/4 |
| Positive scope regressions | PASS |
| Historical delivery diff audit | FAIL: required archive absent |

The first missing file is
`proof/external_lean/F1_exchange2/r44_F1_exchange2_discharge.zip`.
The public snapshot lacks the referenced historical delivery directory.
Thus the script cannot compare the final proof files with those earlier
deliveries. We did not skip this gate or alter the script to obtain a green
summary. Its final output is correctly recorded as `CONTROLS: FAIL`, with
one failed gate. This prevents claiming full reproduction of the advertised
control command, but it does not negate the successful theorem compilation,
fresh axiom audit or diagnostic-checked logical controls.

## Preserved evidence and remaining scope

- [Assessment](../audit/chair44_build/assessment.json): results, 21 hook names,
  release-checker hashes and evidence hashes.
- [Build receipt](../audit/chair44_build/build_receipt.json): toolchain,
  dependency revisions, all source hashes, exact commands and phase timings.
- [Cold source-build log](../audit/chair44_build/default-build.log).
- [Fresh axiom log](../audit/chair44_build/axioms-reproduced.log) and
  [shipped log](../audit/chair44_build/axioms-before-build.log).
- [Release controls](../audit/chair44_build/release-controls.log) and
  [generated-data check](../audit/chair44_build/generated-check.log).

Our independently written finite replay additionally verified the complete
companion census and collision certificates. Those computations corroborate
a major native-evaluation branch but do not remove the compiler hooks from
the Lean proof. A fully independent semantic audit of every geometric lemma
and every aspect of the manuscript is still beyond this reproduction.

Next useful work is an independent statement-to-geometry audit of the final
formal theorem and a concise account of the shared construction and proof
simplifications. The cold-build and off-grid replay milestones are complete;
do not repeat them without a source change or a specific unresolved concern.
