# S1: per-seed table (15,000 tries; check = validation of the kept brain; test numbers blinded)

| Seed | Check % | Practice % | Gap (pts) | Kept try | Last try | Collapse | Bundle | arena-check-2 % | 11-17 | 21-25 | 31-41 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 92.5 | 87.2 | -5.2 | 5500 | 15000 | no | match | 60.0 | 88.0 | 43.0 | 21.0 |
| 2 | 90.0 | 87.5 | -2.5 | 3250 | 13250 (patience stop) | no | match | 59.2 | 85.0 | 50.0 | 17.0 |
| 3 | 91.2 | 84.2 | -7.0 | 12250 | 15000 | no | match | 64.0 | 84.0 | 55.0 | 33.0 |
| 4 | 93.8 | 88.0 | -5.8 | 6000 | 15000 | no | match | 62.0 | 87.0 | 49.0 | 25.0 |
| 5 | 88.8 | 85.2 | -3.5 | 5750 | 14750 (patience stop) | no | match | 59.2 | 85.0 | 52.0 | 15.0 |
| 6 | 91.2 | 90.0 | -1.2 | 12250 | 14250 (patience stop) | no | match | 61.8 | 86.0 | 55.0 | 20.0 |

| Column | Mean | SD | Worst seed | Best seed |
|---|---|---|---|---|
| check | 91.2 | 1.8 | 88.8 | 93.8 |
| practice | 87.0 | 2.0 | 84.2 | 90.0 |
| ac2 overall | 61.0 | 1.9 | 59.2 | 64.0 |
| band 11-17 | 85.8 | 1.5 | 84.0 | 88.0 |
| band 21-25 | 50.7 | 4.5 | 43.0 | 55.0 |
| band 31-41 | 21.8 | 6.5 | 15.0 | 33.0 |

Flags: none

## Decision vs R0 (pre-registered; arena-check-2 overall, paired by seed, n = 6)

| Seed | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| R0 overall % | 75.0 | 52.0 | 49.0 | 47.2 | 42.8 | 48.8 |
| S1 overall % | 60.0 | 59.2 | 64.0 | 62.0 | 59.2 | 61.8 |
| d (points) | -15.0 | +7.3 | +15.0 | +14.8 | +16.5 | +13.0 |
| R0 kept try | 10250 | 10000 | 1250 | 1750 | 1500 | 1000 |
| S1 kept try | 5500 | 3250 | 12250 | 6000 | 5750 | 12250 |

mean(d) = +8.58 points, SE = 4.90, 2*SE = 9.79. Collapse count: S1 0 of 6, R0 5 of 6.
Worst-seed drops > 10 points: seed 1 (-15.0).

**DROP S1** (rule: mean(d) >= 2*SE and >= 3 points). No later rung is started automatically.
