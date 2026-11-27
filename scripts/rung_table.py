"""Per-seed table for one ladder run, plus the R0 gate. Exit 1 if anything needed is missing.

  python3 rung_table.py NAME [--seeds 6] [--gate] [--compare KEPT]   -> reports/NAME-table.md, logs/NAME-table.json

Per seed: check (scores.json "validation") and practice ("train") of the saved brain, the gap,
kept try (exported_episode), last try reached (below the episode budget = stopped by patience),
the collapse warning (TRAINING.md rule: last check below half of the kept brain's check), bundle
match (manifest "bundles" from verify_bundles.py), arena-check-2 overall and bands 11-17 / 21-25 /
31-41 (runs/NAME/ac2-s<n>.json from eval_brain.py). Summary: mean, SD, worst, best per column.
BLINDED: scores.json "test" and test_stats.json are never read (test_stats.json: existence only).
--gate (R0, protocol 2026-11-26): mean of arena-check-2 band 11-17 over the seeds < 60% -> GATE
FAILED, stop and report. Either way no later rung is started by this script.
--compare KEPT (protocol 2026-11-26 after R0): the pre-registered decision on arena-check-2 OVERALL,
paired by seed against logs/KEPT-table.json: d_i = new_i - kept_i, SE = sd(d)/sqrt(n); KEEP only if
mean(d) >= 2*SE and mean(d) >= 3 points, else DROP. Flag any seed that falls by more than 10 points.
Bands, kept try, last try and the collapse count are reported beside it, never deciding.
"""
import argparse, json, os, statistics as st, sys
from pathlib import Path

P = Path(os.environ.get("MINOTAUR_ROOT", Path.home() / "Minotaur"))
GATE = 0.60
# Owner amendment 2026-11-26 (before S2): S1 is formally DROP but is the provisional base for later rungs.
PROVISIONAL = {"F1": "F1 is built on the PROVISIONAL BASE S1 (formally DROP vs R0; departure from the rule as written); the S1 re-test vs R0 on fresh seeds 7-12 is still owed.", "S1": "S1 is a PROVISIONAL BASE: formally DROP vs R0 (mean d +8.58 < 2*SE 9.79); departure from the rule as written; re-test vs R0 on fresh seeds 7-12 at confirmation is obligatory."}
# Owner 2026-11-27 (label fix, verdicts unchanged): every later base is built on S1 as well.
for _b in ("F4", "F5", "F6"):
    PROVISIONAL[_b] = PROVISIONAL["F1"].replace("F1 is built", f"{_b} is built")
errors = []


