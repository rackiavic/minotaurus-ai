#!/usr/bin/env bash
# Mirror the working root (~/Minotaur, ext4) to D:\Minotaur, then push ladder-work to the fork.
# Run after every run or batch:  ~/Minotaur/scripts/mirror_to_d.sh
# - Never deletes anything on D: (no --delete; deletions need the owner's approval).
# - Never touches D:\Minotaur\secrets\ (excluded both ways; secrets/ is never in ~/Minotaur).
# - Leaves out .venv/ and __pycache__/, plus git worktree metadata (repo/.git/worktrees/ and
#   worktrees/*/.git), so D:'s own worktrees keep pointing at D:'s repo.
set -euo pipefail
P=${MINOTAUR_ROOT:-$HOME/Minotaur}; export MINOTAUR_ROOT=$P
D=/mnt/d/Minotaur
[[ -d $D ]] || { echo "D: mirror $D not mounted"; exit 2; }
[[ ! -e $P/secrets ]] || { echo "refusing: $P/secrets exists (secrets live on D: only)"; exit 3; }
LOG=$P/logs/mirror.log
t0=$(date +%s)
rsync -a --itemize-changes \
  --exclude='/secrets/' --exclude='.venv/' --exclude='__pycache__/' \
  --exclude='/repo/.git/worktrees/' --exclude='/worktrees/*/.git' \
  "$P/" "$D/" > "$P/logs/mirror-last.txt"
# D:'s worktrees keep their own index (in D:'s repo/.git/worktrees/, not mirrored). The files and
# refs are now new, so refresh only the index to HEAD (mixed reset: it never changes working files).
# Then both D: worktrees must be clean, or the mirror reports a failure.
for w in fresh work; do
  git -C "$D/worktrees/$w" reset -q
  [[ -z $(git -C "$D/worktrees/$w" status --porcelain --untracked-files=no) ]] || { echo "D: worktree $w not clean after mirror"; exit 4; }
done
n=$(grep -c '^[<>c]' "$P/logs/mirror-last.txt" || true)
git -C "$P/worktrees/work" push -q origin ladder-work
echo "$(date -Iseconds) mirrored $n changed items to $D in $(( $(date +%s)-t0 )) s; pushed ladder-work $(git -C "$P/worktrees/work" rev-parse --short HEAD)" | tee -a "$LOG"
