# Ladder protocol (frozen)

Frozen before any training run. No edits once any result exists; a change after that point is a
new protocol file with a new name, and results under the old one stay labelled with it.

- Pinned code: `protocol/pinned.json` (upstream `dc888a7`, TRAINING.md sha256 `48c140f9…`).
- Every run comes from `worktrees/fresh` (detached at the pinned SHA) through `scripts/launch.sh`.
- Drift guard: `scripts/drift_check.sh` runs before every step, before each batch, every 30 min
  during runs (`scripts/drift_loop.sh`, writing to `logs/drift.log`) and before any report. On
  CHANGED-RELEVANT, running jobs keep going, nothing is pulled, every affected manifest is marked
  STALE, the owner is told which conclusions are at risk, and work waits for the owner's decision.

## Hard rules

1. Brains learn on their own: no behaviour cloning, demonstrations, copied routes or hand-written
   solver. **`dqn.imitation` is excluded from both tracks**, even though TRAINING.md documents it:
   its teacher is a shortest-way solver.
2. Compliant track: only settings documented in the pinned TRAINING.md, built-in rewards only.
   Anything else is stopped and becomes a PR proposal, with no workaround.
3. Never choose anything using test mazes, hand-made levels or arena levels. This covers
   `scores.json` test, `fixed_levels.json`, `data/levels/test-mazes/` and the final-test set. These
   columns are reported but never compared for a decision.
4. Final-test pile (200 mazes, seeds from 9,600,000): played once, on the final chosen config only.
5. No run starts without owner approval of the plan, the wall-time estimate and the disk estimate.

## Tracks (reported side by side; neither replaces the other)

| Track | Contents | Improvement rule |
|---|---|---|
| Compliant | Rung 0 and the kept rungs; documented settings only | applies within the track, from Rung 0 |
| Research | B-mixed-s1 reference recipe (`configs/ladder/drafts/research-ref.json`); any extra is labelled | reference only |

## Budgets

Rung 0a: 4,000 episodes. Rung 0b and later rungs: 15,000. Research reference: 15,000.

## Seeds and pairing

- 8 seeds (1–8) for every config that feeds a decision. Seed *i* uses the same `seed` and the same
  `maze_seed` (93,000,001), so every config sees the same practice/check/test pools.
- Never select on the best single seed. Each seed's own `seed-<n>/brain.onnx` is scored;
  `best-brain.onnx` (chosen by the trainer on validation) is never used for a decision.
- Overlap check (done 2026-11-25): pools from `maze_seed` 93,000,001 with sizes
  [11,13,15,17,21,25,31,41] and 800/160/160 share **0** wall layouts with arena-check-2 (400) and
  final-test (200). Any new `maze_seed` or size list must pass the same check before it runs.

## Evaluation (every brain)

1. `scores.json`: practice / check / test share finished (written by `train`).
2. arena-check-2: `scripts/eval_brain.py`, using the frozen `protocol/arena-check-2-mazes.json`
   (sha256 `7898e722…`), the same `episode()` as B-mixed-s1's scorer, greedy. Checked: it
   reproduces B-mixed-s1 maze for maze (74.0%).
3. Size bands 11–17, 21–25, 31–41, plus overall, on arena-check-2.

Report per config: mean, SD, worst seed, best seed, and the practice-vs-check gap (memorisation
flag when the gap exceeds 15 points).

## Decision rule (arena-check-2 overall, paired by seed)

d_i = new_i − old_i, for i = 1..8. SE = sd(d) / √8.
**Keep** a rung only if mean(d) ≥ 2·SE **and** mean(d) ≥ 3 points. Otherwise the result is
**inconclusive** and the simpler config is kept. **Flag** any rung where the worst seed falls by
more than 10 points.

## Checkpoints

Rung 0 reports the final `brain.onnx` only (`eval_every: 0`, so no checkpoint picking). From Rung 1
on, the only selection is TRAINING.md's automated rule: best on validation every `eval_every`
tries. Nothing is picked by hand.

## Sizes

Every config records `sizes` exactly. Both tracks use [11,13,15,17,21,25,31,41]: the arena-check-2
sizes, which span the evaluated range, inside the schema's limit of 5–41. The compliant baseline
can configure them, so there is no size limitation to report.

## Bundles, signing and server checks (added 2026-11-25, before any run)

- Every seed's `bundle.tar` is checked by `scripts/verify_bundles.py` (run by `launch.sh`). The
  server's own `read_bundle()` checks must pass. sha256 of the `brain.onnx` inside the tar must
  equal the manifest `brain_id`, the manifest file entry, the seed's `brain.onnx` on disk, and the
  sha256 recorded by `eval_brain.py`. The bundle sha256 is written into the run manifest. Any
  mismatch means that seed is not reported until it is explained.
- Pilot and rung runs are **unsigned**. `launch.sh` sets `MINOTAURUS_SIGNING_KEY` to a path that
  never exists, and `--expect-unsigned` fails on any `signature.json`. `keygen` and `sign` are not
  run without the owner's approval. If approved, the private key lives in `D:\Minotaur\secrets\`
  only: outside every git worktree, gitignored, never pushed, never printed in reports or logs.
  Only the final chosen brain is signed.
- The server's "Verified" replay and the UI Compare / Brains / Random maze pages are for **final
  confirmation and visual inspection only**. They are never used to select a recipe, rung or seed.

## Manifest (written by `scripts/launch.sh` in `runs/<name>/manifest.json`)

Pinned SHA, TRAINING.md hash, config hash, seeds, maze_seed, sizes, uv.lock hash, hardware,
start/end time, exit code, drift status (SAME / STALE + stale_since).
