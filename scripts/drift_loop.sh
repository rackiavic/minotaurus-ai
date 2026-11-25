#!/usr/bin/env bash
# Background drift guard during runs: every 30 min, log to logs/drift.log.
# On CHANGED-RELEVANT: mark every manifest of a running/finished run STALE (adds a field; never kills
# jobs, never pulls) and write logs/DRIFT-ALERT.txt for the human to see.
# Start:  tmux new -d -s drift /mnt/d/Minotaur/scripts/drift_loop.sh
P=/mnt/d/Minotaur
while true; do
  if ! out=$("$P/scripts/drift_check.sh" --log 2>&1); then
    if [[ $(head -1 <<<"$out") == CHANGED-RELEVANT ]]; then
      { date -Iseconds; echo "$out"; } > "$P/logs/DRIFT-ALERT.txt"
      for m in "$P"/runs/*/manifest.json "$P"/runs/*/*/manifest.json; do
        [[ -f "$m" ]] || continue
        python3 - "$m" "$(date -Iseconds)" <<'EOF'
import json, sys
p, t = sys.argv[1], sys.argv[2]
d = json.load(open(p))
if d.get("drift_status") != "STALE":
    d["drift_status"] = "STALE"; d["stale_since"] = t
    json.dump(d, open(p, "w"), indent=2)
EOF
      done
    else
      echo "$(date -Iseconds) ERROR $out" >> "$P/logs/drift.log"
    fi
  fi
  sleep 1800
done
