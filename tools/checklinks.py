import os, re, sys, urllib.parse
from html.parser import HTMLParser
SITE = sys.argv[1] if len(sys.argv) > 1 else "site"
class H(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]; s.ids=set()
    def handle_starttag(s, t, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        for k in ("href", "src"):
            if k in a and a[k]: s.links.append(a[k])
files = {}
for d, _, fs in os.walk(SITE):
    for f in fs:
        if f.endswith(".html"):
            p = os.path.join(d, f); h = H(); h.feed(open(p).read()); files[os.path.normpath(p)] = h
bad, n, ext = [], 0, set()
for p, h in files.items():
    if p.endswith("404.html"): continue
    for l in h.links:
        if l.startswith(("http://", "https://")): ext.add(l); continue
        if l.startswith(("mailto:", "data:")): continue
        n += 1
        u = urllib.parse.urlparse(l); path = urllib.parse.unquote(u.path)
        tgt = os.path.normpath(os.path.join(os.path.dirname(p), path)) if path else p
        if os.path.isdir(tgt): tgt = os.path.join(tgt, "index.html")
        if not os.path.exists(tgt): bad.append(f"{p}: {l} (missing)"); continue
        if u.fragment and tgt in files and u.fragment not in files[tgt].ids: bad.append(f"{p}: {l} (no #{u.fragment})")
print(f"pages={len(files)} internal_links={n} external={len(ext)} broken={len(bad)}")
print("\n".join(bad[:50]))
open("/tmp/ext_links.txt","w").write("\n".join(sorted(ext)))
sys.exit(1 if bad else 0)
