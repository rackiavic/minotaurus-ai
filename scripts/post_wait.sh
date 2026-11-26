#!/usr/bin/env bash
# Wait until all three pilot manifests have an end time, then run post_pilot.sh once.
P=${MINOTAUR_ROOT:-$HOME/Minotaur}; export MINOTAUR_ROOT=$P  # working root (ext4); D:\Minotaur is the mirror
until python3 -c "
import json,sys
d=[json.load(open('$P/runs/'+r+'/manifest.json')).get('end') for r in ('pilot-dqn-brain','pilot-r3','pilot-r3-shaping')]
sys.exit(0 if all(d) else 1)"; do sleep 60; done
[[ -e $P/logs/post_pilot.started ]] && exit 0
date -Iseconds > $P/logs/post_pilot.started
exec $P/scripts/post_pilot.sh
