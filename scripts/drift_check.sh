#!/usr/bin/env bash
# Drift guard: compare upstream/main with the pinned SHA and classify the change.
# Output (first line): SAME | CHANGED-IRRELEVANT | CHANGED-RELEVANT
# Usage: drift_check.sh [--log]     (--log also appends a timestamped line to logs/drift.log)
# Never pulls, never touches worktrees/fresh. Only `git fetch upstream` in repo/.
set -euo pipefail
P=/mnt/d/Minotaur
REPO=$P/repo
PINNED=$(python3 -c "import json;print(json.load(open('$P/protocol/pinned.json'))['pinned_sha'])")
PIN_TMD=$(python3 -c "import json;print(json.load(open('$P/protocol/pinned.json'))['training_md_sha256'])")

# WATCH LIST: anything that can change training, observation, reward, evaluation, scoring,
# maze generation/pools, brain loading/checking, dependencies or the documented rules.
WATCH=(
  TRAINING.md
  minotaurus/trainer/
  minotaurus/engine/
  minotaurus/brain/
  minotaurus/cli/train.py
  minotaurus/cli/check_brain.py
  minotaurus/verify.py
  data/examples/
  data/levels/
  data/schemas/
  pyproject.toml
  uv.lock
)

git -C "$REPO" fetch -q upstream
UP=$(git -C "$REPO" rev-parse upstream/main)
NOW=$(date -Iseconds)

if [[ "$UP" == "$PINNED" ]]; then
  STATUS=SAME
  DETAIL="upstream/main == pinned ${PINNED:0:7}"
else
  ALL=$(git -C "$REPO" diff --name-only "$PINNED" "$UP")
  REL=$(git -C "$REPO" diff --name-only "$PINNED" "$UP" -- "${WATCH[@]}" || true)
  if [[ -z "$REL" ]]; then
    STATUS=CHANGED-IRRELEVANT
    DETAIL="upstream ${UP:0:7} vs pinned ${PINNED:0:7}; $(echo "$ALL" | wc -l) files changed, none on the watch list"
  else
    STATUS=CHANGED-RELEVANT
    NEW_TMD=$(git -C "$REPO" show "$UP:TRAINING.md" | sha256sum | cut -d' ' -f1)
    TMD_NOTE="TRAINING.md unchanged"
    [[ "$NEW_TMD" != "$PIN_TMD" ]] && TMD_NOTE="TRAINING.md CHANGED (rules may differ: re-run Step 3 audit)"
    DETAIL="upstream ${UP:0:7} vs pinned ${PINNED:0:7}; $TMD_NOTE"
  fi
fi

echo "$STATUS"
echo "$DETAIL"
if [[ "$STATUS" == CHANGED-RELEVANT ]]; then
  echo "relevant files:"
  echo "$REL" | sed 's/^/  /'
  echo "summary (newest commits touching watched files; why it may matter: these paths feed training/eval):"
  git -C "$REPO" log --format='  %h %s' "$PINNED..$UP" -- "${WATCH[@]}" | head -3
fi
if [[ "${1:-}" == "--log" ]]; then
  echo "$NOW $STATUS ${UP:0:7} ${DETAIL}" >> "$P/logs/drift.log"
fi
[[ "$STATUS" == CHANGED-RELEVANT ]] && exit 2 || exit 0
