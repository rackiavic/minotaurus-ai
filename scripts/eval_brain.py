"""Score one brain on arena-check-2, greedy. Port of minotaur-research/2026-11-25-head-to-head/scripts/score.py.

Usage (run with the PINNED worktree's interpreter, isolated):
  /mnt/d/Minotaur/worktrees/fresh/.venv/bin/python -I eval_brain.py NAME BRAIN_ONNX OUT_JSON

Same episode() as B-mixed-s1's scorer (player seed f"{digest}|{level.id}", epsilon 0, greedy, step limit
of the level). Only change: MazeEnv gets the brain's obs_version (a v1 brain plays exactly as before).
Mazes: protocol/arena-check-2-mazes.json (400 border-exit mazes, sizes 11-41, seeds from 9,100,000),
rebuilt from their ids with the pinned generator and checked against the frozen grids.
The final-test set and the hand-made levels are NOT played here (test pile: once, final config only).
"""
import hashlib, json, os, sys, warnings
from collections import Counter
from pathlib import Path

MAZES = Path("/mnt/d/Minotaur/protocol/arena-check-2-mazes.json")
BANDS = {"11-17": (11, 13, 15, 17), "21-25": (21, 25), "31-41": (31, 41)}


def episode(brain, level):
    from minotaurus.brain import obs_version_of, player
    from minotaurus.engine import MazeEnv
    from minotaurus.engine.levels import shortest_path_length
    mover = player(brain, seed=f"{brain.digest}|{level.id}", epsilon=0.0)
    env = MazeEnv(level, obs_version=obs_version_of(mover)); obs, _ = env.reset()
    seen = Counter(); bumps = 0; done = finished = False
    while not done:
        seen[(env.pos, obs.tobytes())] += 1
        obs, _, term, trunc, info = env.step(mover(obs))
        bumps += info["bumped"]; finished, done = term, term or trunc
    return {"level": level.id, "size": level.width, "finished": bool(finished), "steps": env.steps,
            "shortest": shortest_path_length(level), "bumps": bumps, "longest_repeat": max(seen.values())}


def main():
    name, path, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    from minotaurus.brain import BrainWarning, load_brain
    from minotaurus.engine.generate import generated_level_from_id
    frozen = json.loads(MAZES.read_text())
    levels = []
    for size in sorted(frozen, key=int):
        for m in frozen[size]:
            lv = generated_level_from_id(m["id"])
            assert list(lv.grid) == m["grid"], f"maze {m['id']} differs from the frozen grid"
            levels.append(lv)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", BrainWarning)
        brain = load_brain(path, time_limit_s=1.0)
    rows = [episode(brain, lv) for lv in levels]
    by = {}
    for r in rows:
        by.setdefault(r["size"], []).append(r["finished"])
    res = {"name": name, "brain": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
           "mazes_sha256": hashlib.sha256(MAZES.read_bytes()).hexdigest(),
           "overall": sum(r["finished"] for r in rows) / len(rows), "n": len(rows),
           "by_size": {str(k): sum(v) / len(v) for k, v in sorted(by.items())},
           "bands": {b: sum(sum(by[s]) for s in ss) / sum(len(by[s]) for s in ss) for b, ss in BANDS.items()},
           "rows": rows}
    tmp = out.with_suffix(".tmp"); tmp.write_text(json.dumps(res, indent=1)); os.replace(tmp, out)
    print(name, "overall", round(100 * res["overall"], 1), {b: round(100 * v, 1) for b, v in res["bands"].items()})


if __name__ == "__main__":
    main()
