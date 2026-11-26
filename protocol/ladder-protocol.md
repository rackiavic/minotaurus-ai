# Ladder protocol (frozen)

Frozen before any training run. No edits once any result exists; a change after that point is a
new protocol file with a new name, and results under the old one stay labelled with it.

- Pinned code: `protocol/pinned.json` (upstream `dc888a7`, TRAINING.md sha256 `48c140f9…`).
- Every run comes from `worktrees/fresh` (detached at the pinned SHA) through `scripts/launch.sh`.
- Drift guard: `scripts/drift_check.sh` runs before every step, before each batch, every 30 min
  during runs (`scripts/drift_loop.sh`, writing to `logs/drift.log`) and before any report. On
  CHANGED-RELEVANT, running jobs keep going, nothing is pulled, every affected manifest is marked
  STALE, the owner is told which conclusions are at risk, and work waits for the owner's decision.

## Owner decision 2026-11-25 (before any result): one track, "Documented"

The pinned TRAINING.md (dc888a7) is the single authority. The Strict / Full-documented split and
the "built-in rewards only" rule are **dropped**. Everything TRAINING.md documents is allowed,
**except `dqn.imitation`** and any demonstration, teacher or copied-route method.

**Actual hardware (not the `.wslconfig` plan):** Intel i7-9750H, **6 physical cores** (12 logical
with hyper-threading), 7.7 GiB RAM, 2 GiB swap. torch is the **CPU build**, pinned by
`pyproject.toml` (`pytorch-cpu` index), with one thread per seed; there is no GPU training (owner
decision 2026-11-25). The
`.wslconfig` (10 cores, 11 GB, 4 GB swap) is in place but not active; the owner approved launching
on the current settings without restarting WSL. RAM guard: `scripts/ram_guard.sh` logs `free -m`
every 10 min to `logs/ram.log`. If available memory drops below 1 GB it stops one arm (pilot-c
first, then pilot-b), notes it in that run's manifest, and writes `logs/RAM-ALERT.txt`.

## Hard rules

1. Brains learn on their own: no behaviour cloning, demonstrations, teacher, copied routes or
   hand-written solver. **`dqn.imitation` appears in no config**, even though TRAINING.md
   documents it: its teacher is a shortest-way solver.
2. Only settings documented in the pinned TRAINING.md. Anything else is stopped and becomes a PR
   proposal, with no workaround.
3. Never choose anything using test mazes, hand-made levels or arena levels. This covers
   `scores.json` test, `test_stats.json`, `fixed_levels.json`, `data/levels/test-mazes/` and the
   final-test set. These numbers stay in files (blinded) and are never compared for a decision.
4. Final-test pile (200 mazes, seeds from 9,600,000): played once, on the final chosen config only.
5. No run starts without owner approval of the plan, the wall-time estimate and the disk estimate.

## Pilot closed (owner, 2026-11-26)

The pilot finished 2026-11-26 00:08 (all 6 runs exit 0, no RAM-guard stop, drift SAME).
`reports/pilot-table.md` and `logs/pilot-decision.json` hold the table.

- All 6 brains (A dqn-brain, B r3, C r3 + shaping; seeds 1, 2) score **0%** on check, practice
  and arena-check-2 (every band). All 6 bundles match.
- The pre-registered **fallback fired**: Rung 0 = r3, "Strict baseline does not learn at 4,000
  episodes".
- **Finding:** r3 and r3 + shaping do not learn on sizes 11–41 at 4,000 tries. Every try ran to its
  step limit, and no validation check finished a single maze.
- No pilot number moves into any rung. The R0–R8 ladder below this note's date is replaced by the
  restructure that follows; no R0–R8 run was ever started.

## Ladder (restructured by the owner 2026-11-26, before any ladder result)

**R0 = the full documented recipe** (`configs/ladder/drafts/R0.json`):

- The r3 network and learning block (hidden [128,128], lr 0.001, batch 64, gamma 0.98, replay 50000,
  target_update 200, epsilon 1.0 → 0.05, decay 0.997).
- Plus `dqn.shaping` true, `wall_mask` true, `dqn.novelty_bonus` 0.02, `dqn.revisit_penalty` 0.01,
  `border_exit` true, `patience` 40 and `eval_every` 250.
- **Narrow pool:** sizes [11,13,15,17], `size` 11, 400 / 80 / 80 mazes (100 / 20 / 20 per size),
  `maze_seed` 93,000,001.
