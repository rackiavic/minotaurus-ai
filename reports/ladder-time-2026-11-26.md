# Ladder time table (rev. 2026-11-27 after F1; base F1, built on provisional S1; order F4 F2 F3)

Measured, 6 seeds at once:
- R0: 2 h 44 min (5 of 6 seeds collapsed).
- S1: 1 h 18 min.
- S2: 1 h 0 min (DROP).
- **F1: 1 h 6 min** (KEEP).

The run time depends on collapse, so each rung is given as a range: F1's time (scaled for maze size) if it learns like F1, up to R0's time if it collapses like R0. F4 is expected to be slower than F1, because its mazes are larger.

| Step | Change | Seeds | Likely (F1-like) h | Upper (R0-like) h | Note |
|---|---|---|---|---|---|
| R0 | done 16:47-19:32 | 1-6 | 2.7 (done) | | |
| S1 | done 20:29-21:47, provisional base | 1-6 | 1.3 (done) | | |
| S2 | done 22:10-23:10, DROP | 1-6 | 1.0 (done) | | |
| F1 | done 23:15-00:21, KEEP | 1-6 | 1.1 (done) | | |
| F4 | F1 + sizes 11-21 (NOW) | 1-6 | 1.5 | 3.6 | larger mazes: about 1.33x the steps per try; also slower to learn, so more tries reach the step limit |
| F2 | + loop_stop + loop_escape (OPTIONAL) | 1-6 | 1.1 | 2.7 | may be skipped if the friend does not confirm it as official |
| F3 | + policy_epsilon 0.1 | 1-6 | 1.1 | 2.7 |  |
| **Screening still to run** | (without F2: 2.6 to 6.4) | | **3.7** | **9.1** | |
| Confirm | confirm-R0 (7-14) beside confirm-S1 (7-12) then confirm-chain (7-14); 6 processes; 22 runs | 7-14 | 8.2 | 13.5 | confirm-R0 (3 R0-like waves) sets the lower figure |
| **Total still to run** | | | **11.9** | **22.6** | |

Approved now: **F4 only**, likely about 1.5 h, at most about 3.6 h. Disk is about 25-35 MB per rung, against a budget of 1 GB. RAM: 6 processes, and the RAM guard stays on.
