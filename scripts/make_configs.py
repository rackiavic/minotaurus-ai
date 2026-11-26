"""Write every ladder config from one place, so rungs differ only where intended.

  python3 make_configs.py [--dropped F2,F3]

Owner restructure 2026-11-26 (pilot closed, before any ladder result):
  R0 = full documented recipe: r3 network/learning block + shaping + wall_mask + novelty 0.02 +
       revisit 0.01 + border_exit + patience 40; NARROW pool sizes [11,13,15,17], size 11,
       400/80/80, maze_seed 93,000,001; 15,000 tries; eval_every 250; 6 paired seeds (1-6).
       Gate: R0 mean arena-check-2 band 11-17 < 60% -> stop and report.
  R0 ran 2026-11-26 (gate passed, band 11-17 76.7%). Owner re-order after R0, before any rung:
  forward rungs, one change each, applied to the last KEPT config (R0 first), in this order:
       S1 learning_rate 0.0003 + target_update 1000 (TRAINING.md L163-167)
       S2 train_step_limit_factor 2
       F1 observation.version 2      F2 loop_stop + loop_escape (NON-potential-based)
       F3 policy_epsilon 0.1         F4 wider training pool, sizes [11..21] (B-mixed-25 risk), LAST
  Every rung is decided on arena-check-2 OVERALL (11-41), n = 6.
  Owner amendment after S1 (before S2): S1 is formally DROP but is the PROVISIONAL BASE (departure
  from the rule as written), so S1 is NOT passed to --dropped; S2 = S1 + factor 2. confirm-S1
  (fresh seeds 7-12) is the obligatory re-test of S1 against confirm-R0 seeds 7-12.
  `--dropped` lists rungs the decision rule dropped; until results exist every rung is assumed
  kept, so S2-F4 and the chain confirmation are drafts.
  Confirmation (finalists): R0 and the kept chain's final config, NARROW pool, 15,000 tries,
  8 FRESH paired seeds (7-14, never used in screening), parallel 3 each (both configs together = 6 processes); decided on
  arena-check-2 OVERALL. No config trains on the wide 11-41 pool.

Pilot configs (configs/ladder/pilot/) are a closed record and are no longer written here.
Recipes come from data/examples/ in the PINNED worktree; only the network/learning block is taken.
No config ever contains dqn.imitation.
"""
import argparse, copy, json, os
from pathlib import Path

P = Path(os.environ.get("MINOTAUR_ROOT", Path.home() / "Minotaur"))  # working root (ext4); D:\Minotaur is the mirror
EX = P / "worktrees" / "fresh" / "data" / "examples"
OUT = P / "configs" / "ladder" / "drafts"
NOT_RECIPE = ("shaping", "shaping_on_bump", "novelty_bonus", "revisit_penalty", "imitation")
NARROW = {"size": 11, "sizes": [11, 13, 15, 17], "maze_seed": 93000001,
          "train": 400, "validation": 80, "test": 80, "border_exit": True}
WIDER = {"sizes": [11, 13, 15, 17, 19, 21], "train": 600, "validation": 120, "test": 120}  # F4: 100/20/20 per size
EPISODES = 15000
SCREEN_SEEDS = list(range(1, 7))
CONFIRM_SEEDS = list(range(7, 15))  # FRESH seeds 7-14: seeds 1-6 selected the chain, and same seed = same run (TRAINING.md L129)


def r0():
    dqn = json.loads((EX / "dqn-mixed-learning-brain.json").read_text())["dqn"]
    dqn = {k: v for k, v in dqn.items() if k not in NOT_RECIPE}
    dqn.update(shaping=True, novelty_bonus=0.02, revisit_penalty=0.01)
    return {"name": "R0", "method": "dqn", "levels": {"generated": copy.deepcopy(NARROW)},
            "episodes": EPISODES, "eval_every": 250, "patience": 40, "wall_mask": True,
            "seed": 1, "seeds": SCREEN_SEEDS, "parallel": len(SCREEN_SEEDS), "dqn": dqn}


def s1(c): c["dqn"].update(learning_rate=0.0003, target_update=1000)
def s2(c): c["train_step_limit_factor"] = 2
def f1(c): c["observation"] = {"version": 2}
def f2(c): c["loop_stop"] = {"repeats": 3, "penalty": 0.5}; c["loop_escape"] = True
def f3(c): c["policy_epsilon"] = 0.1
def f4(c): c["levels"]["generated"].update(copy.deepcopy(WIDER))

RUNGS = [("S1", s1), ("S2", s2), ("F1", f1), ("F2", f2), ("F3", f3), ("F4", f4)]  # owner 2026-11-26 after R0; F4 LAST


def write(name, cfg):
    assert "imitation" not in json.dumps(cfg)
    assert 41 not in cfg["levels"]["generated"]["sizes"], "no config trains on the wide pool"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(cfg, indent=2) + "\n")
    print(f"{name}.json")


def confirm(cfg, name):
    c = copy.deepcopy(cfg)
    c.update(name=name, seed=CONFIRM_SEEDS[0], seeds=CONFIRM_SEEDS, parallel=3)
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dropped", default="")
    a = ap.parse_args()
    dropped = {x for x in a.dropped.split(",") if x}
    assert dropped <= {n for n, _ in RUNGS}, f"unknown rung in --dropped: {dropped}"

    base = r0(); write("R0", base)
    kept, chain = base, ["R0"]
    for name, change in RUNGS:
        cand = copy.deepcopy(kept); cand["name"] = name; change(cand)
        write(name, cand)
        if name not in dropped:
            kept = cand; chain.append(name)
    write("confirm-R0", confirm(base, "confirm-R0"))
    s1cfg = json.loads((OUT / "S1.json").read_text())
    c = confirm(s1cfg, "confirm-S1"); c.update(seeds=CONFIRM_SEEDS[:6]); write("confirm-S1", c)
    write("confirm-chain", confirm(kept, "confirm-chain"))
    print("kept chain:", " + ".join(chain))


if __name__ == "__main__":
    main()