- 15,000 tries; 6 paired seeds (1–6).
- novelty and revisit are **non-potential-based rewards** (labelled in every report).

**Gate:** if R0's mean over its 6 seeds on arena-check-2 **band 11–17** is **below 60%**, stop:
no forward rung runs, and the owner gets a report.

**Forward rungs:** each adds one change to the last **kept** config, starting from R0. A rung that
is not kept is dropped, and the next rung is applied to the previous kept config.

| Rung | One change | Note |
|---|---|---|
| F1 | `observation.version` 2 | |
| F2 | `loop_stop` {repeats 3, penalty 0.5} + `loop_escape` true | **non-potential-based reward** (loop_stop penalty) |
| F3 | `policy_epsilon` 0.1 | |
| F4 | wider training pool: sizes [11,13,15,17,19,21], 600 / 120 / 120 (100 / 20 / 20 per size), same `maze_seed` | **Risk flag:** B-mixed-25 (sizes 11–25, same recipe family, patience 40) had 3 of 4 seeds keep a try-500–750 brain and stop at 10,500–10,750 (arena-check-2 15.8–39.0%, against 63.7% for its one good seed). F4 reports per-seed kept try and early stop next to the score. |
| F5 | `train_step_limit_factor` 2 | Changes what is learned (training tries end at 2× the shortest path, scoring stays at 4×). It is a rung, not a speed setting. |

- No config contains `dqn.imitation`, a teacher, demonstrations or copied routes.
- A downward ablation of R0 (removing one part at a time) is optional and **not scheduled**.
- The reference `ref-b-mixed.json` (wide pool) is **not scheduled**.
- Configs are generated by `scripts/make_configs.py [--dropped F…]`, so each rung differs from its
  parent by exactly one change. The script refuses any config that contains size 41 or imitation.

## Pilot (pre-registered; it decides the Rung 0 recipe and nothing else)

- 6 runs at once (arms A, B, C × seeds 1, 2), 4,000 episodes. Same sizes, pools and `maze_seed` (93,000,001) as Rung 0.
  `eval_every` at its default (250), so best-on-validation applies and test is never used.
- Arms: 2 seeds (1, 2) of `data/examples/dqn-brain.json` as-is (`pilot/pilot-dqn-brain.json`),
  and 2 seeds (1, 2) of **r3** (`pilot/pilot-r3.json`). r3 copies only the network and learning
  settings of `data/examples/dqn-mixed-learning-brain.json`: hidden_layers [128,128], lr 0.001,
  batch 64, gamma 0.98, replay 50000, target_update 200, epsilon 1.0 → 0.05, decay 0.997. It has
  no shaping, novelty, revisit, wall_mask or patience. (Chosen by the owner, 2026-11-25.)
- **Caveat:** r3's documented no-collapse result (TRAINING.md L156–161) is for sizes 9–13 **with
  shaping, wall_mask and novelty on**. It is the best documented starting point, not a proven
  recipe with built-in rewards only.
- **Arm C (Full-documented; does NOT compete for the Rung 0 recipe):** r3 + `dqn.shaping` true
  only (`pilot/pilot-r3-shaping.json`, the F1 change on r3), seeds 1, 2, with the same episodes,
  sizes, pools, `maze_seed` and `eval_every`. It has no novelty, revisit, wall_mask or patience.
  It is reported beside A and B and is never part of the Rung 0 decision.
- Decision (arms A and B only): the arm with the higher mean **check (validation) score** becomes the Rung 0 recipe.
  An arm whose seeds both stay under 5% on check, or both carry the collapse warning, cannot win.
  If the arms are within 3 points, the simpler arm (`dqn-brain.json`) wins. arena-check-2 and size
  bands are reported but do not decide; test and hand-made levels are never looked at for this.
- **Fallback (pre-registered):** if both A and B score under 5% on validation (both seeds of
  each arm), then: Rung 0 = r3 (owner decision); the report states **"Strict baseline does not
  learn at 4,000 episodes"**; Full-documented F1 becomes the first rung expected to learn; and the
  Strict rungs S1, S2, S3a and S3b run only as **2-seed, 4,000-episode screens** (seeds 1, 2, same
  pools), not as full 8-seed, 15,000-episode rungs. A screen cannot "keep" a rung under the
  decision rule; it only shows whether anything starts to learn.
