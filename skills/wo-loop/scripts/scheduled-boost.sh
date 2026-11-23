#!/bin/sh
# Canonical lane boost pointer for scheduled.
# Resolve transport through registry/transports.json; this script does not own VM state.
set -eu
HQ_ROOT=${HQ_ROOT:-/srv/repos/hq/vm-hq-core}
cat "$HQ_ROOT/skills/wo-loop/scheduled/SKILL.md"
