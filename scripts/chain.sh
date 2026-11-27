#!/usr/bin/env bash
# Pre-registered conditional chain (owner, 2026-11-27, before any F6 result). Runs inside tmux, not
# from a chat session:   tmux new -d -s chain ~/Minotaur/scripts/chain.sh
#   (a) F6 = F5 + sizes odd 11-31, judged vs F5 (post_rung.sh F6 F5 -> rung_table --compare F5).
#   (b) F3 = retained base + policy_epsilon 0.1: F3-on-F6 if F6 is KEEP, else F3-on-F5, judged vs that base.
#   (c) STOP. Never starts F2, confirmation or the final test. Writes reports/chain-summary.md.
# Abort (logs/ALERT.txt, start nothing further, never auto-resume) on: any run failure (launch refused,
# exit code != 0, post_rung.sh failure), RAM guard trip (logs/RAM-ALERT.txt), drift CHANGED-RELEVANT
# (logs/DRIFT-ALERT.txt or a drift line in ALERT.txt), or more than 3 of 6 seeds collapsed in F6.
# Each rung is launched in its own tmux session (f6, f3) so the RAM guard can stop it with Ctrl-C:
#   ram_guard.sh f6:F6 f3:F3-on-F6 f3:F3-on-F5
# CHAIN_TEST=1: no launch, no post_rung, no commit, no mirror; exercises the decision on existing
# tables (RUNG1=F5 vs BASE0=F4 by default) and writes the summary to logs/chain-test-summary.md.
set -uo pipefail
P=${MINOTAUR_ROOT:-$HOME/Minotaur}; export MINOTAUR_ROOT=$P
T=${CHAIN_TEST:-}; RUNG1=${RUNG1:-F6}; BASE0=${BASE0:-F5}
[[ -n $T ]] && { RUNG1=${RUNG1_TEST:-F5}; BASE0=${BASE0_TEST:-F4}; }
LOG=$P/logs/chain${T:+-test}.log; STATE=$P/logs/chain${T:+-test}-state.json
WT=$P/worktrees/work; APP=$P/configs/ladder/approved
exec >> "$LOG" 2>&1
say(){ echo "$(date -Iseconds) $*"; }
SUMMARY=$P/reports/chain-summary.md; [[ -n $T ]] && SUMMARY=$P/logs/chain-test-summary.md