- **Owner decision 2026-11-25 (supersedes the track wording above, rule unchanged):** with one
  track, arms A and B are the reported **no-shaping reference** and arm C is the **candidate
  starting line**. The A-vs-B rule and the fallback above are kept unchanged for the pilot report.
  The ladder's R0 is r3 by owner decision. The fallback's "Strict rungs S1–S3b screens" clause no
  longer applies, because every rung is now screened at 4,000 × 8 anyway.
- No pilot result moves into any rung's statistics.

## Budgets (2026-11-26)

- Pilot (closed): 4,000 episodes, 2 seeds per arm.
- **Screening:** R0 and F1–F5 each at **15,000 tries × 6 paired seeds (1–6)**, on the narrow
  pool (F4 and later use F4's pool if F4 is kept). That is one batch of 6 processes on the 6
  physical cores. `patience` 40 may stop a seed early.
- **Confirmation (finalists):** retrain **R0** and the **kept chain's final config** at 15,000 tries
  × **8 paired seeds (1–8)** (`confirm-R0.json`, `confirm-chain.json`). Each config runs with
  `parallel` 3, and both run together, so 6 processes at once.
  - They train on the **narrow pool**. **Nothing trains on the wide 11–41 pool**, for confirmation
    or otherwise.
  - Exception: if F4 is kept, the chain's final config carries F4's 11–21 pool, because the pool is
    that rung's one change. R0 stays narrow.

## Seeds and pairing

- Screening uses seeds 1–6, confirmation 1–8. Seed *i* uses the same `seed` and the same
  `maze_seed` (93,000,001), so configs on the same pool see the same practice/check/test mazes.
- Never select on the best single seed. Each seed's own `seed-<n>/brain.onnx` is scored;
  `best-brain.onnx` (chosen by the trainer on validation) is never used for a decision.
- Overlap check (done 2026-11-25): pools from `maze_seed` 93,000,001 with sizes
  [11,13,15,17,21,25,31,41] and 800/160/160 share **0** wall layouts with arena-check-2 (400) and
  final-test (200). Any new `maze_seed` or size list must pass the same check before it runs.
- Overlap check (2026-11-26, `scripts/overlap_check.py`, pinned code; layouts rebuilt from ids and
  compared with `walls()`):
  - Narrow pool, sizes [11–17], 400/80/80 (R0–F3, confirmation): **0** shared with arena-check-2
    and **0** with final-test.
  - F4 pool, sizes [11–21], 600/120/120: **0** and **0**.

## Evaluation (every brain)

1. `scores.json`: practice / check / test share finished (written by `train`).
2. arena-check-2: `scripts/eval_brain.py`, using the frozen `protocol/arena-check-2-mazes.json`
   (sha256 `7898e722…`), the same `episode()` as B-mixed-s1's scorer, greedy. Checked: it
   reproduces B-mixed-s1 maze for maze (74.0%).
3. Size bands 11–17, 21–25, 31–41, plus overall, on arena-check-2.

Report per config: mean, SD, worst seed, best seed, and the practice-vs-check gap (memorisation
flag when the gap exceeds 15 points).

## Decision rule (paired by seed; amended 2026-11-26)

- **Screening (F1–F5):** the score is arena-check-2 **band 11–17**, the sizes the narrow pool
  trains on. n = 6.
- **Confirmation:** the score is arena-check-2 **overall** (11–41, 400 mazes), comparing the
  chain's final config against R0. n = 8.
- Every report also shows the other bands and overall.

d_i = new_i − kept_i over the n paired seeds actually used.
SE = sd(d) / √n. The rule itself is unchanged.
**Keep** a rung only if mean(d) ≥ 2·SE **and** mean(d) ≥ 3 points. Otherwise **drop** it and
continue from the previous kept config. **Flag** any rung where the worst seed falls by more than
10 points (reported; it does not by itself overrule the rule).

## Checkpoints

Every run, Rung 0 included, uses TRAINING.md's automated rule: `eval_every` at its default (250),
and each seed's `brain.onnx` is the best on validation. Test and hand-made levels never take part.
Nothing is picked by hand. `best-brain.onnx` (the best seed) is never used for a decision.

## Sizes

Every config records `sizes` exactly.

- Ladder and confirmation configs use the narrow pool, [11,13,15,17].
- F4 and later use [11,13,15,17,19,21] if F4 is kept.
- The pilot used [11,13,15,17,21,25,31,41] (closed).
- Evaluation always covers all arena-check-2 sizes, 11–41.

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
