import sys, os, json, re, html, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "content"), os.path.join(ROOT, "tools")]
from parts import PARTS, GROUPS
from toollist import TOOLS, TCATS, WHERE
from guides import GUIDES, GCATS
from biketypes import TYPES
from history import HISTORY, ERAS
from makers import MAKERS, MAKERS_INTRO, MCATS
from buildguide import BUILD_INTRO, BUILD_STEPS, BUILD_WARN
from glossary import TERMS
from svgs import DIAGRAMS
SITE = os.path.join(ROOT, "site")
CRED = json.load(open(os.path.join(ROOT, "content/credits.json")))
LEVEL = {1: ("Легко", "easy"), 2: ("Средне", "mid"), 3: ("Сложно", "hard")}
P = {p["id"]: p for p in PARTS}; T = {t["id"]: t for t in TOOLS}; G = {g["id"]: g for g in GUIDES}; TY = {t["id"]: t for t in TYPES}
PAGES = {"history": "history/", "anatomy": "anatomy/", "types": "types/", "tools": "tools/", "guides": "guides/", "makers": "makers/", "build": "build/", "glossary": "glossary/", "credits": "credits/", "parts": "anatomy/#parts"}
errors = []
def path_of(kind, ident):
    base, _, frag = ident.partition("#")
    frag = ("#" + frag) if frag else ""
    if kind == "part": ok, p = base in P, f"parts/{base}/"
    elif kind == "tool": ok, p = base in T, f"tools/{base}/"
    elif kind == "guide": ok, p = base in G, f"guides/{base}/"
    elif kind == "type": ok, p = base in TY, f"types/{base}/"
    elif kind == "page": ok, p = base in PAGES, PAGES.get(base, "")
    else: ok, p = False, ""
    if not ok: errors.append(f"bad ref {kind}:{ident}")
    return p + frag
def name_of(kind, ident):
    return {"part": lambda i: P[i]["ru"], "tool": lambda i: T[i]["ru"], "guide": lambda i: G[i]["title"], "type": lambda i: TY[i]["ru"]}.get(kind, lambda i: i)(ident)
def md(text, R):
    def rep(m):
        kind, ident, label = m.group(1), m.group(2), m.group(3)
        return f'<a href="{R}{path_of(kind, ident)}">{html.escape(label or name_of(kind, ident))}</a>'
    out = []
    for para in text.strip().split("\n"):
        para = para.strip()
        if not para: continue
        e = html.escape(para, quote=False)
        e = re.sub(r"\[\[(\w+):([\w#-]+)(?:\|([^\]]+))?\]\]", rep, e)
        out.append(e)
    return out
def P_html(text, R):
    res, items = [], []
    for line in md(text, R):
        if line.startswith("•"): items.append(f"<li>{line[1:].strip()}</li>")
        else:
            if items: res.append("<ul>" + "".join(items) + "</ul>"); items = []
            res.append(f"<p>{line}</p>")
    if items: res.append("<ul>" + "".join(items) + "</ul>")
    return "".join(res)
def inline(text, R): return " ".join(md(text, R))
def fig(key, R, cls=""):
    if not key: return ""
    if isinstance(key, list): return "".join(fig(k, R, cls) for k in key)
    c = CRED[key]
    alt = html.escape(c.get("desc") or key)[:140]
    return (f'<figure class="photo {cls}"><img src="{R}img/photos/{key}.webp" width="{c["w"]}" height="{c["h"]}" loading="lazy" alt="{alt}">'
            f'<figcaption>Фото: {html.escape(c["author"][:80])}, {html.escape(c["license"])} · <a href="{R}credits/#{key}">источник</a></figcaption></figure>')
def badge(level): l, c = LEVEL[level]; return f'<span class="badge {c}">{l}</span>'
def chips(kind, ids, R):
    if not ids: return ""
    return '<ul class="chips">' + "".join(f'<li><a href="{R}{path_of(kind, i)}">{html.escape(name_of(kind, i))}</a></li>' for i in ids) + "</ul>"
