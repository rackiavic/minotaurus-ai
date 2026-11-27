# Conditional chain summary (owner pre-registration 2026-11-27; F6 then F3, then STOP)

Status: **COMPLETE: F6 DROP; F3-on-F5 DROP; retained base F5. STOPPED (F2, confirmation and final test need the owner).**

Chain started 2026-11-27T15:27:26+00:00; summary written 2026-11-27T23:31:02.004582+00:00.
**Label: provisional base, departure from rule.** Every base here is built on S1 (formally DROP vs R0); the S1 re-test vs R0 on fresh seeds 7-12 is still owed.

| Rung | Judged vs | Start | End | Wall time | mean(d) | 2*SE | Decision | Collapse | Worst-seed drops > 10 |
|---|---|---|---|---|---|---|---|---|---|
| F6 | F5 | 2026-11-27T15:27 | 2026-11-27T20:54 | 5:27:13 | +2.67 | 2.50 | DROP | 2 of 6 | none |
| F3-on-F5 | F5 | 2026-11-27T20:56 | 2026-11-27T23:29 | 2:32:36 | +0.00 | 0.00 | DROP | 0 of 6 | none |

Retained base at the end: **F5**

Minimum MemAvailable during the chain (logs/ram.log, every 10 min): **7617 MB**

Flags: none

F2, confirmation and the final test were NOT started (owner decision required).

## F6 table (verbatim from reports/F6-table.md)

F6: per-seed table (15,000 tries; check = validation of the kept brain; test numbers blinded)

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


## F3-on-F5 table (verbatim from reports/F3-on-F5-table.md)

F3-on-F5: per-seed table (15,000 tries; check = validation of the kept brain; test numbers blinded)

| Seed | Check % | Practice % | Gap (pts) | Kept try | Last try | Collapse | Bundle | arena-check-2 % | 11-17 | 21-25 | 31-41 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 91.9 | 90.8 | -1.1 | 13500 | 15000 | no | match | 96.8 | 100.0 | 99.0 | 88.0 |
| 2 | 88.8 | 92.0 | 3.3 | 10250 | 15000 | no | match | 88.0 | 99.5 | 88.0 | 65.0 |
| 3 | 94.4 | 91.1 | -3.2 | 10250 | 15000 | no | match | 90.8 | 98.0 | 91.0 | 76.0 |
| 4 | 91.2 | 90.6 | -0.6 | 14750 | 15000 | no | match | 91.8 | 99.5 | 90.0 | 78.0 |
| 5 | 90.6 | 90.6 | 0.0 | 14000 | 15000 | no | match | 91.0 | 99.5 | 94.0 | 71.0 |
| 6 | 88.8 | 90.4 | 1.6 | 5750 | 15000 | no | match | 89.0 | 98.5 | 92.0 | 67.0 |

| Column | Mean | SD | Worst seed | Best seed |
|---|---|---|---|---|
| check | 90.9 | 2.1 | 88.8 | 94.4 |
| practice | 90.9 | 0.6 | 90.4 | 92.0 |
| ac2 overall | 91.2 | 3.0 | 88.0 | 96.8 |
| band 11-17 | 99.2 | 0.8 | 98.0 | 100.0 |
| band 21-25 | 92.3 | 3.8 | 88.0 | 99.0 |
| band 31-41 | 74.2 | 8.4 | 65.0 | 88.0 |

Flags: none

## Decision vs F5 (pre-registered; arena-check-2 overall, paired by seed, n = 6)

| Seed | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| F5 overall % | 96.8 | 88.0 | 90.8 | 91.8 | 91.0 | 89.0 |
| F3-on-F5 overall % | 96.8 | 88.0 | 90.8 | 91.8 | 91.0 | 89.0 |
| d (points) | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| F5 kept try | 13500 | 10250 | 10250 | 14750 | 14000 | 5750 |
| F3-on-F5 kept try | 13500 | 10250 | 10250 | 14750 | 14000 | 5750 |

mean(d) = +0.00 points, SE = 0.00, 2*SE = 0.00. Collapse count: F3-on-F5 0 of 6, F5 0 of 6.
Worst-seed drops > 10 points: none.

**Label: provisional base, departure from rule.** F5 is built on the PROVISIONAL BASE S1 (formally DROP vs R0; departure from the rule as written); the S1 re-test vs R0 on fresh seeds 7-12 is still owed.

**DROP F3-on-F5** (rule: mean(d) >= 2*SE and >= 3 points). No later rung is started automatically.


