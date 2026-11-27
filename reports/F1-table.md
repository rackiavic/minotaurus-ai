# F1: per-seed table (15,000 tries; check = validation of the kept brain; test numbers blinded)

| Seed | Check % | Practice % | Gap (pts) | Kept try | Last try | Collapse | Bundle | arena-check-2 % | 11-17 | 21-25 | 31-41 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 97.5 | 96.5 | -1.0 | 13250 | 15000 | no | match | 75.2 | 93.0 | 72.0 | 43.0 |
| 2 | 97.5 | 95.5 | -2.0 | 11000 | 15000 | no | match | 73.2 | 95.5 | 69.0 | 33.0 |
| 3 | 98.8 | 97.0 | -1.8 | 12250 | 15000 | no | match | 76.8 | 93.5 | 75.0 | 45.0 |
| 4 | 98.8 | 96.0 | -2.8 | 12500 | 15000 | no | match | 73.2 | 93.0 | 74.0 | 33.0 |
| 5 | 96.2 | 94.5 | -1.8 | 13000 | 13000 (patience stop) | no | match | 74.8 | 95.5 | 72.0 | 36.0 |
| 6 | 97.5 | 96.8 | -0.7 | 7000 | 15000 | no | match | 75.2 | 96.5 | 71.0 | 37.0 |

| Column | Mean | SD | Worst seed | Best seed |
|---|---|---|---|---|
| check | 97.7 | 0.9 | 96.2 | 98.8 |
| practice | 96.0 | 0.9 | 94.5 | 97.0 |
| ac2 overall | 74.8 | 1.3 | 73.2 | 76.8 |
| band 11-17 | 94.5 | 1.5 | 93.0 | 96.5 |
| band 21-25 | 72.2 | 2.1 | 69.0 | 75.0 |
| band 31-41 | 37.8 | 5.1 | 33.0 | 45.0 |

Flags: none

## Decision vs S1 (pre-registered; arena-check-2 overall, paired by seed, n = 6)

| Seed | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| S1 overall % | 60.0 | 59.2 | 64.0 | 62.0 | 59.2 | 61.8 |
| F1 overall % | 75.2 | 73.2 | 76.8 | 73.2 | 74.8 | 75.2 |
| d (points) | +15.2 | +14.0 | +12.7 | +11.3 | +15.5 | +13.5 |
| S1 kept try | 5500 | 3250 | 12250 | 6000 | 5750 | 12250 |
| F1 kept try | 13250 | 11000 | 12250 | 12500 | 13000 | 7000 |

mean(d) = +13.71 points, SE = 0.65, 2*SE = 1.30. Collapse count: F1 0 of 6, S1 0 of 6.
Worst-seed drops > 10 points: none.

**Label: provisional base, departure from rule.** S1 is a PROVISIONAL BASE: formally DROP vs R0 (mean d +8.58 < 2*SE 9.79); departure from the rule as written; re-test vs R0 on fresh seeds 7-12 at confirmation is obligatory.

**KEEP F1** (rule: mean(d) >= 2*SE and >= 3 points). No later rung is started automatically.
