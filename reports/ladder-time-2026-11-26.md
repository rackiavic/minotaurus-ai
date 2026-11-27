# Ladder time table (rev. 2026-11-27 after F4; base F4, built on provisional S1; order F5 F3 F2)

Measured, 6 seeds at once:
- R0: 2 h 44 min (5 of 6 seeds collapsed).
- S1: 1 h 18 min.
- S2: 1 h 0 min (DROP).
- F1: 1 h 6 min (KEEP).
- **F4: 1 h 37 min** (KEEP; sizes 11-21).

The run time depends on maze size and on collapse.

| Step | Change | Seeds | Likely h | Upper (R0-like) h | Note |
|---|---|---|---|---|---|
| R0 | done 16:47-19:32 | 1-6 | 2.7 (done) | | |
| S1 | done 20:29-21:47, provisional base | 1-6 | 1.3 (done) | | |
| S2 | done 22:10-23:10, DROP | 1-6 | 1.0 (done) | | |
| F1 | done 23:15-00:21, KEEP | 1-6 | 1.1 (done) | | |
| F4 | done 06:25-08:02, KEEP | 1-6 | 1.6 (done) | | |
| F5 | F4 + sizes 11-25 (NOW) | 1-6 | 2.5 | 4.0 | owner estimate 2-3 h (larger mazes, more tries to learn them); F4 x 375/340 alone would give about 1.8 h |
| F3 | + policy_epsilon 0.1 | 1-6 | 2.5 | 4.0 | on the 11-25 pool if F5 is kept, else about F4's 1.6 h |
| F2 | + loop_stop + loop_escape (OPTIONAL) | 1-6 | 2.5 | 4.0 | only if the friend confirms it as official |
| **Screening still to run** | (without F2: 5.0 to 8.0) | | **7.5** | **12.0** | |
| Confirm | confirm-R0 (7-14) beside confirm-S1 (7-12) then confirm-chain (7-14, 11-25 pool if F5 kept); 6 processes; 22 runs | 7-14 | 10.1 | 14.6 | |
| **Total still to run** | | | **17.6** | **26.6** | |

**RAM for the larger pool:**
- Memory per seed does not grow with maze size: the observation is a fixed 82-number window, the replay buffer holds a fixed 50,000 transitions, and the network is unchanged.
- The pool grows from 840 to 1,120 mazes, which is a few MB.
- Measured during F4: MemAvailable 3,874-3,910 MB (lowest 3,874). F5 is expected about the same, roughly 3.8 GB available. The RAM guard stops F5 below 1 GB.

Disk: about 30-40 MB for F5, against a budget of 1 GB.

Approved now: **F5 only**, likely 2-3 h, at most about 4.0 h.
