# R0 collapses (read-only, from runs/R0 metrics.jsonl; 2026-11-26)

Training columns: mean of the 100 tries ending at the kept try, at the fall (first check below half the kept check), and at the last try. Loops = validation_loops on the 80 check mazes.

| Seed | Kept try (check %, loops) | Fall (try; check %, loops) | Training success % kept→fall→end | Avg steps kept→fall→end | Loss kept→fall→end | Max loss (try) | Epsilon at kept |
|---|---|---|---|---|---|---|---|
| 1 | 10,250 (88.8, 9) | none | 83→–→66 | 122→–→162 | 0.018→–→0.093 | 692.7 (5,890) | 0.05 |
| 2 | 10,000 (76.2, 19) | 11,250; 33.8, 53 | 93→80→0 | 100→145→248 | 0.058→0.039→0.045 | 52,434.7 (3,730) | 0.05 |
| 3 | 1,250 (72.5, 22) | 1,750; 35.0, 52 | 77→73→8 | 123→135→244 | 0.007→0.009→0.235 | 2.4 (2,740) | 0.05 |
| 4 | 1,750 (83.8, 13) | 4,250; 11.2, 71 | 83→25→0 | 116→224→250 | 0.008→0.041→3.572 | 76,404.1 (5,250) | 0.05 |
| 5 | 1,500 (81.2, 15) | 4,500; 18.8, 65 | 79→33→0 | 125→210→256 | 0.007→0.074→0.169 | 339.0 (5,130) | 0.05 |
| 6 | 1,000 (78.8, 17) | 3,250; 23.8, 61 | 86→63→43 | 107→161→198 | 0.006→0.019→0.249 | 30.7 (4,880) | 0.06 |
