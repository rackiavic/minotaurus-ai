# Ladder protocol (frozen)

Frozen before any training run. No edits once any result exists; a change after that point is a
new protocol file with a new name, and results under the old one stay labelled with it.

- **Working root (owner, 2026-11-26): `~/Minotaur` (WSL ext4). `D:\Minotaur` is now the
  mirror.** The reason is tooling lag on the 9p mount (git, uv and scans). Results are not
  affected.
  - Scripts take `MINOTAUR_ROOT`, default `~/Minotaur`.
  - `scripts/mirror_to_d.sh` copies the root to D: after every run or batch and pushes
    ladder-work. It never deletes on D: and never touches `D:\Minotaur\secrets\`. `secrets/` lives
    on D: only; it is never copied to `~/Minotaur` and never goes into git.
  - Checked before any ladder run, under `~/Minotaur`:
    - same packages as the D: venv (`uv sync --frozen`, uv.lock unchanged);
    - drift SAME;
    - regression output identical to `logs/regress-dc888a7.json`;
    - eval_brain reproduces B-mixed-s1 maze for maze (74.0%; bands 93.5 / 65.0 / 44.0);
    - verify_bundles passes;
    - `make_configs.py` writes byte-identical configs.
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

**Forward rungs (owner, 2026-11-26, after R0 and before any rung result; supersedes the
F1, F2, F3, F5, F4 order):** each rung adds one change to the last **kept** config, starting from R0.
They run in this order: **S1, S2, F1, F2, F3, F4**, with F4 last. *(Order of the remaining rungs changed after F1, before any F4/F2 result:
**F4, then F2, then F3**. See "F1 result and reorder".)* *(Changed again after F4, before any F5 result:
**F5, then F3, then F2**. See "F4 result and F5".)* *(Changed again after F5, before any F6 or F3 result:
conditional chain **F6, then F3 on the retained base, then STOP**. See "F5 result and the conditional chain".)* A rung that is not kept is
dropped, and the next rung is applied to the previous kept config. Every rung keeps 15,000 tries,
`eval_every` 250, `patience` 40, 6 paired seeds (1–6), `maze_seed` 93,000,001 and the narrow pool
(F4 excepted).

| Rung | One change | Note |
|---|---|---|
| S1 | `dqn.learning_rate` 0.0003 + `dqn.target_update` 1000 | Stability. TRAINING.md L163–167 documents it as `dqn-mixed-wide-stable-brain.json`, "a guess at a steadier run; not run yet", given after a run where the loss diverged and wins fell to 0%. |
| S2 | `train_step_limit_factor` 2 | Changes what is learned (training tries end at 2× the shortest path, scoring stays at 4×). It is a rung, not a speed setting. |
| F1 | `observation.version` 2 | |
| F2 | `loop_stop` {repeats 3, penalty 0.5} + `loop_escape` true | **non-potential-based reward** (loop_stop penalty) |
| F3 | `policy_epsilon` 0.1 | |
| F4 (last) | wider training pool: sizes [11,13,15,17,19,21], 600 / 120 / 120 (100 / 20 / 20 per size), same `maze_seed` | **Risk flag:** B-mixed-25 (sizes 11–25, same recipe family, patience 40) had 3 of 4 seeds keep a try-500–750 brain and stop at 10,500–10,750 (arena-check-2 15.8–39.0%, against 63.7% for its one good seed). |

- No config contains `dqn.imitation`, a teacher, demonstrations or copied routes.
- A downward ablation of R0 (removing one part at a time) is optional and **not scheduled**.
- The reference `ref-b-mixed.json` (wide pool) is **not scheduled**.
- Configs are generated by `scripts/make_configs.py [--dropped S1,F2…]`, so each rung differs from its
  parent by exactly one change. The script refuses any config that contains size 41 or imitation.

## R0 result (recorded 2026-11-26, before any rung result)

R0 ran 2026-11-26 from 16:47 to 19:32 UTC: **2 h 44 min** for 6 seeds, exit 0, unsigned, drift
SAME. All 6 bundles match. Table: `reports/R0-table.md`.

- **Gate PASSED:** arena-check-2 band 11–17 mean **76.7%** (SD 8.0), above the 60% threshold.
- **Overall:** arena-check-2 mean **52.5%** (SD 11.4); worst seed 42.8, best seed 75.0. Bands:
  21–25 mean 40.3, 31–41 mean 16.2.
- **Collapse: 5 of 6 seeds** carry the collapse warning (seeds 2–6). Kept-at-try per seed:

  | Seed | 1 | 2 | 3 | 4 | 5 | 6 |
  |---|---|---|---|---|---|---|
  | Kept try | 10,250 | 10,000 | 1,250 | 1,750 | 1,500 | 1,000 |
  | Last try | 15,000 | 15,000 | 11,250 | 11,750 | 11,500 | 11,000 |

  Seeds 3–6 were stopped by patience.
- **Late-kept brains generalise better at 31–41.** Seeds 1 and 2, kept at try 10,000 or later,
  score 41.0 and 11.0. The four early-kept seeds score 9.0–13.0. Seed 1's 21–25 band is also the
  highest (77.0).
- **B-mixed-s1's 74.0%** corresponds to the **best seed** of its run, the same role seed 1 has here
  (75.0%). It is not a mean over seeds.
  - TRAINING.md documents `best-brain.onnx` as the best seed chosen on validation (L191–192). That is
    the way to produce a final brain.
  - Recipes are compared on the **mean of paired seeds**, never on a best seed.

## S1 result and owner amendment (2026-11-26, after S1, BEFORE any S2 result)

**S1 result (unchanged, not reinterpreted).** S1 ran 2026-11-26 20:29–21:47 UTC (**1 h 18 min**),
exit 0, unsigned, drift SAME, all 6 bundles matched. Table: `reports/S1-table.md`.

- arena-check-2 overall: mean 61.0 (SD 1.9). 0 of 6 seeds collapsed.
- Paired with R0 on seeds 1–6: d = −15.0, +7.3, +15.0, +14.8, +16.5, +13.0. mean(d) = **+8.58**,
  SE = 4.90, 2·SE = **9.79**. Worst-seed flag: seed 1, −15.0.
- **Verdict under the rule as written: DROP.** The S1 table and its verdict stay exactly as written.

**Owner amendment (pre-registered before S2 runs). This is a DEPARTURE FROM THE RULE AS WRITTEN.**

1. **S1 is the PROVISIONAL BASE** for S2 and every later rung, even though it is formally DROP.
   - Reason, stated before any S2 result exists: R0 collapsed in 5 of 6 seeds (seed SD 11.4), so
     comparisons against R0 are unreliable.
   - S1 had 0 of 6 collapses and a seed SD of 1.9.
   - Every report that uses S1 as a base carries the label **"provisional base, departure from
     rule"**.
2. **Obligation: re-test S1 against R0 at the confirmation stage.**
   - Fresh paired seeds **7–12** (n = 6), configs `confirm-R0.json` (seeds 7–14, of which 7–12
     pair) and `confirm-S1.json` (seeds 7–12).
   - Same rule and metric: keep only if mean(d) ≥ 2·SE **and** mean(d) ≥ 3 points, on
     arena-check-2 overall.
   - **If S1 fails there**, it is reported as failed, and every later rung that was built on it is
     revisited. Nothing is hidden or reframed.
3. **S2 = S1 + `train_step_limit_factor` 2**, judged against **S1** on paired seeds 1–6, with the
   same rule and metric (arena-check-2 overall).
4. **F1–F4** stay cumulative on the retained base. Each is judged against the previous retained
   config.
   - A rung that is KEEP becomes the new base.
   - A rung that is DROP is left out, and the next rung is applied to the previous retained config.
   - The only exception to the rule as written is S1, above.

## F1 result and reorder (owner, 2026-11-27, after F1, BEFORE any F4, F2 or F3 result)

**S2 result:** S2 ran 2026-11-26 22:10–23:10 UTC (1 h 0 min).
- arena-check-2 overall: mean 54.2 (SD 2.5).
- Against S1, paired on seeds 1–6: mean(d) = −6.79, SE = 1.64, so **DROP**. Worst-seed flag: seed 3,
  −14.0. Band 31–41 fell from 21.8 to 11.8.
- Table: `reports/S2-table.md`.

**F1 result:** F1 = S1 + `observation.version` 2. It ran 2026-11-26 23:15 to 2026-11-27 00:21 UTC
(**1 h 6 min**): exit 0, unsigned, drift SAME, all 6 bundles matched, and every brain takes 82
inputs (`logs/inputs-F1.md`).
- arena-check-2 overall: mean **74.8** (SD 1.3); worst seed 73.2, best 76.8. Bands: 11–17 94.5,
  21–25 72.2, 31–41 **37.8**. Check mean 97.7. 0 of 6 seeds collapsed; kept at tries 7,000–13,250.
- Against S1, paired on seeds 1–6: d = +15.2, +14.0, +12.7, +11.3, +15.5, +13.5. mean(d) =
  **+13.71**, SE = 0.65, 2·SE = 1.30, so **KEEP**. No worst-seed flag.
- Table: `reports/F1-table.md`.
- **F1 is the retained base.** It is built on the provisional base S1, and the re-test of S1 against
  R0 on fresh seeds 7–12 is still owed. Reports judged against F1 carry the provisional-base label
  too.

**Reorder of the remaining rungs** (stated before any of their results exist):
- **F4 now**, then **F2**, then **F3**. Each is applied to the last retained config and judged
  against it. Same rule and metric (arena-check-2 overall), paired seeds 1–6.
- **Reason:** the remaining weakness is large mazes (band 31–41 = 37.8), and the training pool stops
  at size 17. F4 widens it to [11..21].
- **F4 = F1 + sizes [11,13,15,17,19,21] only.** The pool keeps 100 / 20 / 20 mazes per size (600 /
  120 / 120), the same `maze_seed` and separate practice / check / test piles. The B-mixed-25 risk
  flag stays.
- **F2 (loop_stop + loop_escape) is optional.** It may be skipped if the friend does not confirm
  loop_stop / loop_escape as official (friend question 1: reward status of loop_stop). Skipping it
  is not a DROP; it is recorded as "not run". *(Superseded 2026-11-27, before any F3 or F2 result:
  F2 is no longer pending the friend. See "Friend answers and F2 status".)*

## F4 result and F5 (owner, 2026-11-27, after F4, BEFORE any F5, F3 or F2 result)

**F4 result:** F4 = F1 + sizes [11,13,15,17,19,21]. It ran 2026-11-27 06:25–08:02 UTC (**1 h 37
min**): exit 0, unsigned, drift SAME, all 6 bundles matched, and every brain takes 82 inputs.
- arena-check-2 overall: mean **83.6** (SD 2.2); worst seed 80.2, best 86.0. Bands: 11–17 98.0,
  21–25 83.0, 31–41 **55.3**. Check mean 97.4. 0 of 6 seeds collapsed.
- Against F1, paired on seeds 1–6: d = +5.0, +12.7, +5.5, +12.7, +8.7, +8.3. mean(d) = **+8.83**,
  SE = 1.38, 2·SE = 2.75, so **KEEP**. No worst-seed flag.
- Table: `reports/F4-table.md`.
- **F4 is the retained base** (R0 + S1 + F1 + F4). It is still built on the provisional base S1, and
  the S1 re-test against R0 on fresh seeds 7–12 is still owed.
- **Note:** band 31–41 (55.3) is the weakest. Most seeds kept a late brain: 5 of 6 at tries
  10,750–14,000, and seed 6 at 7,000.

**New rung F5** (stated before any of its results exist):
- **F5 = F4 + sizes [11,13,15,17,19,21,23,25] only.** It keeps the per-size scheme of 100 / 20 / 20
  (800 / 160 / 160), the same `maze_seed`, separate practice / check / test piles, and the default
  `train_step_limit_factor` (4×).
- It is judged against **F4** on paired seeds 1–6, with the same rule and metric (arena-check-2
  overall).
- **Label note:** "F5" once named the `train_step_limit_factor` 2 rung. That rung was renamed S2
  before it ran, so no result exists under the old label F5.

**Queue after F5:** F3 (`policy_epsilon` 0.1), then F2 (loop_stop + loop_escape). F2 is optional,
pending the friend's confirmation that it counts as official. Each is applied to the last retained
config and judged against it. *(Amended 2026-11-27, before any F3 or F2 result:
F2 is no longer pending the friend; whether it runs is the owner's decision. See "Friend answers and
F2 status".)*

## Friend answers and F2 status (owner, 2026-11-27, after F5, BEFORE any F3 or F2 result)

The friend (upstream repo owner) answered four questions:

1. **Tie rule:** TRAINING.md L247 ("on a tie the try with fewer loops wins, and after that the
   earlier one") and L275 ("a tie keeps the later brain") disagree, and the docs need fixing. The
   pinned code (`minotaurus/trainer/train.py:343–350`, tests `tests/test_loops.py:256–263`) does
   this: a higher check score wins; on a tied score, fewer loops wins; on a full tie, the **later**
   try is kept. Every rung ran on the same pinned code, so no recorded result changes. The docs fix
   is a PR proposal only; the pin stays at `dc888a7`.
2. **`loop_stop` and `loop_escape` are official** (documented settings, allowed under hard rule 2).
   loop_stop's penalty is still a **non-potential-based reward**, labelled in every report.
3. A **local verify command** (bundles and pool overlap in one command) is fine as a PR proposal.
4. **Speed PRs** (`train_every`, preallocated replay buffer) are fine as proposals.

**F2 status:**
- F2 is **no longer pending the friend's confirmation**.
- F2 **stays queued after F3**. The order is unchanged: F3, then F2.
- F2 **does not start automatically**. After F3's result, the owner decides whether F2 runs. If
  the owner decides not to run it, it is recorded as "not run (owner decision)", not as a DROP.
- If it runs, it is applied to the last retained config and judged against it, with the same rule
  and metric (arena-check-2 overall), on paired seeds 1–6.
- Nothing else changes: no approved config, pin, pool, seed or rule is edited by this note.

## F5 result and the conditional chain (owner, 2026-11-27, after F5, BEFORE any F6 or F3 result)

**F5 result:** F5 = F4 + sizes [11,13,15,17,19,21,23,25]. It ran 2026-11-27 08:07–10:40 UTC (**2 h
33 min**): exit 0, unsigned, drift SAME, all 6 bundles matched, and every brain takes 82 inputs.
- arena-check-2 overall: mean **91.2** (SD 3.0); worst seed 88.0, best 96.8. Bands: 11–17 99.2,
  21–25 92.3, 31–41 **74.2 (SD 8.4)**. Check mean 97.8. 0 of 6 seeds collapsed.
- Against F4, paired on seeds 1–6: d = +16.5, +2.0, +8.5, +5.8, +7.5, +5.5. mean(d) = **+7.63**,
  SE = 1.99, 2·SE = 3.99, so **KEEP**. No seed is worse than under F4.
- **Seed 1 is an outlier** (+16.5). Without it, mean(d) is about **+5.9**. This is reported and does
  not change the verdict.
- Table: `reports/F5-table.md`. It was regenerated to add the label "provisional base, departure from
  rule" (F4 is built on S1). The verdict and every number are unchanged; `logs/F5-table.json` is
  byte-identical.
- **F5 is the retained base.** It is still built on the provisional base S1, and the S1 re-test
  against R0 on fresh seeds 7–12 is still owed.

**Hardware note:** the WSL restart of 2026-11-27 activated `.wslconfig` (10 processors, 11 GB, 4 GB
swap). Rungs still run 6 processes with one thread each, so results are unaffected; wall time may
differ slightly.

**Pre-registered conditional chain (approved by the owner; it runs unattended and then STOPS):**

1. **F6 = F5 + sizes [11,13,15,…,31] only** (odd sizes; 100 / 20 / 20 per size, 1100 / 220 / 220;
   same `maze_seed`, separate practice / check / test piles, default 4× step limit).
   - Judged against **F5** on paired seeds 1–6, on arena-check-2 overall. The rule is unchanged:
     KEEP only if mean(d) ≥ 2·SE **and** mean(d) ≥ 3 points.
   - Overlap check: 0 shared layouts with arena-check-2 and 0 with final-test (all three piles).
2. **F3 = the retained base + `policy_epsilon` 0.1 only**, judged against that base by the same rule
   and metric.
   - The retained base is **F6 if F6 is KEEP, otherwise F5**.
   - Both variants are written before any result: `F3-on-F6.json` and `F3-on-F5.json`.
   - Decisions follow the rule only; nothing is chosen by hand.
3. **STOP after F3.** F2, the confirmation stage and the final test are **not** started. Each needs
   a new owner decision.

**Abort conditions.** On any of these the chain writes `logs/ALERT.txt`, starts nothing further and
**never resumes by itself**:
- any run failure (launch refused, exit code ≠ 0, or a post-rung step fails);
- a RAM guard trip;
- drift CHANGED-RELEVANT;
- a collapse count **above 3 of 6 in F6**.

**Mechanics:**
- `scripts/chain.sh` runs inside tmux (session `chain`), not from a chat session.
- Each rung goes through `launch.sh` in its own tmux session (`f6`, then `f3`), with the same
  safeguards as before: pinned worktree, unsigned, drift check and RAM guard
  (`ram_guard.sh f6:F6 f3:F3-on-F6 f3:F3-on-F5`).
- `post_rung.sh NAME BASE` evaluates each rung and decides it (`rung_table.py --compare BASE`).
  `chain.sh` then starts the F3 variant that the recorded decision selects.
- After each rung the chain commits that rung's table to ladder-work, mirrors to D: and pushes
  **ladder-work only**.
- At the end it writes `reports/chain-summary.md`: both tables, the decisions, the retained base,
  the time per rung, the minimum available memory and any flags.

**During the chain:** no PRs, no merges, no pushes to the friend's repo (upstream), and no change to
the pin (`dc888a7`).

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
- **Screening:** R0 and S1, S2, F1, F2, F3, F4 each at **15,000 tries × 6 paired seeds (1–6)**, on the narrow
  pool (F4, which runs last, uses its own 11–21 pool). That is one batch of 6 processes on the 6
  physical cores. `patience` 40 may stop a seed early.
- **Confirmation (finalists):** retrain **R0** and the **kept chain's final config** at 15,000 tries
  × **8 fresh paired seeds (7–14)** (`confirm-R0.json`, `confirm-chain.json`).
  - **Why fresh seeds:** the same seed gives the same run (TRAINING.md L129), and seeds 1–6
    selected the chain. Reusing them would only replay the screening.
  - **Plus `confirm-S1.json`** (S1 on fresh seeds 7–12, `parallel` 3). It is the obligatory re-test of
    the provisional base against confirm-R0's seeds 7–12 (owner, 2026-11-26).
  - That makes 16 runs (22 with confirm-S1), never more than 6 at a time. Each config runs with
  `parallel` 3, and both run together, so 6 processes at once.
  - They train on the **narrow pool**. **Nothing trains on the wide 11–41 pool**, for confirmation
    or otherwise.
  - Exception: if F4 is kept, the chain's final config carries F4's 11–21 pool, because the pool is
    that rung's one change. R0 stays narrow.

## Seeds and pairing

- Screening uses seeds 1–6, confirmation uses fresh seeds 7–14 (owner, 2026-11-26). Seed *i* uses the same `seed` and the same
  `maze_seed` (93,000,001), so configs on the same pool see the same practice/check/test mazes.
- Never select a recipe on the best single seed. Each seed's own `seed-<n>/brain.onnx` is scored;
  `best-brain.onnx` (chosen by the trainer on validation) is never used for a rung decision. It is the
  documented way to produce the **final** brain from the chosen config (see "R0 result").
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

- **Decision metric (owner, 2026-11-26, after R0 and before any rung result; supersedes band
  11–17):** every rung (S1, S2, F1, F2, F3, F4) is decided on arena-check-2 **overall** (11–41, 400
  mazes), n = 6, paired on seeds 1–6 against the last kept config.
- **Confirmation:** also decided on arena-check-2 **overall**, comparing the chain's final config
  against R0 on fresh seeds 7–14 (n = 8).
- **Secondary (reported, never deciding):** per seed, the bands 11–17 / 21–25 / 31–41, the kept-at-try,
  the last try (patience stop) and the collapse warning; per rung, the collapse count.
- The R0 gate stays as recorded (band 11–17 ≥ 60%, passed).
- **Provisional base (owner, 2026-11-26, before S2):** S1 is formally DROP but is the base for S2
  and later rungs, with a re-test against R0 on fresh seeds 7–12 at confirmation. See "S1 result and
  owner amendment". This is a departure from the rule as written.

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
- F4 (last rung) uses [11,13,15,17,19,21]. If F4 is kept, the chain's confirmation does too, and R0's confirmation stays on [11,13,15,17]. Both are scored on arena-check-2 overall (owner, 2026-11-26).
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
