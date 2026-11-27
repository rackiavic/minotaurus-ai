# Ladder time table (rev. 2026-11-27 after F5; base F5, built on provisional S1; conditional chain F6 then F3, then STOP)

Measured, 6 seeds at once:
- R0: 2 h 44 min (5 of 6 seeds collapsed).
- S1: 1 h 18 min.
- S2: 1 h 0 min (DROP).
- F1: 1 h 6 min (KEEP).
- F4: 1 h 37 min (KEEP; sizes 11-21).
- **F5: 2 h 33 min** (KEEP; sizes 11-25). That is 1.58x F4, more than the 1.29x from mean squared size alone (larger mazes also fail more often and run to their step limit).

The run time depends on maze size and on collapse. Since the WSL restart (2026-11-27), `.wslconfig` is active: 10 processors, 11 GB, 4 GB swap (it was 12 logical / 7.7 GiB / 2 GiB). Still 6 processes with one thread each, so results are unaffected. Wall time may differ slightly.

| Step | Change | Seeds | Likely h | Upper h | Note |
|---|---|---|---|---|---|
| R0 | done 16:47-19:32 | 1-6 | 2.7 (done) | | |
| S1 | done 20:29-21:47, provisional base | 1-6 | 1.3 (done) | | |
| S2 | done 22:10-23:10, DROP | 1-6 | 1.0 (done) | | |
| F1 | done 23:15-00:21, KEEP | 1-6 | 1.1 (done) | | |
| F4 | done 06:25-08:02, KEEP | 1-6 | 1.6 (done) | | |
| F5 | done 08:07-10:40, KEEP | 1-6 | 2.6 (done) | | |
| **F6** | F5 + sizes odd 11-31 (1100/220/220) | 1-6 | **4.3** | **5.5** | mean squared size 481 vs 345 (1.39x), times F5's extra factor 1.22, gives about 1.7x F5 |
| **F3** | + policy_epsilon 0.1 on the retained base | 1-6 | **4.3** (on F6) / **2.6** (on F5) | 5.5 / 3.5 | F3-on-F6 if F6 is KEEP, else F3-on-F5 |
| **Chain (F6 + F3)** | | | **6.9 to 8.6** | **11.0** | plus about 2 min post-rung per rung; then STOP |
| F2 | loop_stop + loop_escape | | | | not in the chain; owner decision after F3 |
| Confirm | confirm-R0 (7-14) beside confirm-S1 (7-12), then confirm-chain (7-14) | 7-14 | not estimated here | | not in the chain; needs the owner |

**RAM for the 11-31 pool:**
- Memory per seed does not grow with maze size. The observation is a fixed 82-number window, the replay buffer holds a fixed 50,000 transitions, and the network is unchanged. Max RSS during F5: 517 MB (`logs/time-F5.log`).
- The pool grows from 1,120 to 1,540 mazes (up to 31x31), which is a few MB.
- Measured during F5 (7.7 GiB total): lowest MemAvailable 3,801 MB. With 11 GB total now, F6 is expected at about 6.5-7 GB available. The RAM guard (`ram_guard.sh f6:F6 f3:F3-on-F6 f3:F3-on-F5`) stops the running rung below 1 GB, and the chain then aborts.

Disk: F4 27 MB, F5 28 MB, so about 30-40 MB per rung (about 80 MB for the chain), against a budget of 1 GB. 951 GB free.

Approved now (owner, 2026-11-27): **the conditional chain F6 then F3, then STOP**. Likely 7-9 h, at most about 11 h.
