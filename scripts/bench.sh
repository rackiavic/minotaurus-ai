#!/usr/bin/env bash
# Benchmark (owner request 2026-11-25): r3 recipe, 300 tries, nice 0.
# Usage: bench.sh BATCH_LABEL NAME [NAME ...]
#   All NAMEs (configs/bench/<NAME>.json) start AT ONCE (one batch, real contention); for an
#   uncontended reference pass a single NAME. Never more than 6 at once (owner: no 12-process run).
# Each config runs through launch.sh (pinned code, drift check, manifest, unsigned). A sampler
# records every 2 s, per run: rows and steps in each seed's metrics.jsonl; plus RSS of every
# pinned-venv python process and MemAvailable -> logs/bench-<BATCH_LABEL>.samples.jsonl.
# Rates use only the span between a run's first and last metrics row, so uv start-up and
# end-of-run scoring are not counted.
P=${MINOTAUR_ROOT:-$HOME/Minotaur}; export MINOTAUR_ROOT=$P  # working root (ext4); D:\Minotaur is the mirror
LABEL=$1; shift
(( $# <= 6 )) || { echo "refusing: more than 6 concurrent runs"; exit 2; }
S=$P/logs/bench-$LABEL.samples.jsonl; : > "$S"
PIDS=()
for NAME in "$@"; do
  "$P/scripts/launch.sh" "$P/configs/bench/$NAME.json" > "$P/logs/bench-$NAME.launch.log" 2>&1 &
  PIDS+=($!)
  sleep 5  # stagger: each launch.sh runs `git fetch` in repo/; simultaneous fetches can hit a ref lock
done
alive(){ for p in "${PIDS[@]}"; do kill -0 "$p" 2>/dev/null && return 0; done; return 1; }
while alive; do
  python3 - "$S" "$@" <<'EOF'
import json, sys, time, glob, subprocess, os
out, names = sys.argv[1], sys.argv[2:]
runs = {}
for n in names:
    seeds = {}
    for m in glob.glob(f"{os.environ['MINOTAUR_ROOT']}/runs/{n}/**/seed-*/metrics.jsonl", recursive=True):
        rows = [json.loads(l) for l in open(m) if l.strip()]
        tr = [r for r in rows if "avg_steps" in r]
        seeds[m.split("/")[-2]] = {"episode": max([r["episode"] for r in tr], default=0),
                                   "steps": sum(r["avg_steps"] * 10 for r in tr),
                                   "success": [r["success_rate"] for r in tr]}
    runs[n] = seeds
ps = subprocess.run(["ps", "-eo", "rss,args"], capture_output=True, text=True).stdout.splitlines()
rss = [(int(l.split()[0]), l.split(None, 1)[1][:160]) for l in ps[1:] if "/worktrees/fresh/.venv/bin/python" in l]
avail = int(open("/proc/meminfo").read().split("MemAvailable:")[1].split()[0])
open(out, "a").write(json.dumps({"t": time.time(), "runs": runs, "rss": rss, "avail_kb": avail}) + "\n")
EOF
  sleep 2
done
echo "batch $LABEL done $(date -Iseconds)"
