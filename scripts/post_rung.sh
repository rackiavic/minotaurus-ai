#!/usr/bin/env bash
# After one approved rung. Usage: post_rung.sh NAME KEPT   (e.g. post_rung.sh S1 R0). Waits for runs/NAME/manifest.json to get an end time
# (no process matching, so it cannot see itself), then: clean-finish check -> eval_brain on all 6
# seeds -> verify_bundles (after eval, so the eval sha256 is checked) -> rung table + paired decision vs KEPT -> drift
# check -> mirror to D: + push. Any failure goes to logs/ALERT.txt (the mirror still runs).
# Decision: rung_table.py NAME --compare KEPT (arena-check-2 overall). It NEVER starts another rung.
# Start: tmux new -d -s post-s1 "~/Minotaur/scripts/post_rung.sh S1 R0"
P=${MINOTAUR_ROOT:-$HOME/Minotaur}; export MINOTAUR_ROOT=$P
PY=$P/worktrees/fresh/.venv/bin/python; R=${1:?NAME}; KEPT=${2:?KEPT}; LOG=$P/logs/post_$R.log; M=$P/runs/$R/manifest.json
finish(){ [[ -n ${POST_RUNG_TEST:-} ]] && { echo "TEST: mirror skipped"; touch "$P/logs/$R-DONE"; exit "$1"; }; "$P/scripts/mirror_to_d.sh" >> "$LOG" 2>&1 || echo "$(date -Iseconds) mirror failed (see logs/post_$R.log)" >> "$P/logs/ALERT.txt"; touch "$P/logs/$R-DONE"; exit "$1"; }
alert(){ { echo "$(date -Iseconds) POST-RUNG $R STOPPED: $1"; [[ -n "${2:-}" ]] && tail -20 "$2"; } >> "$P/logs/ALERT.txt"; echo "ALERT: $1" >> "$LOG"; finish 1; }
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
(( n_seeds == ${RUNG_SEEDS:-6} )) || alert "$R: expected ${RUNG_SEEDS:-6} seed folders, found $n_seeds"
"$PY" -I "$P/scripts/verify_bundles.py" "$P/runs/$R" --expect-unsigned > "$P/logs/bundles-$R.md" 2>&1 || alert "verify_bundles.py failed on $R" "$P/logs/bundles-$R.md"
"$PY" -I "$P/scripts/check_inputs.py" "$P/runs/$R" > "$P/logs/inputs-$R.md" 2>&1 || alert "brain input size does not match the config on $R" "$P/logs/inputs-$R.md"
python3 "$P/scripts/rung_table.py" "$R" --seeds ${RUNG_SEEDS:-6} --compare "$KEPT" > "$P/logs/$R-table.out" 2>&1 || alert "$R table cannot be produced" "$P/logs/$R-table.out"
"$P/scripts/drift_check.sh" --log || echo "$(date -Iseconds) drift CHANGED-RELEVANT after $R (see logs/drift.log)" >> "$P/logs/ALERT.txt"
echo "== $R table written $(date -Iseconds); no later rung started"
finish 0
