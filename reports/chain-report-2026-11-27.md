# Conditional chain report: F6, then F3 (2026-11-27)

**Result: F6 DROP, F3-on-F5 DROP. F5 stays the retained base.** The chain ran unattended from 15:27
to 23:31 UTC (8 h 4 min), stopped as pre-registered and started nothing further. No abort condition
fired.

**The F3 verdict carries no information.** `policy_epsilon` changes only how a brain *plays*, not
how it learns, and the decision metric plays with random moves off. F3-on-F5 trained the same
brains as F5, weight for weight, so d = 0 on every seed was certain before it ran. See section 4.

Every base here is built on the **provisional base S1** (formally DROP vs R0; a departure from the
rule as written). The S1 re-test against R0 on fresh seeds 7–12 is still owed.

## 1. What was pre-registered

Protocol amendment `787c0ab` was committed and pushed before any F6 result existed (section "F5
result and the conditional chain"):

1. **F6 = F5 + sizes [11,13,…,31]** (odd sizes, 1100 / 220 / 220, same `maze_seed`, default 4× step
   limit), judged against F5.
2. **F3 = the retained base + `policy_epsilon` 0.1**, judged against that base. The retained base
   is F6 if F6 is KEEP, otherwise F5.
3. **STOP.** F2, the confirmation stage and the final test are not started.

**Rule (unchanged):** paired seeds 1–6, arena-check-2 overall (400 mazes, sizes 11–41). KEEP only
if mean(d) ≥ 2·SE **and** mean(d) ≥ 3 points.

**Aborts:** any run failure, a RAM guard trip, drift CHANGED-RELEVANT, or more than 3 of 6 seeds
collapsed in F6.

## 2. Run log

| Rung | Config sha256 | Start (UTC) | End (UTC) | Wall time | Exit | Drift | Bundles | Inputs | Max RSS |
|---|---|---|---|---|---|---|---|---|---|
| F6 | `8cf917d5…` | 15:27 | 20:54 | 5 h 27 min | 0 | SAME | 6 / 6 match | 82 (obs v2) | 541 MB |
| F3-on-F5 | `94a68550…` | 20:56 | 23:29 | 2 h 33 min | 0 | SAME | 6 / 6 match | 82 (obs v2) | 517 MB |

- Both runs were unsigned and came from the pinned worktree (`dc888a7`).
- Drift was checked 40 times during the chain, every time SAME (`logs/drift.log`).
- The RAM guard never stopped a run. Lowest MemAvailable was **7,617 MB** (11 GB total).
- No `ALERT.txt`, `RAM-ALERT.txt` or `DRIFT-ALERT.txt` was written.
- Backups to ladder-work: `9b0cf93` after F6 and `7f5c3ed` after F3, each mirrored to D: and pushed
  (fork only). No PR, no merge, no push upstream, and no change to the pin.
- **Time estimate miss:** F6 took 5 h 27 min, against my estimate of 4.3 h likely and 5.5 h at most.
  The chain took 8 h 4 min in total.

## 3. F6: sizes 11–31, judged against F5. DROP (near miss)

| Seed | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| F5 overall % | 96.8 | 88.0 | 90.8 | 91.8 | 91.0 | 89.0 |
| F6 overall % | 95.8 | 94.2 | 92.8 | 98.2 | 91.5 | 90.8 |
| d (points) | −1.0 | +6.2 | +2.0 | +6.5 | +0.5 | +1.7 |
| F5 kept try | 13,500 | 10,250 | 10,250 | 14,750 | 14,000 | 5,750 |
| F6 kept try | 9,750 | 8,000 | 2,250 | 14,500 | 1,500 | 6,250 |
| F6 last try | 15,000 | 15,000 | 12,250 (patience) | 15,000 | 11,500 (patience) | 14,500 (patience) |
| F6 collapse | no | **yes** | **yes** | no | no | no |

- **mean(d) = +2.67**, SE 1.25, 2·SE 2.50.
- It clears 2·SE but **not the 3-point minimum**, so the rule gives **DROP**.
- No seed fell by more than 10 points.

| arena-check-2 | F5 mean (SD) | F6 mean (SD) | Change |
|---|---|---|---|
| overall | 91.2 (3.0) | 93.9 (2.8) | +2.7 |
| band 11–17 | 99.2 (0.8) | 98.9 (1.2) | −0.3 |
| band 21–25 | 92.3 (3.8) | 95.0 (3.5) | +2.7 |
| band 31–41 | 74.2 (8.4) | **82.7 (6.4)** | **+8.5** |
| check | 97.8 (0.8) | 96.7 (2.2) | −1.1 |

**Reading (secondary, not deciding):**
- The wider pool helps where intended: band 31–41 rose by 8.5 points, and 5 of 6 seeds gained
  overall.
- It is less stable:
  - 2 of 6 seeds carry the collapse warning; F5 had none.
  - Three seeds were stopped early by patience.
  - Seeds 3 and 5 kept very early brains (tries 2,250 and 1,500), yet still scored 92.8 and 91.5.
- Small mazes (11–17) did not suffer.
- Under the rule F6 is DROP. It cannot be adopted by hand.

## 4. F3-on-F5: policy_epsilon 0.1, judged against F5. DROP (uninformative)

| Seed | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| F5 overall % | 96.8 | 88.0 | 90.8 | 91.8 | 91.0 | 89.0 |
| F3-on-F5 overall % | 96.8 | 88.0 | 90.8 | 91.8 | 91.0 | 89.0 |
| d (points) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Kept try (both) | 13,500 | 10,250 | 10,250 | 14,750 | 14,000 | 5,750 |

mean(d) = 0.00, SE 0.00, so the rule gives **DROP**. Collapse 0 of 6.

**Why d is exactly zero (checked 2026-11-28):**
1. **The pinned TRAINING.md L304 describes `policy_epsilon` as a playing setting.** The brain makes
   10% of its moves at random "in the arena and in scoring". It is not a training setting.
2. **Training was identical.** For all 6 seeds, `metrics.jsonl` from F5 and F3-on-F5 have the same
   1,561 lines with no differing field (timing fields excluded). That includes every validation
   check, so the same brain was kept at the same try.
3. **The weights are identical.** All ONNX initializers are equal on all 6 seeds. The `.onnx` sha256
   differs only because the file stores `name`, `training` and `policy_epsilon` in its metadata.
4. **The decision metric cannot see the change.** `scripts/eval_brain.py` plays arena-check-2
   greedily (epsilon 0.0, the same scorer that reproduced B-mixed-s1), so it ignores the brain's
   own `policy_epsilon`.
5. **The only place the setting shows is the trainer's own scoring,** which plays with the 10%
   random moves: check 90.9 for F3-on-F5 against 97.8 for F5, from the same weights. That number
   never decides a rung.

**Consequence:** as designed, F3 could only ever return d = 0, which is DROP. The run settles nothing
about whether random moves help in play. This should have been caught when F3 was specified; the
TRAINING.md line was available then.

## 5. Ladder status after the chain

| Rung | Change | vs | mean(d) | Verdict | Base after |
|---|---|---|---|---|---|
| R0 | full documented recipe | – | gate 76.7% | passed | R0 |
| S1 | lr 0.0003 + target_update 1000 | R0 | +8.58 | DROP (provisional base) | S1 |
| S2 | step limit factor 2 | S1 | −6.79 | DROP | S1 |
| F1 | observation v2 | S1 | +13.71 | KEEP | F1 |
| F4 | sizes 11–21 | F1 | +8.83 | KEEP | F4 |
| F5 | sizes 11–25 | F4 | +7.63 | KEEP | **F5** |
| F6 | sizes 11–31 | F5 | +2.67 | DROP | F5 |
| F3 | policy_epsilon 0.1 | F5 | 0.00 | DROP (uninformative) | F5 |
| F2 | loop_stop + loop_escape | – | – | not run (owner decision pending) | – |

**Retained base: F5** = R0 + S1 + F1 + F4 + F5. It scores 91.2% on arena-check-2 overall (SD 3.0),
with bands 99.2 / 92.3 / 74.2.

## 6. Decisions for the owner (nothing is running; nothing will start without you)

1. **Record F3.**
   - (a) As the rule says: DROP, with the note "uninformative: policy_epsilon does not change
     training and the metric is greedy". *Recommended.*
   - (b) Or: pre-register a play-time test that scores the **existing** F5 brains on arena-check-2
     with `policy_epsilon` 0.1. No training is needed; it is an evaluation-only change to
     `eval_brain.py`.
   - Either way, the protocol (which takes no edits once a result exists) needs a new amendment
     before (b).
2. **F2** (loop_stop + loop_escape, on F5): run it or record it as "not run (owner decision)".
   Unlike F3, it changes training rewards. Likely about 2.5 h on the 11–25 pool.
3. **Confirmation stage:** confirm-R0 (seeds 7–14), confirm-S1 (seeds 7–12, the S1 re-test that is
   still owed) and confirm-chain (F5 chain, seeds 7–14). `configs/ladder/drafts/confirm-chain.json`
   must be regenerated with the final `--dropped` list (S2, F6, F3 and possibly F2) and checked
   before approval.
4. **Optional note for later:** F6's gain at 31–41 (+8.5) came with collapse and early stops. Any
   future wider-pool rung would need a separately pre-registered change (for example to patience).
   It cannot be a re-run of F6.

## Files

- Tables: `reports/F6-table.md`, `reports/F3-on-F5-table.md` (JSON in `logs/`).
- Automatic summary: `reports/chain-summary.md`. Chain log: `logs/chain.log`.
- Protocol: `protocol/ladder-protocol.md` (amendment `787c0ab`). Time table:
  `reports/ladder-time-2026-11-26.md`.
- Runs: `runs/F6/`, `runs/F3-on-F5/`. `F3-on-F6` was not run.
