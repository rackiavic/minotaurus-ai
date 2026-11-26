"""Pilot table + pre-registered decision. Exit 1 if anything needed is missing (no table then).

  python3 pilot_table.py        -> reports/pilot-table.md, logs/pilot-decision.json

Per run (arm x seed): check (validation) score of the saved brain (scores.json "validation"),
practice (scores.json "train"), practice-vs-check gap, saved try, success-rate curve and
random-move rate (mean of the last 100 tries before 500/1000/2000/3000/4000), the collapse warning
(TRAINING.md rule: last validation check below half of the saved brain's), bundle match
(manifest "bundles" written by verify_bundles.py), arena-check-2 overall + bands (reported only).
BLINDED: scores.json "test" and test_stats.json are never read into the table; test_stats.json is
only checked to exist.

Decision (protocol, pre-registered; arms A and B only, C is reported but never competes):
  an arm whose two seeds are both < 5% on check, or both carry the collapse warning, cannot win;
  of the eligible arms, the higher mean check wins; within 3 points the simpler arm A wins.
  Fallback: if A and B are both < 5% on check on every seed -> Rung 0 = r3 (owner decision),
  report "Strict baseline does not learn at 4,000 episodes".
"""
import json, sys
from pathlib import Path

import os
P = Path(os.environ.get("MINOTAUR_ROOT", Path.home() / "Minotaur"))  # working root (ext4); D:\Minotaur is the mirror
ARMS = [("A", "pilot-dqn-brain", "dqn-brain.json as-is (64-64, decay 0.99)", True),
        ("B", "pilot-r3", "r3 (128-128, decay 0.997)", True),
        ("C", "pilot-r3-shaping", "r3 + shaping (Full-documented candidate, does not compete)", False)]
MARKS = (500, 1000, 2000, 3000, 4000)
errors = []


def need(cond, msg):
    if not cond:
        errors.append(msg)
    return cond


def curve(rows, key):
    tr = [r for r in rows if "avg_steps" in r]
    out = []
    for m in MARKS:
        w = [r[key] for r in tr if m - 100 < r["episode"] <= m]
        out.append(round(sum(w) / len(w), 3) if w else None)
    return out


