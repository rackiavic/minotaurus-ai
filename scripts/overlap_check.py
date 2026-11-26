"""Wall layouts shared between a config's practice/check/test pools and the frozen evaluation sets.

  $MINOTAUR_ROOT/worktrees/fresh/.venv/bin/python -I overlap_check.py CONFIG.json [...]

Evaluation sets: protocol/arena-check-2-mazes.json (400) and the final-test layouts
(~/minotaur-research/2026-11-25-head-to-head/final-test-mazes.json, 200, read-only; only the wall
layouts are read, never any score). Both are rebuilt from their ids with the pinned generator and
compared with walls(), the same function the pools use. Exit 1 if any layout is shared.
"""
import json, os, sys
from pathlib import Path
from minotaurus.engine.generate import generated_level_from_id
from minotaurus.engine.pools import walls
from minotaurus.trainer.config import ConfigFile

P = Path(os.environ.get("MINOTAUR_ROOT", Path.home() / "Minotaur"))  # working root (ext4); D:\Minotaur is the mirror
SETS = {"arena-check-2": P / "protocol" / "arena-check-2-mazes.json",
        "final-test": Path.home() / "minotaur-research/2026-11-25-head-to-head/final-test-mazes.json"}


def layouts(path):
    out = set()
    for ms in json.loads(path.read_text()).values():
        for m in ms:
            lv = generated_level_from_id(m["id"]); assert list(lv.grid) == m["grid"]
            out.add(walls(lv))
    return out


ev = {n: layouts(p) for n, p in SETS.items()}
bad = 0
for f in sys.argv[1:]:
    cfg = json.loads(Path(f).read_text()); cfg.pop("seeds", None); cfg.pop("parallel", None)
    pools = ConfigFile.model_validate(cfg).resolve_pools()
    for pool in ("train", "validation", "test"):
        lv = getattr(pools, pool)
        per = {s: sum(l.width == s for l in lv) for s in sorted({l.width for l in lv})}
        lay = {walls(l) for l in lv}
        shared = {n: len(lay & s) for n, s in ev.items()}
        bad += sum(shared.values())
        print(f"{Path(f).name} {pool}: {len(lv)} mazes {per}; shared {shared}")
sys.exit(1 if bad else 0)
