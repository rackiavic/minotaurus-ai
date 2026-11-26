# Ladder time table (rev. 2026-11-26 after R0; order S1 S2 F1 F2 F3 F4)

Basis: **R0 measured 2 h 44 min** for 6 seeds at once (15,000 tries, narrow pool, 2 seeds ran the full 15,000; wall time = slowest seed). Each rung is one batch of 6 processes. A seed that fails to learn runs every try to its step limit and could be slower than R0.

| Step | Change | Seeds | Basis | Wall time (h) |
|---|---|---|---|---|
| R0 | done 2026-11-26 16:47-19:32 | 1-6 | measured | 2.7 (done) |
| S1 | lr 0.0003 + target_update 1000 | 1-6 | R0 measured | 2.7 |
| S2 | + train_step_limit_factor 2 | 1-6 | R0 measured (upper bound: factor 2 only shortens training tries) | 2.7 |
| F1 | + observation v2 | 1-6 | R0 measured | 2.7 |
| F2 | + loop_stop + loop_escape | 1-6 | R0 measured (upper bound) | 2.7 |
| F3 | + policy_epsilon 0.1 | 1-6 | R0 measured | 2.7 |
| F4 | + sizes 11-21 (LAST) | 1-6 | R0 x 340/256 (ESTIMATE from bench steps/try) | 3.6 |
| **Screening still to run** | S1 + S2 + F1 + F2 + F3 + F4 | | | **17.3** |
| Confirm | confirm-R0 + confirm-chain together, fresh seeds 7-14, parallel 3 each = 6 at a time, 3 waves (3+3+2) | 7-14 | 3 x R0 (x 340/256 if F4 kept) | 8.2 to 10.9 |
| **Total still to run** | | | | **25.5 to 28.2** (about 1.1-1.2 days of machine time) |

Approved now: **S1 only**, about 2.7 h.

Disk: R0 used 24M for 6 seeds. Budget 1 GB per rung.

RAM: 6 processes. R0 used about 2.9 GB at start, and the RAM guard stays on.
