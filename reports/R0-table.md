# R0: per-seed table (15,000 tries; check = validation of the kept brain; test numbers blinded)

| Seed | Check % | Practice % | Gap (pts) | Kept try | Last try | Collapse | Bundle | arena-check-2 % | 11-17 | 21-25 | 31-41 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 88.8 | 94.5 | 5.8 | 10250 | 15000 | no | match | 75.0 | 91.0 | 77.0 | 41.0 |
| 2 | 76.2 | 80.5 | 4.3 | 10000 | 15000 | YES | match | 52.0 | 77.5 | 42.0 | 11.0 |
| 3 | 72.5 | 74.0 | 1.5 | 1250 | 11250 (patience stop) | YES | match | 49.0 | 74.0 | 39.0 | 9.0 |
| 4 | 83.8 | 78.0 | -5.8 | 1750 | 11750 (patience stop) | YES | match | 47.2 | 73.5 | 29.0 | 13.0 |
| 5 | 81.2 | 73.8 | -7.5 | 1500 | 11500 (patience stop) | YES | match | 42.8 | 67.0 | 27.0 | 10.0 |
| 6 | 78.8 | 74.5 | -4.2 | 1000 | 11000 (patience stop) | YES | match | 48.8 | 77.0 | 28.0 | 13.0 |

| Column | Mean | SD | Worst seed | Best seed |
|---|---|---|---|---|
| check | 80.2 | 5.7 | 72.5 | 88.8 |
| practice | 79.2 | 8.0 | 73.8 | 94.5 |
| ac2 overall | 52.5 | 11.4 | 42.8 | 75.0 |
| band 11-17 | 76.7 | 8.0 | 67.0 | 91.0 |
| band 21-25 | 40.3 | 19.0 | 27.0 | 77.0 |
| band 31-41 | 16.2 | 12.3 | 9.0 | 41.0 |

Flags: seed 2: collapse warning; seed 3: collapse warning; seed 4: collapse warning; seed 5: collapse warning; seed 6: collapse warning

**Gate (pre-registered): mean arena-check-2 band 11-17 = 76.7% >= 60% -> PASSED.**
No later rung is started automatically (owner, 2026-11-26).
