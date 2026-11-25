#!/usr/bin/env bash
# RAM guard: every 10 min append `free -m` to logs/ram.log. If available memory < 1024 MB, stop ONE
# arm (pilot-c first, then pilot-b) with Ctrl-C (launch.sh then records end + exit code), note it
# in that run's manifest, and write logs/RAM-ALERT.txt. At most one arm is stopped per check.
# Start: tmux new -d -s ramguard /mnt/d/Minotaur/scripts/ram_guard.sh
P=/mnt/d/Minotaur
ORDER=("pilot-c:pilot-r3-shaping" "pilot-b:pilot-r3")
while true; do
  NOW=$(date -Iseconds)
  { echo "== $NOW"; free -m; } >> "$P/logs/ram.log"
  AVAIL=$(free -m | awk '/^Mem:/{print $7}')
  if (( AVAIL < 1024 )); then
    for pair in "${ORDER[@]}"; do
      S=${pair%%:*}; RUN=${pair#*:}
      if tmux has-session -t "$S" 2>/dev/null && pgrep -f "configs/ladder/pilot/$RUN.json" >/dev/null; then
        tmux send-keys -t "$S" C-c
        python3 - "$P/runs/$RUN/manifest.json" "$NOW" "$AVAIL" <<'EOF'
import json, sys
p, t, a = sys.argv[1:4]
d = json.load(open(p)); d["ram_guard_stopped"] = {"at": t, "available_mb": int(a)}
json.dump(d, open(p, "w"), indent=2)
EOF
        echo "$NOW available ${AVAIL} MB < 1024: stopped $S ($RUN)" | tee -a "$P/logs/ram.log" >> "$P/logs/RAM-ALERT.txt"
        break
      fi
    done
  fi
  sleep 600
done
