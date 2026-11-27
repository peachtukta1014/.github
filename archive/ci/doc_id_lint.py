#!/usr/bin/env python3
"""doc_id_lint — every registered doc id must resolve to a real file, and never to a MOVED stub.

Demoted from the retired `reflex` skill (2026-11-21): it is the only checker that caught the six
stub doc ids on 2026-11-21 while every other gate stayed green. Runs ON the VM, no device needed.

Usage (on the VM, from the vault root /srv/repos/hq/vm-hq-core):
    python3 /srv/repos/skills-shared/bin/doc_id_lint.py            # every registered id
    python3 /srv/repos/skills-shared/bin/doc_id_lint.py rule.shared scope.files
Exit code 0 = clean, 1 = at least one BROKEN or MOVED id.
"""
import json
import os
import subprocess
import sys

ROOT = os.environ.get("HQ_ROOT", "/srv/repos/hq/vm-hq-core")
STUB_MAX = 900  # a file this small whose head says MOVED is a stub, not the real home


def resolve(doc_id):
    p = subprocess.run(["bin/doc.py", "path", doc_id], cwd=ROOT,
                       capture_output=True, text=True)
    return p.stdout.strip()


def main(argv):
    reg = json.load(open(os.path.join(ROOT, "registry/docids.json"), encoding="utf-8"))
    ids = reg.get("ids", reg)
    want = argv or sorted(ids)
    bad = 0
    for i in want:
        path = resolve(i)
        if not path or not os.path.isfile(path):
            print("%-24s BROKEN  (no such file)" % i)
            bad += 1
            continue
        size = os.path.getsize(path)
        head = open(path, encoding="utf-8", errors="replace").read(600)
        if size < STUB_MAX and "MOVED" in head.upper():
            print("%-24s MOVED   %s  (%dB stub)" % (i, path, size))
            bad += 1
        else:
            print("%-24s ok      %s" % (i, path))
    print("---")
    print("bad=%d / total=%d" % (bad, len(want)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main([a for a in sys.argv[1:] if not a.startswith("-")]))
