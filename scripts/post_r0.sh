#!/usr/bin/env bash
# After R0 (owner approval 2026-11-26: R0 ONLY). Waits for runs/R0/manifest.json to get an end time
# (no process matching, so it cannot see itself), then: clean-finish check -> eval_brain on all 6
# seeds -> verify_bundles (after eval, so the eval sha256 is checked) -> R0 table + gate -> drift
# check -> mirror to D: + push. Any failure goes to logs/ALERT.txt (the mirror still runs).
# It NEVER starts F1 or any later rung.   Start: tmux new -d -s post-r0 ~/Minotaur/scripts/post_r0.sh
P=${MINOTAUR_ROOT:-$HOME/Minotaur}; export MINOTAUR_ROOT=$P
PY=$P/worktrees/fresh/.venv/bin/python; LOG=$P/logs/post_r0.log; R=R0; M=$P/runs/$R/manifest.json
finish(){ [[ -n ${POST_R0_TEST:-} ]] && { echo "TEST: mirror skipped"; touch "$P/logs/R0-DONE"; exit "$1"; }; "$P/scripts/mirror_to_d.sh" >> "$LOG" 2>&1 || echo "$(date -Iseconds) mirror failed (see logs/post_r0.log)" >> "$P/logs/ALERT.txt"; touch "$P/logs/R0-DONE"; exit "$1"; }
alert(){ { echo "$(date -Iseconds) POST-R0 STOPPED: $1"; [[ -n "${2:-}" ]] && tail -20 "$2"; } >> "$P/logs/ALERT.txt"; echo "ALERT: $1" >> "$LOG"; finish 1; }
exec >> "$LOG" 2>&1
echo "== waiting for $R $(date -Iseconds)"
until [[ -f $M ]] && python3 -c "import json,sys;sys.exit(0 if json.load(open('$M')).get('end') else 1)"; do sleep 60; done
echo "== $R ended $(date -Iseconds)"
python3 -c "import json,sys;sys.exit(0 if json.load(open('$M')).get('exit_code')==0 else 1)" || alert "$R did not finish cleanly (see runs/$R/manifest.json, logs/train-$R.log)"
n_seeds=0
for sd in $(find "$P/runs/$R" -type d -name 'seed-*' | sort -t- -k2 -n); do
  n=${sd##*seed-}; n_seeds=$((n_seeds+1))
  [[ -f $sd/brain.onnx ]] || alert "$R seed $n has no brain.onnx"
  (cd "$P/logs" && "$PY" -I "$P/scripts/eval_brain.py" "$R-s$n" "$sd/brain.onnx" "$P/runs/$R/ac2-s$n.json") || alert "eval_brain.py failed on $R seed $n"
done
(( n_seeds == ${R0_SEEDS:-6} )) || alert "$R: expected ${R0_SEEDS:-6} seed folders, found $n_seeds"
"$PY" -I "$P/scripts/verify_bundles.py" "$P/runs/$R" --expect-unsigned > "$P/logs/bundles-$R.md" 2>&1 || alert "verify_bundles.py failed on $R" "$P/logs/bundles-$R.md"
python3 "$P/scripts/rung_table.py" "$R" --seeds ${R0_SEEDS:-6} --gate > "$P/logs/$R-table.out" 2>&1 || alert "$R table cannot be produced" "$P/logs/$R-table.out"
"$P/scripts/drift_check.sh" --log || echo "$(date -Iseconds) drift CHANGED-RELEVANT after $R (see logs/drift.log)" >> "$P/logs/ALERT.txt"
echo "== $R table written $(date -Iseconds); no later rung started"
finish 0
