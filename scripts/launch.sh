#!/usr/bin/env bash
# Launch one approved config from the PINNED worktree, with a manifest. Run inside tmux.
# Usage: launch.sh CONFIG_JSON
# Refuses to start if: drift is CHANGED-RELEVANT, worktree HEAD != pinned SHA, worktree dirty,
# or TRAINING.md / uv.lock hashes differ from pinned.json.
set -euo pipefail
P=/mnt/d/Minotaur; WT=$P/worktrees/fresh; CFG=$(realpath "$1"); NAME=$(basename "$CFG" .json)
PIN=$P/protocol/pinned.json
get(){ python3 -c "import json;print(json.load(open('$PIN'))['$1'])"; }

"$P/scripts/drift_check.sh" --log || { echo "drift CHANGED-RELEVANT: not launching"; exit 2; }
[[ $(git -C "$WT" rev-parse HEAD) == $(get pinned_sha) ]] || { echo "worktree not at pinned SHA"; exit 3; }
[[ -z $(git -C "$WT" status --porcelain --untracked-files=no) ]] || { echo "worktree dirty"; exit 3; }
[[ $(sha256sum "$WT/TRAINING.md" | cut -d' ' -f1) == $(get training_md_sha256) ]] || { echo "TRAINING.md hash"; exit 3; }
[[ $(sha256sum "$WT/uv.lock" | cut -d' ' -f1) == $(get uv_lock_sha256) ]] || { echo "uv.lock hash"; exit 3; }

RUN=$P/runs/$NAME; mkdir -p "$RUN"; cp "$CFG" "$RUN/config.submitted.json"
M=$RUN/manifest.json
python3 - "$M" "$CFG" "$PIN" <<'EOF'
import json, sys, hashlib, platform, os, subprocess, datetime
m, cfg, pin = sys.argv[1:4]; p = json.load(open(pin)); c = json.load(open(cfg))
mem = open('/proc/meminfo').readline().split()[1]
json.dump({
  "name": c["name"], "pinned_sha": p["pinned_sha"], "training_md_sha256": p["training_md_sha256"],
  "uv_lock_sha256": p["uv_lock_sha256"], "config_path": cfg,
  "config_sha256": hashlib.sha256(open(cfg,'rb').read()).hexdigest(),
  "seeds": c.get("seeds", [c["seed"]]), "maze_seed": c["levels"]["generated"]["maze_seed"],
  "sizes": c["levels"]["generated"].get("sizes"), "episodes": c["episodes"],
  "hardware": {"nproc": os.cpu_count(), "mem_kb": int(mem), "kernel": platform.release(),
               "cpu": subprocess.run(["sh","-c","grep -m1 'model name' /proc/cpuinfo | cut -d: -f2"],capture_output=True,text=True).stdout.strip()},
  "start": datetime.datetime.now().astimezone().isoformat(), "end": None, "exit_code": None,
  "drift_status": "SAME", "stale_since": None}, open(m, "w"), indent=2)
EOF

cd "$WT"
set +e
/usr/bin/time -v uv run --frozen minotaurus train --config "$CFG" --runs-dir "$RUN" > "$P/logs/train-$NAME.log" 2> "$P/logs/time-$NAME.log"
RC=$?
set -e
python3 - "$M" "$RC" <<'EOF'
import json, sys, datetime
m, rc = sys.argv[1], int(sys.argv[2]); d = json.load(open(m))
d["end"] = datetime.datetime.now().astimezone().isoformat(); d["exit_code"] = rc
json.dump(d, open(m, "w"), indent=2)
EOF
"$P/scripts/drift_check.sh" --log || true
echo "$NAME finished rc=$RC"
