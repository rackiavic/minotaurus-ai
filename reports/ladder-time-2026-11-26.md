# Ladder time table (rev. 2026-11-26 after S1; S1 = provisional base; order S2 F1 F2 F3 F4)

Measured, 6 seeds at once: **R0 2 h 44 min** (5 of 6 seeds collapsed: failing tries run to the step limit) and **S1 1 h 18 min** (0 collapsed: short tries). Run time depends on collapse, so each rung is given as a range: S1's time if it learns like S1, up to R0's time if it collapses like R0. S2 may be faster or slower than S1.

| Step | Change | Seeds | Likely (S1-like) h | Upper (R0-like) h |
|---|---|---|---|---|
| R0 | done 16:47-19:32 | 1-6 | 2.7 (done) | |
| S1 | done 20:29-21:47 | 1-6 | 1.3 (done) | |
| S2 | S1 + train_step_limit_factor 2 | 1-6 | 1.3 | 2.7 |
| F1 | + observation v2 | 1-6 | 1.3 | 2.7 |
| F2 | + loop_stop + loop_escape | 1-6 | 1.3 | 2.7 |
| F3 | + policy_epsilon 0.1 | 1-6 | 1.3 | 2.7 |
| F4 | + sizes 11-21 (LAST) | 1-6 | 1.7 | 3.6 |
| **Screening still to run** | | | **6.9** | **14.6** |
| Confirm | confirm-R0 (7-14) beside confirm-S1 (7-12) then confirm-chain (7-14); 3 + 3 processes = 6; 22 runs | 7-14 | 8.2 | 13.5 |
| **Total still to run** | | | **15.1** | **28.1** |

How confirmation is counted: confirm-R0 takes 3 waves of an R0-like run (8.2 h). confirm-S1 (2 waves) and confirm-chain (3 waves) run one after the other in the other 3 slots (6.5-13.5 h). The longer of the two sets the time.

Approved now: **S2 only**, likely about 1.3 h, at most about 2.7 h.

Disk: R0 and S1 used about 24 MB each for 6 seeds. Budget 1 GB per rung. RAM: 6 processes, and the RAM guard stays on.
