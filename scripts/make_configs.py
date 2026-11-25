"""Write every ladder config from one place, so arms and rungs differ only where intended.

  python3 make_configs.py [--dropped R2,R4] [--episodes 4000]

One track, "Documented" (owner decision 2026-11-25). Cumulative ladder, one change per rung:
  R0 r3, eval_every default (250)   R1 shaping            R2 wall_mask      R3 border_exit
  R4 novelty+revisit (NON-potential-based)                R5 policy_epsilon 0.1
  R6 patience 40     R7 observation.version 2             R8 loop_stop+loop_escape (NON-potential-based)
Each rung Rk is applied to the last KEPT config before it. `--dropped` lists rungs the decision
rule dropped; until results exist, every rung is assumed kept and files are written as drafts.
Screening configs use 4,000 episodes x 8 seeds; finalists use 15,000 (`--episodes 15000`).

Pilot configs (arms A, B, C) are always written to configs/ladder/pilot/.
Recipes come from data/examples/ in the PINNED worktree; only the network/learning block is taken.
No config ever contains dqn.imitation.
"""
import argparse, copy, json
from pathlib import Path

EX = Path("/mnt/d/Minotaur/worktrees/fresh/data/examples")
OUT = Path("/mnt/d/Minotaur/configs/ladder")
NOT_RECIPE = ("shaping", "shaping_on_bump", "novelty_bonus", "revisit_penalty", "imitation")
SOURCES = {"dqn-brain": "dqn-brain.json", "r3": "dqn-mixed-learning-brain.json"}
POOLS = {"size": 11, "sizes": [11, 13, 15, 17, 21, 25, 31, 41], "maze_seed": 93000001,
         "train": 800, "validation": 160, "test": 160}


def recipe(key):
    dqn = json.loads((EX / SOURCES[key]).read_text())["dqn"]
    return {k: v for k, v in dqn.items() if k not in NOT_RECIPE}


def base(name, key, episodes, seeds):
    # eval_every left out on purpose: the documented default (250) applies.
    return {"name": name, "method": "dqn", "levels": {"generated": copy.deepcopy(POOLS)},
            "episodes": episodes, "seed": seeds[0], "seeds": seeds, "parallel": len(seeds),
            "dqn": recipe(key)}


def r1(c): c["dqn"]["shaping"] = True
def r2(c): c["wall_mask"] = True
def r3_(c): c["levels"]["generated"]["border_exit"] = True
def r4(c): c["dqn"].update(novelty_bonus=0.02, revisit_penalty=0.01)
def r5(c): c["policy_epsilon"] = 0.1
def r6(c): c["patience"] = 40
def r7(c): c["observation"] = {"version": 2}
def r8(c): c["loop_stop"] = {"repeats": 3, "penalty": 0.5}; c["loop_escape"] = True

RUNGS = [("R1", r1), ("R2", r2), ("R3", r3_), ("R4", r4), ("R5", r5), ("R6", r6), ("R7", r7), ("R8", r8)]


def write(path, cfg):
    assert "imitation" not in json.dumps(cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cfg, indent=2) + "\n")
    print(path.relative_to(OUT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dropped", default="")
    ap.add_argument("--episodes", type=int, default=4000)
    a = ap.parse_args()
    dropped = {x for x in a.dropped.split(",") if x}

    # pilot (pre-registered): A dqn-brain as-is, B r3, C r3 + shaping
    pa = base("pilot-dqn-brain", "dqn-brain", 4000, [1, 2])
    pa["dqn"] = json.loads((EX / "dqn-brain.json").read_text())["dqn"]
    write(OUT / "pilot" / "pilot-dqn-brain.json", pa)
    write(OUT / "pilot" / "pilot-r3.json", base("pilot-r3", "r3", 4000, [1, 2]))
    pc = base("pilot-r3-shaping", "r3", 4000, [1, 2]); pc["dqn"]["shaping"] = True
    write(OUT / "pilot" / "pilot-r3-shaping.json", pc)

    seeds = list(range(1, 9)); ep = a.episodes; tag = f"-{ep // 1000}k"
    kept = base(f"R0{tag}", "r3", ep, seeds)
    write(OUT / "drafts" / f"R0{tag}.json", kept)
    for name, change in RUNGS:
        cand = copy.deepcopy(kept); cand["name"] = f"{name}{tag}"; change(cand)
        write(OUT / "drafts" / f"{name}{tag}.json", cand)
        if name not in dropped:
            kept = cand

    # reference: B-mixed-s1 recipe verbatim, paired pools and seeds
    ref = json.loads(Path("/home/rkhrk/minotaur-research/2026-11-25-head-to-head/release/B-mixed-s1-config.json").read_text())
    for k in ("train_step_limit_factor", "stages"):
        ref.pop(k, None)
    ref.update(name="ref-b-mixed", seeds=seeds, parallel=8)
    ref["levels"]["generated"] = dict(copy.deepcopy(POOLS), border_exit=True)
    write(OUT / "drafts" / "ref-b-mixed.json", ref)


if __name__ == "__main__":
    main()
