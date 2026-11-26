#!/usr/bin/env bash
# After the pilot: score -> bundle checks -> pilot table -> (only if all pass) benchmark.
# GUARD (owner, 2026-11-25): if eval_brain.py or verify_bundles.py fails on any run, or the pilot
# table cannot be produced, the benchmark is NOT started: the failure goes to logs/ALERT.txt and
# the script stops. Run in tmux:  tmux new -d -s post ~/Minotaur/scripts/post_pilot.sh
P=${MINOTAUR_ROOT:-$HOME/Minotaur}; export MINOTAUR_ROOT=$P  # working root (ext4); D:\Minotaur is the mirror
 PY=$P/worktrees/fresh/.venv/bin/python; LOG=$P/logs/post_pilot.log
RUNS=(pilot-dqn-brain pilot-r3 pilot-r3-shaping)
alert(){ { echo "$(date -Iseconds) POST-PILOT STOPPED, benchmark NOT started: $1"; [[ -n "${2:-}" ]] && tail -20 "$2"; } >> "$P/logs/ALERT.txt"; echo "ALERT: $1" | tee -a "$LOG"; exit 1; }
exec >> "$LOG" 2>&1
echo "== start $(date -Iseconds)"

for r in "${RUNS[@]}"; do
  python3 -c "import json,sys;d=json.load(open('$P/runs/$r/manifest.json'));sys.exit(0 if d.get('end') and d.get('exit_code')==0 else 1)" \
    || alert "$r did not finish cleanly (see runs/$r/manifest.json)"
done

# 1. arena-check-2 + size bands for every seed's brain.onnx
for r in "${RUNS[@]}"; do
  n_seeds=0
  for sd in $(find "$P/runs/$r" -type d -name 'seed-*' | sort); do
    n=${sd##*seed-}; n_seeds=$((n_seeds+1))
    [[ -f $sd/brain.onnx ]] || alert "$r seed $n has no brain.onnx"
    (cd "$P/logs" && "$PY" -I "$P/scripts/eval_brain.py" "$r-s$n" "$sd/brain.onnx" "$P/runs/$r/ac2-s$n.json") \
      || alert "eval_brain.py failed on $r seed $n"
  done
  (( n_seeds == 2 )) || alert "$r: expected 2 seed folders, found $n_seeds"
done

# 2. bundle checks (after eval, so the eval sha256 is checked too)
for r in "${RUNS[@]}"; do
  "$PY" -I "$P/scripts/verify_bundles.py" "$P/runs/$r" --expect-unsigned > "$P/logs/bundles-$r.md" 2>&1 \
    || alert "verify_bundles.py failed on $r" "$P/logs/bundles-$r.md"
done

# 3. pilot table + pre-registered decision
python3 "$P/scripts/pilot_table.py" > "$P/logs/pilot_table.out" 2>&1 || alert "pilot table cannot be produced" "$P/logs/pilot_table.out"
echo "pilot table written $(date -Iseconds)"

# 4. drift check before the benchmark batch
"$P/scripts/drift_check.sh" --log || alert "drift CHANGED-RELEVANT before benchmark"

# 5. benchmark: batch 1 (6 at once), then batch 2 (base alone)
"$P/scripts/bench.sh" batch1 bench-base bench-sizes-11-25 bench-sizes-11-17 bench-factor-2 bench-factor-3 bench-batch-32
"$P/scripts/bench.sh" batch2 bench-base-solo
echo "== all done $(date -Iseconds)"
touch "$P/logs/POST-PILOT-DONE"