summary(){  # $1 = status line; reads every rung recorded in STATE
  python3 - "$STATE" "$P" "$SUMMARY" "$1" <<'EOF'
import json, sys, datetime as dt
from pathlib import Path
st, P, out, status = json.load(open(sys.argv[1])), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
t0 = dt.datetime.fromisoformat(st["started"]); low = None
blk = None
for line in (P / "logs/ram.log").read_text().splitlines():  # min MemAvailable since the chain started
    if line.startswith("== "):
        try: blk = dt.datetime.fromisoformat(line[3:].strip())
        except ValueError: blk = None
    elif line.startswith("Mem:") and blk and blk >= t0:
        a = int(line.split()[6]); low = a if low is None else min(low, a)
L = ["# Conditional chain summary (owner pre-registration 2026-11-27; F6 then F3, then STOP)", "",
     f"Status: **{status}**", "", f"Chain started {st['started']}; summary written {dt.datetime.now().astimezone().isoformat()}.",
     "**Label: provisional base, departure from rule.** Every base here is built on S1 (formally DROP vs R0); the S1 re-test vs R0 on fresh seeds 7-12 is still owed.", "",
     "| Rung | Judged vs | Start | End | Wall time | mean(d) | 2*SE | Decision | Collapse | Worst-seed drops > 10 |", "|---|---|---|---|---|---|---|---|---|---|"]
for r in st["rungs"]:
    mf = P / "runs" / r["name"] / "manifest.json"; m = json.loads(mf.read_text()) if mf.is_file() else {}
    tj = P / "logs" / f"{r['name']}-table.json"; dec = json.loads(tj.read_text())["decision"] if tj.is_file() else None
    s, e = m.get("start"), m.get("end")
    wall = str(dt.datetime.fromisoformat(e) - dt.datetime.fromisoformat(s)).split(".")[0] if s and e else "-"
    if dec:
        L.append(f"| {r['name']} | {r['vs']} | {s[:16]} | {(e or '-')[:16]} | {wall} | {dec['mean_d']:+.2f} | {2*dec['se']:.2f} | "
                 f"{'KEEP' if dec['keep'] else 'DROP'} | {dec['collapse_count']['new']} of 6 | {dec['worst_seed_drops_over_10'] or 'none'} |")
    else:
        L.append(f"| {r['name']} | {r['vs']} | {(s or '-')[:16]} | {(e or '-')[:16]} | {wall} | - | - | no result | - | - |")
L += ["", f"Retained base at the end: **{st.get('retained', '-')}**", "",
      f"Minimum MemAvailable during the chain (logs/ram.log, every 10 min): **{low if low is not None else '-'} MB**", "",
      "Flags: " + ("; ".join(st["flags"]) if st["flags"] else "none"), "",
      "F2, confirmation and the final test were NOT started (owner decision required).", ""]
for r in st["rungs"]:
    f = P / "reports" / f"{r['name']}-table.md"
    if f.is_file():
        L += [f"## {r['name']} table (verbatim from reports/{r['name']}-table.md)", "", f.read_text().replace("\n# ", "\n### ").lstrip("# "), ""]
out.write_text("\n".join(L) + "\n"); print(f"summary -> {out}")
EOF
}
state(){ python3 - "$STATE" "$@" <<'EOF'
import json, sys
p, op = sys.argv[1], sys.argv[2]; d = json.load(open(p))
if op == "rung": d["rungs"].append({"name": sys.argv[3], "vs": sys.argv[4]})
elif op == "flag": d["flags"].append(sys.argv[3])
elif op == "retained": d["retained"] = sys.argv[3]
json.dump(d, open(p, "w"), indent=1)
EOF
}
backup(){  # copy ladder files into the ladder-work worktree, commit, mirror to D: and push ladder-work
  [[ -n $T ]] && { say "TEST: commit/mirror skipped ($1)"; return 0; }
  for r in "$RUNG1" F3-on-F5 F3-on-F6; do
    [[ -f $P/reports/$r-table.md ]] && cp "$P/reports/$r-table.md" "$WT/reports/"
    [[ -f $P/logs/inputs-$r.md ]] && cp "$P/logs/inputs-$r.md" "$WT/reports/$r-inputs.md"
  done
  [[ -f $SUMMARY ]] && cp "$SUMMARY" "$WT/reports/"
  git -C "$WT" add reports && { git -C "$WT" diff --cached --quiet || git -C "$WT" -c user.name=rackiavic -c user.email=rackiavic@users.noreply.github.com commit -q -m "ladder (chain.sh, by the pre-registered rule): $1" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"; }
  "$P/scripts/mirror_to_d.sh" >> "$P/logs/mirror.log" 2>&1 || { say "mirror/push failed"; state flag "mirror or push failed after: $1"; }
}
abort(){
  say "ABORT: $1"
  echo "$(date -Iseconds) CHAIN ABORTED: $1. Nothing further was started; the chain never resumes by itself." >> "$P/logs/ALERT.txt"
  state flag "ABORT: $1"; summary "ABORTED: $1"; backup "chain aborted: $1"; exit 1
}
guards(){  # abort conditions checked before and after every rung
  [[ -e $P/logs/RAM-ALERT.txt ]] && abort "RAM guard trip (logs/RAM-ALERT.txt)"
  [[ -e $P/logs/DRIFT-ALERT.txt ]] && abort "drift CHANGED-RELEVANT (logs/DRIFT-ALERT.txt)"
  [[ -f $P/logs/ALERT.txt ]] && grep -q "CHANGED-RELEVANT" "$P/logs/ALERT.txt" && abort "drift CHANGED-RELEVANT (logs/ALERT.txt)"
  [[ -n $T ]] || "$P/scripts/drift_check.sh" --log >/dev/null || abort "drift CHANGED-RELEVANT before $1"
}
run_rung(){  # $1 NAME, $2 judged vs, $3 tmux session
  local R=$1 K=$2 S=$3
  guards "$R"; state rung "$R" "$K"
  if [[ -z $T ]]; then
    [[ -f $APP/$R.json ]] || abort "$R: no approved config $APP/$R.json"
    [[ ! -e $P/runs/$R ]] || abort "$R: runs/$R already exists (never overwrite, never resume)"
    rm -f "$P/logs/launch-$R.rc"
    say "launch $R in tmux session $S"
    tmux new -d -s "$S" "$P/scripts/launch.sh $APP/$R.json; echo \$? > $P/logs/launch-$R.rc"
    until [[ -s $P/logs/launch-$R.rc ]]; do
      sleep 60; tmux has-session -t "$S" 2>/dev/null || [[ -s $P/logs/launch-$R.rc ]] || { sleep 5; [[ -s $P/logs/launch-$R.rc ]] || abort "$R: tmux session $S vanished without an exit code"; }
    done
    rc=$(cat "$P/logs/launch-$R.rc"); say "$R launch.sh rc=$rc"
    [[ $rc == 0 ]] || abort "$R: launch.sh exit $rc (launch refused or failed; see logs/train-$R.log)"
    python3 -c "import json,sys;d=json.load(open('$P/runs/$R/manifest.json'));sys.exit(0 if d.get('end') and d.get('exit_code')==0 else 1)" \
      || abort "$R: run failed (runs/$R/manifest.json exit_code != 0; RAM guard stop or crash)"
    "$P/scripts/post_rung.sh" "$R" "$K" || abort "$R: post_rung.sh failed (see logs/post_$R.log and ALERT.txt)"
  fi
  [[ -f $P/logs/$R-table.json ]] || abort "$R: no table"
  guards "$R (after)"
}
decide(){ python3 -c "import json;d=json.load(open('$P/logs/$1-table.json'))['decision'];print('KEEP' if d['keep'] else 'DROP', d['collapse_count']['new'], len(d['worst_seed_drops_over_10']))"; }

# ---- start ----
[[ -z $T && -e $P/logs/CHAIN-STARTED ]] && { say "refusing: logs/CHAIN-STARTED exists (never auto-resume)"; exit 3; }
[[ -z $T && -e $P/logs/ALERT.txt ]] && { say "refusing: logs/ALERT.txt exists (owner must clear it)"; exit 3; }
[[ -n $T ]] || date -Iseconds > "$P/logs/CHAIN-STARTED"
echo "{\"started\": \"$(date -Iseconds)\", \"rungs\": [], \"flags\": [], \"retained\": \"$BASE0\"}" > "$STATE"
say "chain start: $RUNG1 vs $BASE0, then F3 on the retained base, then STOP${T:+ (TEST)}"

run_rung "$RUNG1" "$BASE0" f6
read -r V1 C1 W1 <<< "$(decide "$RUNG1")"; say "$RUNG1: $V1, collapse $C1 of 6, worst-seed drops $W1"
(( W1 > 0 )) && state flag "$RUNG1: worst-seed drop > 10 points (reported, not deciding)"
(( C1 > 3 )) && abort "$RUNG1: collapse count $C1 of 6 (> 3)"
if [[ $V1 == KEEP ]]; then BASE=$RUNG1; else BASE=$BASE0; fi
state retained "$BASE"; say "retained base: $BASE"
backup "$RUNG1 $V1 vs $BASE0 (mean d by rung_table); retained base $BASE"

F3=F3-on-$BASE
if [[ -n $T ]]; then
  say "TEST: would launch $F3 (approved config $APP/$F3.json exists: $([[ -f $APP/$F3.json || -f $P/configs/ladder/drafts/$F3.json ]] && echo yes || echo no))"
  summary "TEST (no rung launched)"; say "TEST done"; exit 0
fi
run_rung "$F3" "$BASE" f3
read -r V2 C2 W2 <<< "$(decide "$F3")"; say "$F3: $V2, collapse $C2 of 6, worst-seed drops $W2"
(( W2 > 0 )) && state flag "$F3: worst-seed drop > 10 points (reported, not deciding)"
(( C2 > 3 )) && state flag "$F3: collapse count $C2 of 6"
[[ $V2 == KEEP ]] && { BASE=$F3; state retained "$BASE"; }
summary "COMPLETE: $RUNG1 $V1; $F3 $V2; retained base $BASE. STOPPED (F2, confirmation and final test need the owner)."
backup "$F3 $V2 vs ${F3#F3-on-}; chain complete, retained base $BASE; STOP"
say "chain complete; retained base $BASE; nothing further started"
