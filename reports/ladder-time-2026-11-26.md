# Ladder time table (2026-11-26, from measured speeds; run order F1 F2 F3 F5 F4)

Per batch: 15,000 tries x steps/try x 2.9 ms (6 processes at once, benchmark batch 1) x 1.19 (wall time / training steps measured on the pilot: checks, scoring, export).
These are upper bounds. steps/try is the untrained figure (every try to its step limit). It falls as the brain learns, and patience 40 can stop a seed after 10,000+ tries.

| Step | Config | Seeds x parallel | Steps/try used | Source | Wall time (h) |
|---|---|---|---|---|---|
| R0 | full documented recipe, narrow 11-17 | seeds 1-6, 6 x 6 (1 batch) | 256 | measured (bench sizes 11-17) | 3.7 |
| F1 | + observation v2 | seeds 1-6, 6 x 6 (1 batch) | 256 | measured pool; 82 vs 77 inputs, assumed same | 3.7 |
| F2 | + loop_stop + loop_escape | seeds 1-6, 6 x 6 (1 batch) | 256 | upper bound (loop_stop can only end tries sooner) | 3.7 |
| F3 | + policy_epsilon 0.1 | seeds 1-6, 6 x 6 (1 batch) | 256 | measured pool | 3.7 |
| F5 | + train_step_limit_factor 2 (narrow) | seeds 1-6, 6 x 6 (1 batch) | 128 | ESTIMATE: 0.5 x 256 (bench factor 2 = 0.50 x base) | 1.8 |
| F4 | + sizes 11-21 (600/120/120), LAST | seeds 1-6, 6 x 6 (1 batch) | 340 | ESTIMATE, interpolated from bench 11-17 (256) and 11-25 (381); about 170 if F5 is kept | 4.9 |
| **Screening total** | R0 + F1, F2, F3, F5, F4, one after another | | | | **21.5** |
| Confirm | confirm-R0 + confirm-chain together, FRESH seeds 7-14 each: 16 runs, parallel 3 each = 6 at a time, 3 waves (3+3+2) | 8 x 3 | 128-340 | as above | 11.0 (set by R0) to 14.7 (F4 kept, F5 dropped) |
| **Total** | | | | | **32.5 to 36.1** (about 1.4-1.5 days of machine time) |

Approved now: R0 only, about 3.7 h. If the R0 gate fails (band 11-17 < 60%), nothing else runs.

Disk: measured 1.6 MB per 4,000-try seed. That gives at most about 5 MB per 15,000-try seed, x 52 seed runs, so about 0.3 GB. Budget 1 GB.

RAM: 6 processes at once, as measured in benchmark batch 1 (lowest available 3.6 GB). The RAM guard stays on.
