# S2: per-seed table (15,000 tries; check = validation of the kept brain; test numbers blinded)

| Seed | Check % | Practice % | Gap (pts) | Kept try | Last try | Collapse | Bundle | arena-check-2 % | 11-17 | 21-25 | 31-41 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 90.0 | 85.8 | -4.2 | 8000 | 15000 | no | match | 56.2 | 82.0 | 48.0 | 13.0 |
| 2 | 85.0 | 83.5 | -1.5 | 3250 | 13250 (patience stop) | no | match | 53.0 | 80.5 | 38.0 | 13.0 |
| 3 | 86.2 | 84.0 | -2.3 | 9750 | 15000 | no | match | 50.0 | 76.5 | 37.0 | 10.0 |
| 4 | 87.5 | 86.8 | -0.7 | 11500 | 15000 | no | match | 54.5 | 80.0 | 42.0 | 16.0 |
| 5 | 88.8 | 88.5 | -0.2 | 13000 | 15000 | no | match | 56.8 | 84.0 | 48.0 | 11.0 |
| 6 | 85.0 | 87.8 | 2.7 | 14500 | 14500 (patience stop) | no | match | 55.0 | 81.5 | 49.0 | 8.0 |

| Column | Mean | SD | Worst seed | Best seed |
|---|---|---|---|---|
| check | 87.1 | 2.0 | 85.0 | 90.0 |
| practice | 86.0 | 2.0 | 83.5 | 88.5 |
| ac2 overall | 54.2 | 2.5 | 50.0 | 56.8 |
| band 11-17 | 80.8 | 2.5 | 76.5 | 84.0 |
| band 21-25 | 43.7 | 5.4 | 37.0 | 49.0 |
| band 31-41 | 11.8 | 2.8 | 8.0 | 16.0 |

Flags: none

## Decision vs S1 (pre-registered; arena-check-2 overall, paired by seed, n = 6)

| Seed | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| S1 overall % | 60.0 | 59.2 | 64.0 | 62.0 | 59.2 | 61.8 |
| S2 overall % | 56.2 | 53.0 | 50.0 | 54.5 | 56.8 | 55.0 |
| d (points) | -3.7 | -6.2 | -14.0 | -7.5 | -2.5 | -6.8 |
| S1 kept try | 5500 | 3250 | 12250 | 6000 | 5750 | 12250 |
| S2 kept try | 8000 | 3250 | 9750 | 11500 | 13000 | 14500 |

mean(d) = -6.79 points, SE = 1.64, 2*SE = 3.27. Collapse count: S2 0 of 6, S1 0 of 6.
Worst-seed drops > 10 points: seed 3 (-14.0).

**Label: provisional base, departure from rule.** S1 is a PROVISIONAL BASE: formally DROP vs R0 (mean d +8.58 < 2*SE 9.79); departure from the rule as written; re-test vs R0 on fresh seeds 7-12 at confirmation is obligatory.

**DROP S2** (rule: mean(d) >= 2*SE and >= 3 points). No later rung is started automatically.