def main():
    table, by_arm = [], {}
    for arm, run, label, competes in ARMS:
        man = json.loads((P / "runs" / run / "manifest.json").read_text())
        need(man.get("end") and man.get("exit_code") == 0, f"{run}: run did not finish cleanly (exit {man.get('exit_code')})")
        bundles = {Path(b["bundle"]).parent.name: b for b in man.get("bundles", []) if "bundle" in b}
        for seed_dir in sorted((P / "runs" / run).glob("**/seed-*")):
            n = seed_dir.name.split("-")[1]
            sc_file, met = seed_dir / "scores.json", seed_dir / "metrics.jsonl"
            if not (need(sc_file.is_file(), f"{run} s{n}: no scores.json") and need(met.is_file(), f"{run} s{n}: no metrics")):
                continue
            need((seed_dir / "test_stats.json").is_file(), f"{run} s{n}: no test_stats.json")
            sc = json.loads(sc_file.read_text())
            rows = [json.loads(l) for l in met.read_text().splitlines() if l.strip()]
            saved = next((r for r in rows if "exported_episode" in r), None)
            vals = [r["validation_success"] for r in rows if "validation_success" in r and "exported_episode" not in r]
            collapse = bool(saved and vals and saved["validation_success"] > 0 and vals[-1] < saved["validation_success"] / 2)
            b = bundles.get(seed_dir.name)
            need(b is not None and b.get("match") is True, f"{run} s{n}: bundle check missing or failed")
            ac2f = P / "runs" / run / f"ac2-s{n}.json"
            ac2 = json.loads(ac2f.read_text()) if need(ac2f.is_file(), f"{run} s{n}: no arena-check-2 result") else None
            row = {"arm": arm, "run": run, "seed": int(n), "competes": competes,
                   "check": sc["validation"], "practice": sc["train"],
                   "gap_points": round(100 * (sc["train"] - sc["validation"]), 1),
                   "saved_at": saved and saved["exported_episode"], "collapse": collapse,
                   "success_curve": curve(rows, "success_rate"), "epsilon_curve": curve(rows, "epsilon"),
                   "bundle_match": bool(b and b.get("match")), "bundle_sha256": b and b.get("bundle_sha256"),
                   "ac2": ac2 and ac2["overall"], "bands": ac2 and ac2["bands"]}
            table.append(row); by_arm.setdefault(arm, []).append(row)
    for arm, _, _, _ in ARMS:
        need(len(by_arm.get(arm, [])) == 2, f"arm {arm}: expected 2 seeds, found {len(by_arm.get(arm, []))}")
    if errors:
        print("PILOT TABLE CANNOT BE PRODUCED:\n" + "\n".join(errors)); sys.exit(1)

    def mean(a, k): return sum(r[k] for r in by_arm[a]) / len(by_arm[a])
    elig = {a: not (all(r["check"] < 0.05 for r in by_arm[a]) or all(r["collapse"] for r in by_arm[a])) for a in "AB"}
    fallback = all(r["check"] < 0.05 for a in "AB" for r in by_arm[a])
    if fallback:
        winner, why = "B (r3)", "FALLBACK: A and B both < 5% on check on every seed -> Rung 0 = r3 (owner decision). Strict baseline does not learn at 4,000 episodes."
    elif elig["A"] and elig["B"]:
        dA, dB = 100 * mean("A", "check"), 100 * mean("B", "check")
        if abs(dA - dB) <= 3: winner, why = "A (dqn-brain)", f"within 3 points ({dA:.1f} vs {dB:.1f}): simpler arm A"
        else: winner = "A (dqn-brain)" if dA > dB else "B (r3)"; why = f"higher mean check: A {dA:.1f} vs B {dB:.1f}"
    else:
        winner = "A (dqn-brain)" if elig["A"] else "B (r3)"
        why = f"only arm {'A' if elig['A'] else 'B'} is eligible (other arm < 5% on both seeds or collapsed on both)"
    decision = {"winner": winner, "reason": why, "eligible": elig, "fallback": fallback,
                "mean_check": {a: round(100 * mean(a, "check"), 1) for a in "ABC"}}

    pct = lambda x: "-" if x is None else f"{100 * x:.1f}"
    L = ["# Pilot table (4,000 tries; check = validation of the saved brain; test numbers blinded)", "",
         "| Arm | Seed | Check % | Practice % | Gap (pts) | Saved at | Success @500/1k/2k/3k/4k | Random-move rate @same | Collapse | Bundle | arena-check-2 % (11-17 / 21-25 / 31-41) |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in table:
        bands = " / ".join(pct(r["bands"][k]) for k in ("11-17", "21-25", "31-41"))
        L.append(f"| {r['arm']}{'' if r['competes'] else ' (not competing)'} | {r['seed']} | {pct(r['check'])} | {pct(r['practice'])} | {r['gap_points']} | {r['saved_at']} | "
                 f"{' / '.join(pct(x) for x in r['success_curve'])} | {' / '.join('-' if x is None else f'{x:.2f}' for x in r['epsilon_curve'])} | "
                 f"{'YES' if r['collapse'] else 'no'} | {'match' if r['bundle_match'] else 'FAIL'} | {pct(r['ac2'])} ({bands}) |")
    L += ["", f"**Mean check:** A {decision['mean_check']['A']}%, B {decision['mean_check']['B']}%, C {decision['mean_check']['C']}% (C not competing).",
          f"**Decision (pre-registered):** Rung 0 recipe = **{winner}**. {why}",
          "Memorisation flag: gap > 15 points. arena-check-2 is reported only; it did not decide."]
    (P / "reports" / "pilot-table.md").write_text("\n".join(L) + "\n")
    (P / "logs" / "pilot-decision.json").write_text(json.dumps({"decision": decision, "rows": table}, indent=1))
    print("\n".join(L))


if __name__ == "__main__":
    main()
