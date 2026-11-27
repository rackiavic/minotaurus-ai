# F6: per-seed table (15,000 tries; check = validation of the kept brain; test numbers blinded)

| Seed | Check % | Practice % | Gap (pts) | Kept try | Last try | Collapse | Bundle | arena-check-2 % | 11-17 | 21-25 | 31-41 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 98.6 | 96.5 | -2.2 | 9750 | 15000 | no | match | 95.8 | 99.5 | 97.0 | 87.0 |
| 2 | 95.9 | 94.4 | -1.5 | 8000 | 15000 | YES | match | 94.2 | 99.0 | 96.0 | 83.0 |
| 3 | 95.5 | 95.0 | -0.5 | 2250 | 12250 (patience stop) | YES | match | 92.8 | 99.0 | 95.0 | 78.0 |
| 4 | 100.0 | 99.2 | -0.8 | 14500 | 15000 | no | match | 98.2 | 100.0 | 100.0 | 93.0 |
| 5 | 96.4 | 93.1 | -3.3 | 1500 | 11500 (patience stop) | no | match | 91.5 | 99.5 | 91.0 | 76.0 |
| 6 | 94.1 | 89.6 | -4.5 | 6250 | 14500 (patience stop) | no | match | 90.8 | 96.5 | 91.0 | 79.0 |

| Column | Mean | SD | Worst seed | Best seed |
|---|---|---|---|---|
| check | 96.7 | 2.2 | 94.1 | 100.0 |
| practice | 94.6 | 3.2 | 89.6 | 99.2 |
| ac2 overall | 93.9 | 2.8 | 90.8 | 98.2 |
| band 11-17 | 98.9 | 1.2 | 96.5 | 100.0 |
| band 21-25 | 95.0 | 3.5 | 91.0 | 100.0 |
| band 31-41 | 82.7 | 6.4 | 76.0 | 93.0 |

Flags: seed 2: collapse warning; seed 3: collapse warning

## Decision vs F5 (pre-registered; arena-check-2 overall, paired by seed, n = 6)

| Seed | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| F5 overall % | 96.8 | 88.0 | 90.8 | 91.8 | 91.0 | 89.0 |
| F6 overall % | 95.8 | 94.2 | 92.8 | 98.2 | 91.5 | 90.8 |
| d (points) | -1.0 | +6.2 | +2.0 | +6.5 | +0.5 | +1.7 |
| F5 kept try | 13500 | 10250 | 10250 | 14750 | 14000 | 5750 |
| F6 kept try | 9750 | 8000 | 2250 | 14500 | 1500 | 6250 |

mean(d) = +2.67 points, SE = 1.25, 2*SE = 2.50. Collapse count: F6 2 of 6, F5 0 of 6.
Worst-seed drops > 10 points: none.

**Label: provisional base, departure from rule.** F5 is built on the PROVISIONAL BASE S1 (formally DROP vs R0; departure from the rule as written); the S1 re-test vs R0 on fresh seeds 7-12 is still owed.

**DROP F6** (rule: mean(d) >= 2*SE and >= 3 points). No later rung is started automatically.