def related(blocks):
    inner = "".join(f'<div class="rel"><h3>{t}</h3>{c}</div>' for t, c in blocks if c)
    return f'<section class="related"><h2>Связано</h2><div class="relgrid">{inner}</div></section>' if inner else ""
NAV = [("history/", "История"), ("anatomy/", "Устройство"), ("types/", "Типы"), ("guides/", "Инструкции"), ("tools/", "Инструмент"), ("makers/", "Производители"), ("build/", "Собрать самому"), ("glossary/", "Словарь")]
def page(rel, title, body, crumbs=(), desc=""):
    depth = rel.count("/") if rel.endswith("/") else rel.count("/")
    R = "../" * depth
    nav = "".join(f'<a href="{R}{h}">{n}</a>' for h, n in NAV)
    bc = ""
    if crumbs:
        bc = '<nav class="crumbs" aria-label="Навигация"><a href="' + R + '">Главная</a>' + "".join(
            (f' <span>›</span> <a href="{R}{h}">{html.escape(n)}</a>' if h else f' <span>›</span> <b>{html.escape(n)}</b>') for n, h in crumbs) + "</nav>"
    doc = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — Вело-вселенная</title><meta name="description" content="{html.escape(desc or title)}">
<link rel="icon" href="{R}img/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{R}css/style.css?v=1">
<script>document.documentElement.dataset.theme=localStorage.getItem('vu-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')</script>
</head><body data-root="{R}">
<header class="top"><div class="wrap topin"><a class="logo" href="{R}"><img src="{R}img/favicon.svg" alt="" width="28" height="28"><span>Вело<b>вселенная</b></span></a>
<div class="search"><input id="q" type="search" placeholder="Поиск: камера, Nexus, каретка, Lefty…" autocomplete="off" aria-label="Поиск по сайту"><div id="sr" class="sr" hidden></div></div>
<button id="theme" class="iconbtn" aria-label="Сменить тему">◐</button><button id="menu" class="iconbtn" aria-label="Меню">☰</button></div>
<nav class="mainnav wrap" id="nav">{nav}</nav></header>
<main class="wrap">{bc}{body}</main>
<footer class="foot"><div class="wrap"><p><b>Вело-вселенная</b> — открытый справочник и виртуальная веломастерская: история, устройство, инструмент и инструкции.</p>
<p class="partners"><a href="https://avtomaster24bot-lab.github.io/velopark-panasonic/">Velopark.kz</a> — японские велосипеды, электровелосипеды Panasonic и запчасти · <a href="https://avtomaster24bot-lab.github.io/velomarket/">VeloMarket</a> — объявления о продаже велосипедов и запчастей</p>
<p class="small">Инструкции носят справочный характер. Моменты затяжки и порядок работ для конкретной модели всегда сверяйте с мануалом производителя. Фото — Wikimedia Commons, см. <a href="{R}credits/">источники и лицензии</a>; схемы нарисованы для сайта.</p></div></footer>
<script src="{R}js/app.js?v=1" defer></script></body></html>"""
    out = os.path.join(SITE, rel if rel.endswith(".html") else rel + "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(doc)
    return R
def Rof(rel): return "../" * rel.count("/")
SEARCH = []
def idx(title, url, kind, text="", en=""):
    SEARCH.append({"t": title, "u": url, "k": kind, "e": en, "s": re.sub(r"\[\[\w+:[\w#-]+\|?([^\]]*)\]\]", r"\1", text)[:400]})

# ---------------- Parts
users_of_part = {}
for g in GUIDES:
    for p in g["parts"]: users_of_part.setdefault(p, []).append(g["id"])
types_of_part = {}
for t in TYPES:
    for p in t["parts"]: types_of_part.setdefault(p, []).append(t["id"])
parts_of_tool, guides_of_tool = {}, {}
for p in PARTS:
    for t in p["tools"]: parts_of_tool.setdefault(t, []).append(p["id"])
for g in GUIDES:
    for t in g["tools"]: guides_of_tool.setdefault(t, []).append(g["id"])
gname = dict(GROUPS)
for p in PARTS:
    rel = f"parts/{p['id']}/"; R = Rof(rel)
    dg = ""
    if p.get("diagram"):
        dn, fn = DIAGRAMS[p["diagram"]]
        dg = f'<figure class="diag"><div class="svgbox">{fn(R)}</div><figcaption>Схема: {dn} · <a href="{R}anatomy/#{p["diagram"]}">все схемы</a></figcaption></figure>'
    specs = ("<div class='specs'><h2>Факты и стандарты</h2><ul>" + "".join(f"<li>{inline(s, R)}</li>" for s in p.get("specs", [])) + "</ul></div>") if p.get("specs") else ""
    gl = sorted(set(p["guides"]) | set(users_of_part.get(p["id"], [])), key=lambda x: (G[x]["level"], G[x]["title"]))
    guides_html = '<ul class="glist">' + "".join(f'<li><a href="{R}guides/{x}/">{html.escape(G[x]["title"])}</a> {badge(G[x]["level"])}</li>' for x in gl) + "</ul>" if gl else ""
    others = [q["id"] for q in PARTS if q["group"] == p["group"] and q["id"] != p["id"]]
    body = f"""<article class="item"><div class="kicker">{gname[p['group']]}</div><h1>{html.escape(p['ru'])}</h1><p class="en">{html.escape(p['en'])}</p>
