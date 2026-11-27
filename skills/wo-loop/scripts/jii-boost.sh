#!/bin/sh
# Canonical lane boost pointer for jii.
# Resolve transport through registry/transports.json; this script does not own VM state.
set -eu
HQ_ROOT=${HQ_ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
cat "$HQ_ROOT/skills/wo-loop/jii/SKILL.md"
