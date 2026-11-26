# Ladder time table (rev. 2026-11-26 after S2; base S1 (provisional); order F1 F2 F3 F4)

Measured, 6 seeds at once:
- **R0: 2 h 44 min**, 5 of 6 seeds collapsed, so failing tries ran to the step limit.
- **S1: 1 h 18 min**, 0 collapsed.
- **S2: 0 h 60 min**, 0 collapsed; factor 2 halves the length of training tries. S2 was dropped.

The run time depends on collapse, so each rung is given as a range: S1's time if it learns like S1, up to R0's time if it collapses like R0.

| Step | Change | Seeds | Likely (S1-like) h | Upper (R0-like) h |
|---|---|---|---|---|
| R0 | done 16:47-19:32 | 1-6 | 2.7 (done) | |
| S1 | done 20:29-21:47 | 1-6 | 1.3 (done) | |
| S2 | done 22:10-23:10, DROP | 1-6 | 1.0 (done) | |
| F1 | S1 + observation v2 | 1-6 | 1.3 | 2.7 |
| F2 | + loop_stop + loop_escape | 1-6 | 1.3 | 2.7 |
| F3 | + policy_epsilon 0.1 | 1-6 | 1.3 | 2.7 |
| F4 | + sizes 11-21 (LAST) | 1-6 | 1.7 | 3.6 |
| **Screening still to run** | | | **5.6** | **11.8** |
| Confirm | confirm-R0 (7-14) beside confirm-S1 (7-12) then confirm-chain (7-14); 6 processes; 22 runs | 7-14 | 8.2 | 13.5 |
| **Total still to run** | | | **13.8** | **25.3** |

Approved now: **F1 only**, likely about 1.3 h, at most about 2.7 h. Disk is about 25 MB per rung, against a budget of 1 GB. RAM: 6 processes, and the RAM guard stays on.
