# Pilot table (4,000 tries; check = validation of the saved brain; test numbers blinded)

| Arm | Seed | Check % | Practice % | Gap (pts) | Saved at | Success @500/1k/2k/3k/4k | Random-move rate @same | Collapse | Bundle | arena-check-2 % (11-17 / 21-25 / 31-41) |
|---|---|---|---|---|---|---|---|---|---|---|
| A | 1 | 0.0 | 0.0 | 0.0 | 4000 | 0.0 / 0.0 / 0.0 / 0.0 / 0.0 | 0.05 / 0.05 / 0.05 / 0.05 / 0.05 | no | match | 0.0 (0.0 / 0.0 / 0.0) |
| A | 2 | 0.0 | 0.0 | 0.0 | 4000 | 0.0 / 0.0 / 0.0 / 0.0 / 0.0 | 0.05 / 0.05 / 0.05 / 0.05 / 0.05 | no | match | 0.0 (0.0 / 0.0 / 0.0) |
| B | 1 | 0.0 | 0.0 | 0.0 | 4000 | 0.0 / 0.0 / 0.0 / 0.0 / 0.0 | 0.26 / 0.06 / 0.05 / 0.05 / 0.05 | no | match | 0.0 (0.0 / 0.0 / 0.0) |
| B | 2 | 0.0 | 0.0 | 0.0 | 4000 | 0.0 / 0.0 / 0.0 / 0.0 / 0.0 | 0.26 / 0.06 / 0.05 / 0.05 / 0.05 | no | match | 0.0 (0.0 / 0.0 / 0.0) |
| C (not competing) | 1 | 0.0 | 0.0 | 0.0 | 4000 | 0.0 / 0.0 / 0.0 / 0.0 / 0.0 | 0.26 / 0.06 / 0.05 / 0.05 / 0.05 | no | match | 0.0 (0.0 / 0.0 / 0.0) |
| C (not competing) | 2 | 0.0 | 0.0 | 0.0 | 4000 | 2.0 / 0.0 / 0.0 / 0.0 / 0.0 | 0.26 / 0.06 / 0.05 / 0.05 / 0.05 | no | match | 0.0 (0.0 / 0.0 / 0.0) |

**Mean check:** A 0.0%, B 0.0%, C 0.0% (C not competing).
**Decision (pre-registered):** Rung 0 recipe = **B (r3)**. FALLBACK: A and B both < 5% on check on every seed -> Rung 0 = r3 (owner decision). Strict baseline does not learn at 4,000 episodes.
Memorisation flag: gap > 15 points. arena-check-2 is reported only; it did not decide.
