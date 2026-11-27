# F4: per-seed table (15,000 tries; check = validation of the kept brain; test numbers blinded)

| Seed | Check % | Practice % | Gap (pts) | Kept try | Last try | Collapse | Bundle | arena-check-2 % | 11-17 | 21-25 | 31-41 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 97.5 | 94.5 | -3.0 | 14000 | 15000 | no | match | 80.2 | 96.5 | 79.0 | 49.0 |
| 2 | 96.7 | 96.3 | -0.3 | 13750 | 15000 | no | match | 86.0 | 99.0 | 86.0 | 60.0 |
| 3 | 98.3 | 95.7 | -2.7 | 10750 | 15000 | no | match | 82.2 | 97.5 | 78.0 | 56.0 |
| 4 | 96.7 | 96.8 | 0.2 | 12750 | 15000 | no | match | 86.0 | 99.0 | 87.0 | 59.0 |
| 5 | 96.7 | 95.5 | -1.2 | 12500 | 13500 (patience stop) | no | match | 83.5 | 97.0 | 84.0 | 56.0 |
| 6 | 98.3 | 96.2 | -2.2 | 7000 | 15000 | no | match | 83.5 | 99.0 | 84.0 | 52.0 |

| Column | Mean | SD | Worst seed | Best seed |
|---|---|---|---|---|
| check | 97.4 | 0.8 | 96.7 | 98.3 |
| practice | 95.8 | 0.8 | 94.5 | 96.8 |
| ac2 overall | 83.6 | 2.2 | 80.2 | 86.0 |
| band 11-17 | 98.0 | 1.1 | 96.5 | 99.0 |
| band 21-25 | 83.0 | 3.7 | 78.0 | 87.0 |
| band 31-41 | 55.3 | 4.2 | 49.0 | 60.0 |

Flags: none

## Decision vs F1 (pre-registered; arena-check-2 overall, paired by seed, n = 6)

| Seed | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| F1 overall % | 75.2 | 73.2 | 76.8 | 73.2 | 74.8 | 75.2 |
| F4 overall % | 80.2 | 86.0 | 82.2 | 86.0 | 83.5 | 83.5 |
| d (points) | +5.0 | +12.7 | +5.5 | +12.7 | +8.7 | +8.3 |
| F1 kept try | 13250 | 11000 | 12250 | 12500 | 13000 | 7000 |
| F4 kept try | 14000 | 13750 | 10750 | 12750 | 12500 | 7000 |

mean(d) = +8.83 points, SE = 1.38, 2*SE = 2.75. Collapse count: F4 0 of 6, F1 0 of 6.
Worst-seed drops > 10 points: none.

**Label: provisional base, departure from rule.** F1 is built on the PROVISIONAL BASE S1 (formally DROP vs R0; departure from the rule as written); the S1 re-test vs R0 on fresh seeds 7-12 is still owed.

**KEEP F4** (rule: mean(d) >= 2*SE and >= 3 points). No later rung is started automatically.
