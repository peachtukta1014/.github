#!/usr/bin/env python3
"""Exa web search / fetch, runnable ON THE VM (no browser, no Minis app).

Ported from the device-side skill `exa-search` (OpenMinis/MinisSkills) so every
lane can research from the VM itself (RULE 16, Peach 2026-11-24).

Keyless by default (Exa MCP basic tier). If EXA_API_KEY is present in the
environment (the VM keeps the value in its vault; see system/SECRETS.md) it is sent
for higher
limits. The key is never printed.

Usage:
  search.py search "natural language description of the ideal page" [--num 5] [--json]
  search.py fetch <url> [<url> ...]
  search.py tools
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

URL = os.environ.get("EXA_MCP_URL", "https://mcp.exa.ai/mcp")
KEY = os.environ.get("EXA_API_KEY")
TIMEOUT = int(os.environ.get("EXA_TIMEOUT", "60"))


def post(payload, sid=None):
    h = {"Content-Type": "application/json",
         "Accept": "application/json, text/event-stream",
         "User-Agent": "Minis/1.0"}
    if KEY:
        h["x-api-key"] = KEY
    if sid:
        h["mcp-session-id"] = sid
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers=h)
    try:
        r = urllib.request.urlopen(req, timeout=TIMEOUT)
    except urllib.error.HTTPError as e:
        sys.exit("exa: HTTP %s %s" % (e.code, e.read().decode(errors="replace")[:200]))
    except Exception as e:
        sys.exit("exa: network failed: %s" % e)
    raw = r.read().decode(errors="replace")
    data = [l[6:] for l in raw.splitlines() if l.startswith("data: ")]
    return r.headers.get("mcp-session-id"), ("\n".join(data) if data else raw)


def rpc(method, params, sid=None, rid=1):
    p = {"jsonrpc": "2.0", "id": rid, "method": method}
    if params is not None:
        p["params"] = params
    return post(p, sid)


def session():
    sid, _ = rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                "clientInfo": {"name": "vm-hq-core", "version": "1.0"}})
    post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    return sid


def text_of(body):
    try:
        d = json.loads(body)
    except json.JSONDecodeError:
        return body
    if "error" in d:
        return "exa error: %s" % json.dumps(d["error"])[:300]
    try:
        return "\n".join(c.get("text", "") for c in d["result"]["content"])
    except Exception:
        return json.dumps(d)[:2000]


def main():
    ap = argparse.ArgumentParser(prog="research-search", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="web search")
    s.add_argument("query")
    s.add_argument("--num", type=int, default=5)
    s.add_argument("--json", action="store_true", help="raw MCP payload")
    f = sub.add_parser("fetch", help="fetch URLs as clean markdown")
    f.add_argument("urls", nargs="+")
    f.add_argument("--json", action="store_true")
    sub.add_parser("tools", help="list the tools this endpoint exposes")
    a = ap.parse_args()

    sid = session()
    if a.cmd == "tools":
        _, b = rpc("tools/list", {}, sid)
        names = [t["name"] for t in json.loads(b)["result"]["tools"]]
        print("endpoint: %s\ntools: %s\nkey: %s" % (URL, ", ".join(names),
              "yes" if KEY else "no (keyless basic tier)"))
        return 0
    if a.cmd == "search":
        _, b = rpc("tools/call", {"name": "web_search_exa",
                                  "arguments": {"query": a.query, "numResults": a.num}}, sid)
    else:
        _, b = rpc("tools/call", {"name": "web_fetch_exa", "arguments": {"urls": a.urls}}, sid)
    print(b if a.json else text_of(b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