<p class="lead">{inline(p['short'], R)}</p><div class="cols"><div>{P_html(p['text'], R)}{specs}</div><div>{fig(p.get('img'), R)}{dg}</div></div></article>"""
    body += related([("Инструкции", guides_html), ("Инструмент", chips("tool", p["tools"], R)), ("Где встречается", chips("type", types_of_part.get(p["id"], []), R)), ("Соседние детали", chips("part", others, R))])
    page(rel, p["ru"], body, [("Устройство", "anatomy/"), (p["ru"], None)], p["short"])
    idx(p["ru"], rel, "Деталь", p["short"] + " " + p["text"], p["en"])
# ---------------- Tools
tc = dict(TCATS)
for t in TOOLS:
    rel = f"tools/{t['id']}/"; R = Rof(rel)
    tips = ("<h2>Советы</h2><ul>" + "".join(f"<li>{inline(x, R)}</li>" for x in t.get("tips", [])) + "</ul>") if t.get("tips") else ""
    gl = sorted(guides_of_tool.get(t["id"], []), key=lambda x: G[x]["level"])
    guides_html = '<ul class="glist">' + "".join(f'<li><a href="{R}guides/{x}/">{html.escape(G[x]["title"])}</a> {badge(G[x]["level"])}</li>' for x in gl) + "</ul>" if gl else ""
    body = f"""<article class="item"><div class="kicker">Инструмент · {tc[t['cat']]}</div><h1>{html.escape(t['ru'])}</h1><p class="en">{html.escape(t['en'])}</p>
<div class="cols"><div>{P_html(t['text'], R)}{tips}<h2>Где взять</h2><p>{html.escape(WHERE)}</p></div><div>{fig(t.get('img'), R)}</div></div></article>"""
    body += related([("Нужен в инструкциях", guides_html), ("Для деталей", chips("part", parts_of_tool.get(t["id"], []), R))])
    page(rel, t["ru"], body, [("Инструмент", "tools/"), (t["ru"], None)], t["text"][:150])
    idx(t["ru"], rel, "Инструмент", t["text"], t["en"])
# ---------------- Guides
gcn = dict(GCATS)
for g in GUIDES:
    rel = f"guides/{g['id']}/"; R = Rof(rel)
    steps = "".join(f'<li><span class="sn">{i}</span><div>{inline(s, R)}</div></li>' for i, s in enumerate(g["steps"], 1))
    warn = ('<div class="warn"><b>⚠ Важно</b><ul>' + "".join(f"<li>{inline(w, R)}</li>" for w in g["warn"]) + "</ul></div>") if g["warn"] else ""
    tools_box = '<div class="toolbox"><h2>Понадобится</h2><ul>' + "".join(f'<li><a href="{R}tools/{t}/">{html.escape(T[t]["ru"])}</a></li>' for t in g["tools"]) + "</ul></div>" if g["tools"] else ""
    tlist = [x for x in g["types"] if x != "all"]
    tchips = chips("type", tlist, R) if tlist else '<p class="muted">Подходит для любых велосипедов</p>'
    note = f'<p class="note">{inline(g["note"], R)}</p>' if g.get("note") else ""
    body = f"""<article class="item guide"><div class="kicker">Инструкция · {gcn[g['cat']]}</div><h1>{html.escape(g['title'])}</h1>