def need(cond, msg):
    if not cond:
        errors.append(msg)
    return cond


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name"); ap.add_argument("--seeds", type=int, default=6); ap.add_argument("--gate", action="store_true"); ap.add_argument("--compare")
    a = ap.parse_args()
    run = P / "runs" / a.name
    man = json.loads((run / "manifest.json").read_text())
    need(man.get("end") and man.get("exit_code") == 0, f"run did not finish cleanly (exit {man.get('exit_code')})")
    need(man.get("drift_status") == "SAME", f"manifest drift_status {man.get('drift_status')}")
    budget = man["episodes"]
    bundles = {Path(b["bundle"]).parent.name: b for b in man.get("bundles", []) if "bundle" in b}
    rows = []
    for sd in sorted(run.glob("**/seed-*"), key=lambda p: int(p.name.split("-")[1])):
        n = sd.name.split("-")[1]
        sc_f, met = sd / "scores.json", sd / "metrics.jsonl"
        if not (need(sc_f.is_file(), f"s{n}: no scores.json") and need(met.is_file(), f"s{n}: no metrics")):
            continue
        need((sd / "test_stats.json").is_file(), f"s{n}: no test_stats.json")
        sc = json.loads(sc_f.read_text())
        mrows = [json.loads(l) for l in met.read_text().splitlines() if l.strip()]
        saved = next((r for r in mrows if "exported_episode" in r), None)
        vals = [r["validation_success"] for r in mrows if "validation_success" in r and "exported_episode" not in r]
        last = max((r["episode"] for r in mrows if "episode" in r), default=0)
        b = bundles.get(sd.name)
        need(b is not None and b.get("match") is True, f"s{n}: bundle check missing or failed")
        ac2f = run / f"ac2-s{n}.json"
        ac2 = json.loads(ac2f.read_text()) if need(ac2f.is_file(), f"s{n}: no arena-check-2 result") else None
        if ac2:
            need(ac2["sha256"] == (b or {}).get("onnx_sha256_in_tar"), f"s{n}: eval sha differs from bundle")
        rows.append({"seed": int(n), "check": sc["validation"], "practice": sc["train"],
                     "gap_points": round(100 * (sc["train"] - sc["validation"]), 1),
                     "kept_try": saved and saved["exported_episode"], "last_try": last,
                     "stopped_early": last < budget,
                     "collapse": bool(saved and vals and saved["validation_success"] > 0 and vals[-1] < saved["validation_success"] / 2),
                     "bundle_match": bool(b and b.get("match")),
                     "ac2": ac2 and ac2["overall"], "bands": ac2 and ac2["bands"]})
    need(len(rows) == a.seeds, f"expected {a.seeds} seeds, found {len(rows)}")
    if errors:
        print(f"{a.name} TABLE CANNOT BE PRODUCED:\n" + "\n".join(errors)); sys.exit(1)

    cols = {"check": lambda r: r["check"], "practice": lambda r: r["practice"], "ac2 overall": lambda r: r["ac2"],
            "band 11-17": lambda r: r["bands"]["11-17"], "band 21-25": lambda r: r["bands"]["21-25"],
            "band 31-41": lambda r: r["bands"]["31-41"]}
    summ = {k: {"mean": st.mean(f(r) for r in rows), "sd": st.stdev(f(r) for r in rows) if len(rows) > 1 else 0.0,
                "worst": min(f(r) for r in rows), "best": max(f(r) for r in rows)} for k, f in cols.items()}
    pct = lambda x: f"{100 * x:.1f}"
    L = [f"# {a.name}: per-seed table ({budget:,} tries; check = validation of the kept brain; test numbers blinded)", "",
         "| Seed | Check % | Practice % | Gap (pts) | Kept try | Last try | Collapse | Bundle | arena-check-2 % | 11-17 | 21-25 | 31-41 |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['seed']} | {pct(r['check'])} | {pct(r['practice'])} | {r['gap_points']} | {r['kept_try']} | "
                 f"{r['last_try']}{' (patience stop)' if r['stopped_early'] else ''} | {'YES' if r['collapse'] else 'no'} | "
                 f"{'match' if r['bundle_match'] else 'FAIL'} | {pct(r['ac2'])} | {pct(r['bands']['11-17'])} | "
                 f"{pct(r['bands']['21-25'])} | {pct(r['bands']['31-41'])} |")
    L += ["", "| Column | Mean | SD | Worst seed | Best seed |", "|---|---|---|---|---|"]
    for k, s in summ.items():
        L.append(f"| {k} | {pct(s['mean'])} | {pct(s['sd'])} | {pct(s['worst'])} | {pct(s['best'])} |")
    flags = [f"seed {r['seed']}: gap {r['gap_points']} > 15 (memorisation flag)" for r in rows if r["gap_points"] > 15]
    flags += [f"seed {r['seed']}: collapse warning" for r in rows if r["collapse"]]
    L += ["", "Flags: " + ("; ".join(flags) if flags else "none")]
    gate = None
    if a.gate:
        m = summ["band 11-17"]["mean"]
        gate = {"band_11_17_mean": m, "threshold": GATE, "passed": m >= GATE}
        L += ["", f"**Gate (pre-registered): mean arena-check-2 band 11-17 = {pct(m)}% "
                  f"{'>=' if m >= GATE else '<'} 60% -> {'PASSED' if m >= GATE else 'FAILED: stop and report; no forward rung runs'}.**",
              "No later rung is started automatically (owner, 2026-11-26)."]
    decision = None
    if a.compare:
        kept = {r["seed"]: r for r in json.loads((P / "logs" / f"{a.compare}-table.json").read_text())["rows"]}
        new = {r["seed"]: r for r in rows}
        if set(kept) != set(new):
            print(f"seeds differ from {a.compare}: {sorted(kept)} vs {sorted(new)}"); sys.exit(1)
        sd_ = sorted(new)
        d = [100 * (new[i]["ac2"] - kept[i]["ac2"]) for i in sd_]
        md = st.mean(d); se = st.stdev(d) / len(d) ** 0.5
        keep = md >= 2 * se and md >= 3
        drops = [(i, x) for i, x in zip(sd_, d) if x < -10]
        decision = {"vs": a.compare, "metric": "arena-check-2 overall", "n": len(d), "d_points": dict(zip(sd_, d)),
                    "mean_d": md, "se": se, "keep": keep, "worst_seed_drops_over_10": drops,
                    "collapse_count": {"new": sum(r["collapse"] for r in rows), "kept": sum(r["collapse"] for r in kept.values())}}
        L += ["", f"## Decision vs {a.compare} (pre-registered; arena-check-2 overall, paired by seed, n = {len(d)})", "",
              "| Seed | " + " | ".join(str(i) for i in sd_) + " |", "|---|" + "---|" * len(sd_),
              f"| {a.compare} overall % | " + " | ".join(pct(kept[i]["ac2"]) for i in sd_) + " |",
              f"| {a.name} overall % | " + " | ".join(pct(new[i]["ac2"]) for i in sd_) + " |",
              "| d (points) | " + " | ".join(f"{x:+.1f}" for x in d) + " |",
              f"| {a.compare} kept try | " + " | ".join(str(kept[i]["kept_try"]) for i in sd_) + " |",
              f"| {a.name} kept try | " + " | ".join(str(new[i]["kept_try"]) for i in sd_) + " |", "",
              f"mean(d) = {md:+.2f} points, SE = {se:.2f}, 2*SE = {2 * se:.2f}. Collapse count: {a.name} "
              f"{decision['collapse_count']['new']} of {len(rows)}, {a.compare} {decision['collapse_count']['kept']} of {len(kept)}.",
              f"Worst-seed drops > 10 points: {', '.join(f'seed {i} ({x:+.1f})' for i, x in drops) if drops else 'none'}.", "",
              *([f"**Label: provisional base, departure from rule.** {PROVISIONAL[a.compare]}", ""] if a.compare in PROVISIONAL else []),
              f"**{'KEEP' if keep else 'DROP'} {a.name}** (rule: mean(d) >= 2*SE and >= 3 points). "
              "No later rung is started automatically."]
    (P / "reports" / f"{a.name}-table.md").write_text("\n".join(L) + "\n")
    (P / "logs" / f"{a.name}-table.json").write_text(json.dumps({"rows": rows, "summary": summ, "gate": gate, "decision": decision}, indent=1))
    print("\n".join(L))


if __name__ == "__main__":
    main()
