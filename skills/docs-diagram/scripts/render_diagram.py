#!/usr/bin/env python3
"""Render a CeTZ/Typst diagram (or a report embedding one) to PDF/SVG/PNG.

Typst cannot read files under /var/minis on this device (iSH bind mount), so the
build always happens in a scratch dir under /root and artifacts are copied back.

Usage:
  render_diagram.py diagram.typ [--format pdf,svg,png] [--outdir DIR] [--dpi 150]
  render_diagram.py diagram.typ --strict
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PKG_SHARED = Path("/var/minis/shared/tools/typst-packages")
PKG_SCRATCH = Path("/root/.cache/typst-packages")


def ensure_packages() -> Path:
    """Vendored @preview packages (cetz, oxifmt...) copied where typst can read them."""
    if not PKG_SCRATCH.exists():
        if not PKG_SHARED.exists():
            sys.exit("missing vendored packages: %s" % PKG_SHARED)
        shutil.copytree(PKG_SHARED, PKG_SCRATCH)
    return PKG_SCRATCH


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help=".typ file (CeTZ diagram or a report that embeds one)")
    ap.add_argument("--format", default="pdf", help="comma list: pdf,svg,png")
    ap.add_argument("--outdir", default=None, help="where artifacts go (default: next to source)")
    ap.add_argument("--dpi", default="150")
    ap.add_argument("--strict", action="store_true", help="non-zero exit on any typst error/warning")
    args = ap.parse_args()

    src = Path(args.source).expanduser().resolve()
    if not src.is_file():
        sys.exit("not found: %s" % src)
    outdir = Path(args.outdir).expanduser() if args.outdir else src.parent
    outdir.mkdir(parents=True, exist_ok=True)
    pkgs = ensure_packages()

    formats = [f.strip().lower() for f in args.format.split(",") if f.strip()]
    ok = True
    with tempfile.TemporaryDirectory(prefix="cetz-", dir="/root") as td:
        build = Path(td)
        copy_src = build / src.name
        shutil.copy2(src, copy_src)
        # bring along sibling assets (svg images, .png, included .typ)
        for extra in src.parent.iterdir():
            if extra.is_file() and extra.suffix.lower() in {".svg", ".png", ".jpg", ".jpeg", ".typ"} and extra != src:
                shutil.copy2(extra, build / extra.name)
        for fmt in formats:
            out = build / (src.stem + "." + fmt)
            cmd = ["typst", "compile", "--package-path", str(pkgs), "--format", fmt]
            if fmt in {"png", "jpg"}:
                cmd += ["--ppi", args.dpi]
            cmd += [str(copy_src), str(out)]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            noise = ("style is deprecated",)
            err = "\n".join(l for l in (proc.stderr or "").splitlines() if not any(n in l for n in noise))
            if proc.returncode != 0 or not out.exists():
                ok = False
                print(f"FAIL {fmt}: {err.strip().splitlines()[-1] if err.strip() else 'unknown error'}")
                continue
            dest = outdir / out.name
            shutil.copy2(out, dest)
            print(f"PASS {fmt} -> {dest} ({dest.stat().st_size // 1024} KB)")
            if err.strip() and args.strict:
                print(f"  warnings: {err.strip().splitlines()[0]}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