<div class="meta">{badge(g['level'])}<span>⏱ {html.escape(g['time'])}</span><span>{len(g['steps'])} шагов</span></div>
<p class="lead">{inline(g['intro'], R)}</p>{fig(g.get('img'), R, 'gimg')}{tools_box}{warn}<h2>Пошагово</h2><ol class="steps">{steps}</ol>{note}</article>"""
    body += related([("Детали", chips("part", g["parts"], R)), ("Инструмент", chips("tool", g["tools"], R)), ("Типы велосипедов", tchips)])
    page(rel, g["title"], body, [("Инструкции", "guides/"), (g["title"], None)], g["intro"][:150])
    idx(g["title"], rel, "Инструкция · " + LEVEL[g["level"]][0], g["intro"] + " " + " ".join(g["steps"]))
# ---------------- Types
for t in TYPES:
    rel = f"types/{t['id']}/"; R = Rof(rel)
    feats = "<ul class='feat'>" + "".join(f"<li>{inline(f, R)}</li>" for f in t["features"]) + "</ul>"
    gl = sorted(t["guides"], key=lambda x: G[x]["level"])
    guides_html = '<ul class="glist">' + "".join(f'<li><a href="{R}guides/{x}/">{html.escape(G[x]["title"])}</a> {badge(G[x]["level"])}</li>' for x in gl) + "</ul>"
    body = f"""<article class="item"><div class="kicker">Тип велосипеда</div><h1>{html.escape(t['ru'])}</h1><p class="en">{html.escape(t['en'])}</p>
