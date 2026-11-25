"""Write every ladder config from one place, so arms and rungs differ only where intended.

  python3 make_configs.py RECIPE      RECIPE = dqn-brain | r3 | wide-stable  (the Rung 0 recipe)

Pilot configs are always written (both arms). Rung 0 and the S/F rungs use RECIPE; until the pilot
has decided, they are written to configs/ladder/drafts/ with "provisional" in the file name.
Recipes are copied from data/examples/ in the PINNED worktree. Only the network/learning block is
taken from them: for r3 and wide-stable, shaping / novelty / revisit / wall_mask / patience /
border_exit are left out, because those are rungs of their own.
"""
import copy, json, sys
from pathlib import Path

EX = Path("/mnt/d/Minotaur/worktrees/fresh/data/examples")
OUT = Path("/mnt/d/Minotaur/configs/ladder")
NOT_RECIPE = ("shaping", "shaping_on_bump", "novelty_bonus", "revisit_penalty", "imitation")
SOURCES = {"dqn-brain": "dqn-brain.json", "r3": "dqn-mixed-learning-brain.json",
           "wide-stable": "dqn-mixed-wide-stable-brain.json"}
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


def write(path, cfg):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cfg, indent=2) + "\n")
    print(path.relative_to(OUT))


def main():
    key = sys.argv[1]
    # pilot: dqn-brain as-is (its dqn block is copied whole) + the approved candidate
    pilot_a = base("pilot-dqn-brain", "dqn-brain", 4000, [1, 2])
    pilot_a["dqn"] = json.loads((EX / "dqn-brain.json").read_text())["dqn"]
    write(OUT / "pilot" / "pilot-dqn-brain.json", pilot_a)
    for cand in ("r3", "wide-stable"):
        write(OUT / "pilot" / f"pilot-{cand}.json", base(f"pilot-{cand}", cand, 4000, [1, 2]))

    seeds = list(range(1, 9))
    tag = "" if (OUT / "pilot" / "DECIDED").exists() else "-provisional"
    d = OUT / ("" if not tag else "drafts")
    r0a = base("rung0a", key, 4000, seeds); write(d / f"rung0a{tag}.json", r0a)
    r0 = base("rung0b", key, 15000, seeds); write(d / f"rung0b{tag}.json", r0)
    # Strict: S1 wall_mask -> S2 border_exit -> S3 policy_epsilon + patience
    s1 = copy.deepcopy(r0); s1["name"] = "S1"; s1["wall_mask"] = True
    s2 = copy.deepcopy(s1); s2["name"] = "S2"; s2["levels"]["generated"]["border_exit"] = True
    s3 = copy.deepcopy(s2); s3["name"] = "S3"; s3["policy_epsilon"] = 0.1; s3["patience"] = 8
    # Full-documented: F1 shaping -> F2 novelty+revisit -> F3 obs v2 -> F4 loop_stop+loop_escape
    f1 = copy.deepcopy(r0); f1["name"] = "F1"; f1["dqn"]["shaping"] = True
    f2 = copy.deepcopy(f1); f2["name"] = "F2"; f2["dqn"].update(novelty_bonus=0.02, revisit_penalty=0.01)
    f3 = copy.deepcopy(f2); f3["name"] = "F3"; f3["observation"] = {"version": 2}
    f4 = copy.deepcopy(f3); f4["name"] = "F4"; f4["loop_stop"] = {"repeats": 3, "penalty": 0.5}; f4["loop_escape"] = True
    for c in (s1, s2, s3, f1, f2, f3, f4):
        write(OUT / "drafts" / f"{c['name']}{tag}.json", c)
    # reference: B-mixed-s1 recipe verbatim, paired pools and seeds
    ref = json.loads(Path("/home/rkhrk/minotaur-research/2026-11-25-head-to-head/release/B-mixed-s1-config.json").read_text())
    for k in ("train_step_limit_factor", "stages"):
        ref.pop(k, None)
    ref.update(name="full-ref", seeds=seeds, parallel=8)
    ref["levels"]["generated"] = dict(copy.deepcopy(POOLS), border_exit=True)
    write(OUT / "drafts" / "full-ref.json", ref)


if __name__ == "__main__":
    main()
