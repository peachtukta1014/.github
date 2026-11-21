#!/bin/sh
# scripts/webhook-boost.sh
# Canonical invocation (run on the VM): vm "cat /srv/repos/hq/vm-hq-core/skills/wo-loop/webhook/SKILL.md
# vm = om-ssh (auto route, IAP pinned).
# This shell file is a static pointer to the complete skill body; no identity data is duplicated.
cat /srv/repos/hq/vm-hq-core/skills/wo-loop/webhook/SKILL.md