<p class="lead">{inline(t['short'], R)}</p><div class="cols"><div>{P_html(t['text'], R)}<h2>Отличительные черты</h2>{feats}<h2>Уход</h2><p>{inline(t['care'], R)}</p></div><div>{fig(t.get('img'), R)}</div></div></article>"""
    body += related([("Инструкции для этого типа", guides_html), ("Ключевые детали", chips("part", t["parts"], R)), ("Другие типы", chips("type", [x["id"] for x in TYPES if x["id"] != t["id"]], R))])
    page(rel, t["ru"], body, [("Типы велосипедов", "types/"), (t["ru"], None)], t["short"])
    idx(t["ru"], rel, "Тип велосипеда", t["short"] + " " + t["text"], t["en"])
# ---------------- Index pages
def card(R, href, title, sub, img=None, extra=""):
    im = f'<img src="{R}img/photos/{img}.webp" alt="" loading="lazy">' if img else ""
    return f'<a class="card" href="{R}{href}">{im}<div><h3>{html.escape(title)}</h3><p>{sub}</p>{extra}</div></a>'
# anatomy
R = Rof("anatomy/")
groups = "".join(f'<h3 id="g-{gid}">{gn}</h3><div class="grid small">' + "".join(card(R, f"parts/{p['id']}/", p["ru"], html.escape(p["en"])) for p in PARTS if p["group"] == gid) + "</div>" for gid, gn in GROUPS)
diags = "".join(f'<section class="diagsec" id="{k}"><h2>{v[0]}</h2><div class="svgbox">{v[1](R)}</div></section>' for k, v in DIAGRAMS.items() if k != "anatomy")
body = f"""<h1>Устройство велосипеда</h1><p class="lead">Нажмите на любую подпись на схеме — откроется страница детали: как называется, зачем нужна, какие бывают стандарты, каким инструментом обслуживать и какие инструкции к ней относятся.</p>
<div class="svgbox big">{DIAGRAMS['anatomy'][1](R)}</div><p class="muted small">Схема условная: показан горный хардтейл с дисковыми тормозами.</p>
<section id="parts"><h2>Все детали по узлам ({len(PARTS)})</h2>{groups}</section>{diags}"""
page("anatomy/", "Устройство велосипеда", body, [("Устройство", None)], "Из чего состоит велосипед: интерактивная схема и все детали")
idx("Устройство велосипеда — схема", "anatomy/", "Раздел", "схема детали названия анатомия геометрия рама трансмиссия колесо втулка вилка планетарная")
for k, v in DIAGRAMS.items(): idx("Схема: " + v[0], f"anatomy/#{k}", "Схема", v[0])
# tools index
R = Rof("tools/")
body = '<h1>Инструмент</h1><p class="lead">Что нужно для обслуживания велосипеда, как это называется и где применяется. Начните с базового набора — его хватит на большинство инструкций уровня «Легко».</p>'
for cid, cn in TCATS:
    body += f'<h2>{cn}</h2><div class="grid">' + "".join(card(R, f"tools/{t['id']}/", t["ru"], html.escape(t["en"]), t.get("img")) for t in TOOLS if t["cat"] == cid) + "</div>"
page("tools/", "Инструмент", body, [("Инструмент", None)])
# guides index
R = Rof("guides/")
fl = '<div class="filters" id="gf"><button data-l="0" class="on">Все</button><button data-l="1">Легко</button><button data-l="2">Средне</button><button data-l="3">Сложно</button></div>'
body = f'<h1>Инструкции</h1><p class="lead">{len(GUIDES)} пошаговых инструкций — от замены камеры на колесе с планетарной втулкой до обслуживания вилки Cannondale Lefty. В каждой — список инструмента со ссылками и предупреждения.</p>{fl}'
for cid, cn in GCATS:
    gs = sorted([g for g in GUIDES if g["cat"] == cid], key=lambda g: (g["level"], g["title"]))
    body += f'<h2 class="gcat">{cn}</h2><div class="grid">' + "".join(f'<a class="card gcard" data-level="{g["level"]}" href="{R}guides/{g["id"]}/"><div><h3>{html.escape(g["title"])}</h3><p>{badge(g["level"])} ⏱ {html.escape(g["time"])}</p></div></a>' for g in gs) + "</div>"
page("guides/", "Инструкции", body, [("Инструкции", None)])
# types index
R = Rof("types/")
body = '<h1>Типы велосипедов</h1><p class="lead">Чем отличаются шоссейные, горные, городские и другие велосипеды, для чего каждый подходит и как за ним ухаживать.</p><div class="grid">' + "".join(card(R, f"types/{t['id']}/", t["ru"], inline(t["short"], R) if False else html.escape(re.sub(r'\[\[.*?\|(.*?)\]\]', r'\1', t["short"])), t.get("img")) for t in TYPES) + "</div>"
page("types/", "Типы велосипедов", body, [("Типы", None)])
# history
R = Rof("history/")
tl = ""
for eid, en in ERAS:
    tl += f'<h2 class="era">{en}</h2><ol class="timeline">'
    for h in [x for x in HISTORY if x["era"] == eid]:
        tl += f'<li><div class="yr">{html.escape(h["year"])}</div><div class="tbody"><h3>{html.escape(h["title"])}</h3><p>{inline(h["text"], R)}</p>{fig(h.get("img"), R, "tl")}</div></li>'
    tl += "</ol>"
body = f'<h1>История велосипеда</h1><p class="lead">От «беговой машины» Карла Драйса 1817 года до электровелосипедов и электронных переключателей — {len(HISTORY)} ключевых событий. Только проверенные факты; спорные версии помечены.</p>{fig("rover-ad", R, "float")}{tl}'
page("history/", "История велосипеда", body, [("История", None)], "История велосипеда: дрезина, костотряс, пенни-фартинг, безопасный велосипед и современность")
for h in HISTORY: idx(f'{h["year"]}: {h["title"]}', "history/", "История", h["text"])
# makers
R = Rof("makers/")
body = f'<h1>Где и кто производит велосипеды</h1>{P_html(MAKERS_INTRO, R)}'
for cid, cn in MCATS:
    body += f'<h2>{cn}</h2><div class="grid">' + "".join(f'<div class="card static"><div><h3>{html.escape(m["name"])}</h3><p class="muted">{html.escape(m["country"])}{(", " + html.escape(m["city"])) if m.get("city") else ""}{(" · с " + m["founded"] + " г.") if m.get("founded") else ""}</p><p>{html.escape(m["text"])}</p></div></div>' for m in MAKERS if m["cat"] == cid) + "</div>"
    for m in MAKERS:
        if m["cat"] == cid: idx(m["name"], "makers/", "Производитель", m["country"] + " " + m["text"])
page("makers/", "Производители", body, [("Производители", None)])
# build
R = Rof("build/")
steps = "".join(f'<li><span class="sn">{i}</span><div><h3>{html.escape(t)}</h3><p>{inline(x, R)}</p></div></li>' for i, (t, x) in enumerate(BUILD_STEPS, 1))
body = f'<h1>Как собрать велосипед самому</h1><p class="lead">{inline(BUILD_INTRO, R)}</p><ol class="steps big">{steps}</ol><div class="warn"><b>⚠ Важно</b><ul>' + "".join(f"<li>{inline(w, R)}</li>" for w in BUILD_WARN) + "</ul></div>"
page("build/", "Собрать велосипед самому", body, [("Собрать самому", None)])
idx("Как собрать велосипед самому", "build/", "Руководство", BUILD_INTRO + " " + " ".join(t + " " + x for t, x in BUILD_STEPS))
# glossary
R = Rof("glossary/")
terms = []
for p in PARTS: terms.append((p["ru"], p["en"], p["short"], f"parts/{p['id']}/", "p-" + p["id"]))
for t in TOOLS: terms.append((t["ru"], t["en"], re.split(r"(?<=[.!])\s", t["text"])[0], f"tools/{t['id']}/", "t-" + t["id"]))
for tid, ru, en, d, link in TERMS:
    url = path_of(*link.split(":", 1)) if link else ""
    terms.append((ru, en, d, url, tid))
terms.sort(key=lambda x: x[0].lower().replace("ё", "е").lstrip("«"))
letters, rows = [], ""
cur = None
for ru, en, d, url, tid in terms:
    L = ru.lstrip("«")[0].upper()
    if L != cur:
        cur = L; letters.append(L); rows += f'<h2 id="l-{L}" class="letter">{L}</h2>'
    name = f'<a href="{R}{url}">{html.escape(ru)}</a>' if url else html.escape(ru)
    rows += f'<div class="term" id="{tid}"><dt>{name} <span class="en">{html.escape(en)}</span></dt><dd>{inline(d, R)}</dd></div>'
    if not tid.startswith(("p-", "t-")): idx(ru, f"glossary/#{tid}", "Термин", d, en)
body = f'<h1>Словарь велосипедных терминов</h1><p class="lead">{len(terms)} терминов: русское название, английский вариант (как пишут в мануалах и магазинах) и короткое объяснение. Название ведёт на подробную страницу.</p><nav class="letters">' + "".join(f'<a href="#l-{L}">{L}</a>' for L in letters) + f"</nav><dl class='gloss'>{rows}</dl>"
page("glossary/", "Словарь терминов", body, [("Словарь", None)])
# credits
R = Rof("credits/")
rows = "".join(f'<tr id="{k}"><td><img src="{R}img/photos/{k}.webp" alt="" loading="lazy"></td><td><a href="{html.escape(c["source"])}">{html.escape(c["file"])}</a></td><td>{html.escape(c["author"])}</td><td>' + (f'<a href="{html.escape(c["license_url"])}">{html.escape(c["license"])}</a>' if c.get("license_url") else html.escape(c["license"])) + "</td></tr>" for k, c in sorted(CRED.items()))
body = f'<h1>Источники фотографий и лицензии</h1><p class="lead">Все фотографии на сайте — реальные снимки с Wikimedia Commons, распространяемые под свободными лицензиями (общественное достояние, CC0, CC BY, CC BY-SA). Изображения уменьшены и переведены в формат WebP; иных изменений не вносилось. Схемы и чертежи нарисованы специально для сайта.</p><div class="tablewrap"><table class="cred"><thead><tr><th></th><th>Файл (ссылка на источник)</th><th>Автор</th><th>Лицензия</th></tr></thead><tbody>{rows}</tbody></table></div>'
page("credits/", "Источники и лицензии", body, [("Источники фото", None)])
# home
R = ""
sec = [("history/", "История", f"{len(HISTORY)} вех: от дрезины 1817 года до e-bike", "penny"),
       ("anatomy/", "Устройство", f"Интерактивная схема и {len(PARTS)} деталей", "crankset"),
       ("types/", "Типы велосипедов", f"{len(TYPES)} типов: шоссе, МТБ, город, BMX…", "mtb"),
       ("guides/", "Инструкции", f"{len(GUIDES)} пошаговых инструкций", "nexus7"),
       ("tools/", "Инструмент", f"{len(TOOLS)} инструментов: что и зачем", "park-tools"),
       ("makers/", "Производители", f"{len(MAKERS)} брендов и стран", "rear-derailleur"),
       ("build/", "Собрать самому", "Совместимость и порядок сборки", "chain-tool"),
       ("glossary/", "Словарь", "Термины RU / EN с объяснением", "valves")]
cards = "".join(card(R, h, t, s, i) for h, t, s, i in sec)
path_g = ["m-check", "nexus-tube", "chain-clean", "rd-adjust", "wheel-true", "lefty-service"]
pg = "".join(f'<a class="pathstep" href="guides/{g}/">{badge(G[g]["level"])}<span>{html.escape(G[g]["title"])}</span></a>' for g in path_g)
body = f"""<section class="hero"><div><h1>Вело-вселенная</h1><p class="lead">Всё о велосипедах в одном месте: история, устройство, названия деталей, инструмент и пошаговые инструкции — от замены камеры на планетарной втулке до разбора вилки Cannondale Lefty.</p>
<p class="stats"><span><b>{len(HISTORY)}</b> вех истории</span><span><b>{len(PARTS)}</b> деталей</span><span><b>{len(TYPES)}</b> типов</span><span><b>{len(TOOLS)}</b> инструментов</span><span><b>{len(GUIDES)}</b> инструкций</span><span><b>{len(terms)}</b> терминов</span></p></div>
<div class="herosvg">{DIAGRAMS['anatomy'][1](R)}</div></section>
<h2>Разделы</h2><div class="grid">{cards}</div>
<h2>Мастерская: от простого к сложному</h2><div class="path">{pg}</div>
<h2>С чего начать</h2><div class="grid three"><a class="card" href="anatomy/"><div><h3>Не знаю, как что называется</h3><p>Откройте схему и нажмите на деталь.</p></div></a><a class="card" href="guides/nexus-tube/"><div><h3>Проколол колесо на городском велосипеде</h3><p>Замена камеры на втулке Shimano Nexus.</p></div></a><a class="card" href="tools/"><div><h3>Собираю набор инструмента</h3><p>Что купить в первую очередь.</p></div></a></div>"""
page("index.html", "Энциклопедия и мастерская велосипеда", body, (), "Вело-вселенная: история, устройство, типы велосипедов, инструмент и пошаговые инструкции по ремонту")
page("404.html", "Страница не найдена", '<h1>Страница не найдена</h1><p>Попробуйте поиск вверху или вернитесь на <a href="/velo-universe/">главную</a>.</p>')
for h, t, s, i in sec: idx(t, h, "Раздел", s)
f404 = os.path.join(SITE, "404.html"); open(f404, "w").write(open(f404).read().replace("<head>", '<head><base href="/velo-universe/">', 1))
json.dump(SEARCH, open(os.path.join(SITE, "search.json"), "w"), ensure_ascii=False, separators=(",", ":"))
if errors:
    print("\n".join(sorted(set(errors)))); sys.exit(1)
print("OK", "parts", len(PARTS), "tools", len(TOOLS), "guides", len(GUIDES), "types", len(TYPES), "history", len(HISTORY), "makers", len(MAKERS), "terms", len(terms), "photos", len(CRED), "search", len(SEARCH))
