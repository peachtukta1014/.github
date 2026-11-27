#!/bin/sh
# lane-boost.sh <lane> - the ONE lane boost. There used to be eight copies
# (jii-boost.sh, code-boost.sh, ...) that differed only in the lane name: copy drift (RULE 1).
# The lane is already bound to the session (bin/lane-id), so this takes it as an argument and
# prints the same boot the eight files cat'd.
set -e
LANE="${1:?usage: lane-boost.sh <lane>}"
exec "$(dirname "$0")/../../../bin/om-boot" "$LANE"
