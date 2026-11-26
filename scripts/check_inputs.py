"""Every seed's brain.onnx takes the input the run's config asks for.

  $MINOTAUR_ROOT/worktrees/fresh/.venv/bin/python -I check_inputs.py RUN_DIR   (exit 1 on any mismatch)

Expected length = obs_size(5, observation.version) from runs/<name>/config.submitted.json (77 for v1,
82 for v2). Checked twice per seed: the ONNX graph's input shape, and the obs version the pinned
loader reads from the brain (obs_version_of), plus one forward pass of that length.
"""
import json, sys, warnings
from pathlib import Path
import numpy as np, onnx
from minotaurus.brain import BrainWarning, load_brain, obs_version_of
from minotaurus.engine.observe import obs_size

run = Path(sys.argv[1])
cfg = json.loads((run / "config.submitted.json").read_text())
ver = (cfg.get("observation") or {}).get("version", 1); want = obs_size(5, ver)
bad = 0
print(f"| seed | onnx input shape | loader obs version | forward pass ({want}) | ok |\n|---|---|---|---|---|")
for sd in sorted(run.glob("**/seed-*"), key=lambda p: int(p.name.split("-")[1])):
    f = sd / "brain.onnx"
    dims = [d.dim_value or d.dim_param for d in onnx.load(str(f)).graph.input[0].type.tensor_type.shape.dim]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", BrainWarning)
        b = load_brain(f, time_limit_s=1.0)
    lv = obs_version_of(b)
    try:
        b(np.zeros(want, dtype=np.float32)); fp = "ok"
    except Exception as e:  # noqa: BLE001
        fp = f"FAIL {type(e).__name__}"
    ok = dims[-1] == want and lv == ver and fp == "ok"; bad += not ok
    print(f"| {sd.name} | {dims} | {lv} | {fp} | {ok} |")
print(f"\nexpected: observation version {ver}, {want} inputs")
sys.exit(1 if bad else 0)
