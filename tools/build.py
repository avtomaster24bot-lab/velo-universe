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
from art_compat import A_COMPAT
from art_susp_ebike import A_SUSP, A_EBIKE
from art_other import A_BUY, A_FRAMES, A_HIST
from round3 import TOOLS3, GUIDES3, TERMS3, A_R3, TROUBLE, TCATS3, MAINT, MAINT_LINKS, CATEYE, CATEYE_SRC
_g3 = {g["id"] for g in GUIDES3}
GUIDES[:] = [g for g in GUIDES if g["id"] not in _g3] + GUIDES3
TOOLS += TOOLS3; TERMS += TERMS3
A_COMPAT += A_R3
for g in GUIDES:
    if g["id"] == "hydraulic-bleed": g["note"] = "Пошагово для конкретных марок: [[guide:bleed-shimano|Shimano]], [[guide:bleed-sram|SRAM (DOT)]], [[guide:bleed-magura|Magura]]. После прокачки — [[guide:pad-bedin|приработка колодок]]."
    if g["id"] == "disc-pads": g["note"] = "Новые колодки нужно приработать: [[guide:pad-bedin|как это сделать]]."
for t in TOOLS:
    if t["id"] == "torque-wrench": t["tips"] = t["tips"] + ["Моменты из руководств Shimano, SRAM и Campagnolo — в [[art:torque-table|таблице моментов]]"]; t.setdefault("img", "torque-click")
for p in PARTS:
    if p["id"] == "tyre": p.setdefault("specs", []).append("Длина окружности колеса для велокомпьютера — [[page:calc#wheelsize|калькулятор и таблица]]; совместимость с ободом — [[art:compat-tyre-rim|статья]].")
    if p["id"] == "rim": p.setdefault("specs", []).append("Какие покрышки подходят ободу, маркировка C / TC / TSS (hookless) — [[art:compat-tyre-rim|статья]].")
    if p["id"] == "tubeless": p["guides"] = p["guides"] + ["tubeless-plug"]
    if p["id"] == "disc-brake": p["guides"] = p["guides"] + ["bleed-shimano", "bleed-sram", "bleed-magura", "pad-bedin"]
ARTICLES = A_COMPAT + A_SUSP + A_EBIKE + A_BUY + A_FRAMES + A_HIST
ACATS = [("compat", "Совместимость и стандарты", "compat/", "Какие детали подходят друг к другу: трансмиссия, каретки, колонки, тормоза, оси, размеры колёс."),
 ("susp", "Подвеска", "suspension/", "Как устроена подвеска, производители вилок и амортизаторов, настройка и обслуживание."),
 ("ebike", "Электровелосипеды", "ebike/", "Типы приводов, системы Bosch, Shimano, Yamaha, Panasonic, Bafang, безопасность батарей и уход."),
 ("buy", "Покупка и подбор", "buy/", "Как выбрать размер рамы и проверить б/у велосипед перед покупкой."),
 ("frames", "Рамостроение", "frames/", "Как делают рамы и с чего начать, если хочется построить раму самому."),
 ("hist", "История: подробнее", "history/#more", "")]
A = {a["id"]: a for a in ARTICLES}
EXT = {"checklist": "https://avtomaster24bot-lab.github.io/bike-checklist/"}
from svgs import DIAGRAMS
SITE = os.path.join(ROOT, "site")
CRED = json.load(open(os.path.join(ROOT, "content/credits.json")))
LEVEL = {1: ("Легко", "easy"), 2: ("Средне", "mid"), 3: ("Сложно", "hard")}
P = {p["id"]: p for p in PARTS}; T = {t["id"]: t for t in TOOLS}; G = {g["id"]: g for g in GUIDES}; TY = {t["id"]: t for t in TYPES}
PAGES = {"trouble": "trouble/", "maintenance": "maintenance/", "calc": "calc/", "compat": "compat/", "suspension": "suspension/", "ebike": "ebike/", "buy": "buy/", "frames": "frames/", "history": "history/", "anatomy": "anatomy/", "types": "types/", "tools": "tools/", "guides": "guides/", "makers": "makers/", "build": "build/", "glossary": "glossary/", "credits": "credits/", "parts": "anatomy/#parts"}
errors = []
def path_of(kind, ident):
    base, _, frag = ident.partition("#")
    frag = ("#" + frag) if frag else ""
    if kind == "part": ok, p = base in P, f"parts/{base}/"
    elif kind == "tool": ok, p = base in T, f"tools/{base}/"
    elif kind == "guide": ok, p = base in G, f"guides/{base}/"
    elif kind == "type": ok, p = base in TY, f"types/{base}/"
    elif kind == "page": ok, p = base in PAGES, PAGES.get(base, "")
    elif kind == "art": ok, p = base in A, f"a/{base}/"
    elif kind == "ext": ok, p = base in EXT, EXT.get(base, "")
    else: ok, p = False, ""
    if not ok: errors.append(f"bad ref {kind}:{ident}")
    return p + frag
def name_of(kind, ident):
    return {"part": lambda i: P[i]["ru"], "tool": lambda i: T[i]["ru"], "guide": lambda i: G[i]["title"], "type": lambda i: TY[i]["ru"], "art": lambda i: A[i]["title"]}.get(kind, lambda i: i)(ident)
def md(text, R):
    def rep(m):
        kind, ident, label = m.group(1), m.group(2), m.group(3)
        pre = "" if kind == "ext" else R
        return f'<a href="{pre}{path_of(kind, ident)}">{html.escape(label or name_of(kind, ident))}</a>'
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
NAV = [("trouble/", "Что случилось?"), ("history/", "История"), ("anatomy/", "Устройство"), ("types/", "Типы"), ("guides/", "Инструкции"), ("tools/", "Инструмент"), ("compat/", "Совместимость"), ("calc/", "Калькуляторы"), ("suspension/", "Подвеска"), ("ebike/", "Электро"), ("buy/", "Покупка"), ("makers/", "Производители"), ("build/", "Собрать самому"), ("frames/", "Рамы"), ("maintenance/", "Чек-лист ТО"), ("glossary/", "Словарь")]
def page(rel, title, body, crumbs=(), desc="", js=""):
    depth = rel.count("/") if rel.endswith("/") else rel.count("/")
    R = "../" * depth
    nav = "".join(f'<a href="{R}{h}">{n}</a>' for h, n in NAV)
    bc = ""
    if crumbs:
        bc = '<nav class="crumbs" aria-label="Навигация"><a href="' + R + '">Главная</a>' + "".join(
            (f' <span>›</span> <a href="{R}{h}">{html.escape(n)}</a>' if h else f' <span>›</span> <b>{html.escape(n)}</b>') for n, h in crumbs) + "</nav>"
    extra_js = f'<script src="{"../" * (rel.count("/"))}js/{js}" defer></script>' if js else ""
    doc = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — Вело-вселенная</title><meta name="description" content="{html.escape(desc or title)}">
<link rel="icon" href="{R}img/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{R}css/style.css?v=5"><link rel="manifest" href="{R}manifest.webmanifest"><meta name="theme-color" content="#0f766e"><link rel="apple-touch-icon" href="{R}img/icon-192.png">
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
<script src="{R}js/app.js?v=3" defer></script>{extra_js}</body></html>"""
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
arts_of = {}
for a_ in ARTICLES:
    for k_ in ("parts", "guides", "types", "tools"):
        for x_ in a_.get(k_, []): arts_of.setdefault((k_, x_), []).append(a_["id"])
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
    body += related([("Инструкции", guides_html), ("Инструмент", chips("tool", p["tools"], R)), ("Где встречается", chips("type", types_of_part.get(p["id"], []), R)), ("Статьи", chips("art", arts_of.get(("parts", p["id"]), []), R)), ("Соседние детали", chips("part", others, R))])
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
    body += related([("Детали", chips("part", g["parts"], R)), ("Инструмент", chips("tool", g["tools"], R)), ("Типы велосипедов", tchips), ("Статьи", chips("art", arts_of.get(("guides", g["id"]), []), R))])
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
    body += related([("Инструкции для этого типа", guides_html), ("Ключевые детали", chips("part", t["parts"], R)), ("Статьи", chips("art", arts_of.get(("types", t["id"]), []), R)), ("Другие типы", chips("type", [x["id"] for x in TYPES if x["id"] != t["id"]], R))])
    page(rel, t["ru"], body, [("Типы велосипедов", "types/"), (t["ru"], None)], t["short"])
    idx(t["ru"], rel, "Тип велосипеда", t["short"] + " " + t["text"], t["en"])
# ---------------- Index pages
def strip(t): return re.sub(r"\[\[\w+:[\w#-]+\|?([^\]]*)\]\]", r"\1", t)
def imgof(a):
    i = a.get("img"); return i[0] if isinstance(i, list) else i
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
    def yk(x):
        m = re.search(r"\d{4}", x["year"]); return int(m.group()) if m else (1950 if "XX" in x["year"] else 0)
    for h in sorted([x for x in HISTORY if x["era"] == eid], key=yk):
        tl += f'<li><div class="yr">{html.escape(h["year"])}</div><div class="tbody"><h3>{html.escape(h["title"])}</h3><p>{inline(h["text"], R)}</p>{fig(h.get("img"), R, "tl")}</div></li>'
    tl += "</ol>"
body = f'<h1>История велосипеда</h1><p class="lead">От «беговой машины» Карла Драйса 1817 года до электровелосипедов и электронных переключателей — {len(HISTORY)} ключевых событий. Только проверенные факты; спорные версии помечены.</p>{fig("rover-ad", R, "float")}{tl}<section id="more"><h2>Подробнее</h2><div class="grid">' + "".join(card(R, f"a/{a['id']}/", a["title"], html.escape(strip(a["intro"])[:120]) + "…", imgof(a)) for a in A_HIST) + "</div></section>"
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
# ---------------- Articles
acn = {c[0]: c for c in ACATS}
def table_html(t, R):
    return '<div class="tablewrap"><table><thead><tr>' + "".join(f"<th>{html.escape(h)}</th>" for h in t["head"]) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{inline(c, R)}</td>" for c in row) + "</tr>" for row in t["rows"]) + "</tbody></table></div>"
for a in ARTICLES:
    rel = f"a/{a['id']}/"; R = Rof(rel)
    secs = ""
    for sec in a["sections"]:
        x = f'<section><h2>{html.escape(sec["h"])}</h2>'
        if sec.get("text"): x += P_html(sec["text"], R)
        if sec.get("list"): x += "<ul>" + "".join(f"<li>{inline(i, R)}</li>" for i in sec["list"]) + "</ul>"
        if sec.get("table"): x += table_html(sec["table"], R)
        if sec.get("img"): x += fig(sec["img"], R, "tl")
        secs += x + "</section>"
    imgs = a.get("img"); imgs = imgs if isinstance(imgs, list) else ([imgs] if imgs else [])
    ph = '<div class="photos">' + "".join(fig(i, R) for i in imgs) + "</div>" if imgs else ""
    cid, cname, chref, _ = acn[a["cat"]]
    same = [x["id"] for x in ARTICLES if x["cat"] == a["cat"] and x["id"] != a["id"]]
    body = f'<article class="item art"><div class="kicker">{cname}</div><h1>{html.escape(a["title"])}</h1><p class="lead">{inline(a["intro"], R)}</p>{ph}{secs}</article>'
    body += related([("Детали", chips("part", a.get("parts", []), R)), ("Инструкции", chips("guide", a.get("guides", []), R)), ("Инструмент", chips("tool", a.get("tools", []), R)), ("Типы велосипедов", chips("type", a.get("types", []), R)), ("Ещё в разделе", chips("art", same, R))])
    page(rel, a["title"], body, [(cname, chref), (a["title"], None)], strip(a["intro"])[:150])
    alltext = a["intro"] + " " + " ".join(sec.get("text", "") + " " + " ".join(sec.get("list", [])) + " " + " ".join(" ".join(r) for r in sec.get("table", {}).get("rows", [])) for sec in a["sections"])
    idx(a["title"], rel, "Статья · " + cname, alltext)
EXTRA = {"compat": [("art", "Калькуляторы", "calc/")], "susp": [("guide", "sag-setup", None), ("guide", "fork-lowers", None), ("guide", "lefty-service", None)],
         "ebike": [("guide", "ebike-care", None)], "buy": [("guide", "m-check", None), ("guide", "bike-fit-saddle", None)], "frames": [("page", "Собрать велосипед самому", "build/")]}
for cid, cname, chref, cdesc in ACATS:
    if cid == "hist": continue
    R = Rof(chref)
    cards = "".join(card(R, f"a/{a['id']}/", a["title"], html.escape(strip(a["intro"])[:130]) + "…", imgof(a)) for a in ARTICLES if a["cat"] == cid)
    ex = ""
    for kind, x, href in EXTRA.get(cid, []):
        if kind == "guide": ex += card(R, f"guides/{x}/", G[x]["title"], badge(G[x]["level"]) + " Инструкция")
        else: ex += card(R, href, x, "Раздел")
    body = f'<h1>{cname}</h1><p class="lead">{cdesc}</p><div class="grid">{cards}{ex}</div>'
    page(chref, cname, body, [(cname, None)], cdesc)
    idx(cname, chref, "Раздел", cdesc)
# ---------------- Calculators
R = Rof("calc/")
calc_body = f"""<h1>Калькуляторы</h1><p class="lead">Расчёты выполняются прямо в браузере. Результаты — ориентировочные: для точной подборки деталей сверяйтесь с данными производителя.</p>
<p class="chips"><a href="#tyre">Размер шины</a> <a href="#gear">Передачи и скорость</a> <a href="#chain">Длина цепи</a> <a href="#spoke">Длина спиц</a> <a href="#pressure">Давление в шинах</a> <a href="#wheelsize">Окружность колеса для велокомпьютера</a></p>
<section class="calc" id="tyre"><h2>Размер шины: ETRTO ↔ дюймы ↔ французская система</h2>
<label>Посадочный диаметр (BSD)<select id="t_bsd"></select></label><label>Ширина шины, мм<input id="t_w" type="number" value="37" min="16" max="130"></label>
<div class="out" id="t_out"></div><p class="disc">Полная таблица размеров — в статье <a href="{R}a/compat-wheels/">«Размеры колёс и шин»</a>.</p></section>
<section class="calc" id="gear"><h2>Передаточные отношения, gear inches и скорость</h2>
<label>Передние звёзды (через запятую)<input id="g_rings" value="50, 34"></label><label>Кассета (через запятую)<input id="g_cogs" value="11, 12, 13, 14, 15, 17, 19, 21, 24, 28"></label>
<label>Обод (BSD)<select id="g_bsd"></select></label><label>Ширина шины, мм<input id="g_w" type="number" value="28"></label><label>Каденс, об/мин<input id="g_cad" type="number" value="90"></label>
<div class="out" id="g_out"></div></section>
<section class="calc" id="chain"><h2>Длина цепи (ориентировочно)</h2>
<label>Длина нижних перьев, мм<input id="c_cs" type="number" value="430"></label><label>Самая большая передняя звезда<input id="c_f" type="number" value="50"></label><label>Самая большая задняя звезда<input id="c_r" type="number" value="28"></label>
<div class="out" id="c_out"></div></section>
<section class="calc" id="spoke"><h2>Длина спиц</h2>
<label>ERD обода, мм<input id="s_erd" type="number" value="600" step="0.1"></label><label>Диаметр фланца (PCD), мм<input id="s_pcd" type="number" value="45" step="0.1"></label>
<label>Центр → левый фланец, мм<input id="s_wl" type="number" value="35" step="0.1"></label><label>Центр → правый фланец, мм<input id="s_wr" type="number" value="20" step="0.1"></label>
<label>Спиц в колесе<input id="s_n" type="number" value="32"></label><label>Кресты<input id="s_x" type="number" value="3" min="0" max="4"></label><label>Отверстие фланца, мм<input id="s_h" type="number" value="2.6" step="0.1"></label>
<div class="out" id="s_out"></div><p class="disc">Как собрать колесо — <a href="{R}guides/wheel-build/">инструкция</a>.</p></section>
<section class="calc" id="pressure"><h2>Давление в шинах — приблизительный ориентир</h2>
<label>Ширина шины, мм<input id="p_w" type="number" value="35"></label><label>Вес ездока с велосипедом, кг<input id="p_kg" type="number" value="85"></label>
<label>Покрытие<select id="p_s"><option value="asphalt">Асфальт</option><option value="gravel">Грунт, гравий</option><option value="trail">Тропы МТБ</option><option value="snow">Снег, песок (фэтбайк)</option></select></label>
<label>Бескамерка<input id="p_tl" type="checkbox"></label>
<div class="out" id="p_out"></div><p class="disc">Как накачивать — <a href="{R}guides/pumping/">инструкция</a>.</p></section>
<section class="calc" id="wheelsize"><h2>Окружность колеса для велокомпьютера</h2>
<p>Велокомпьютер считает скорость и пробег по оборотам колеса, поэтому ему нужна длина окружности колеса. Обычно её вводят в миллиметрах (4 цифры) или, в некоторых моделях, в сантиметрах (3 цифры). Выберите размер по маркировке ETRTO на боковине покрышки (например, 37-622 = 700×37C = 28×1,40) или введите свой замер.</p>
<label>Посадочный диаметр (BSD)<select id="w_bsd"></select></label><label>Ширина шины, мм<input id="w_w" type="number" value="25" min="16" max="130"></label><label>Свой замер роллаутом, мм (необязательно)<input id="w_ro" type="number" placeholder="например 2112"></label>
<div class="out" id="w_out"></div>
<h3>Как измерить точно (роллаут)</h3><ol><li>Накачайте шину до обычного давления. Поставьте колесо с датчиком так, чтобы ниппель был в самой нижней точке, и отметьте это место на полу.</li><li>Сядьте на велосипед (с вашим весом шина проминается) и прокатите его ровно на один оборот колеса — пока ниппель снова не окажется внизу. Отметьте вторую точку.</li><li>Измерьте расстояние между отметками рулеткой в миллиметрах (дюймы × 25,4 = мм) и введите его в велокомпьютер.</li></ol>
<h3>Таблица окружностей (Cateye)</h3><p class="disc">Значения из опубликованной таблицы производителя велокомпьютеров Cateye (<a href="{CATEYE_SRC}">cateye.com, раздел поддержки</a>), выборка распространённых размеров. Cateye указывает, что реальная окружность зависит от давления, а значения в таблицах разных лет могут немного отличаться. Отдельных «кодов размера колеса» в новых приборах Cateye нет — вводится сама длина окружности; у других марок (Sigma, Garmin и т. д.) смотрите их руководства: в большинстве современных приборов также вводятся миллиметры или окружность определяется автоматически по GPS.</p>
<div class="tablewrap"><table><thead><tr><th>ETRTO</th><th>Размер</th><th>Окружность, мм</th><th>см</th></tr></thead><tbody>{"".join(f"<tr><td>{a}</td><td>{b}</td><td><b>{c}</b></td><td>{round(c/10)}</td></tr>" for a, b, c in CATEYE)}</tbody></table></div>
<script id="cateye" type="application/json">{json.dumps(CATEYE)}</script></section>"""
page("calc/", "Калькуляторы", calc_body, [("Калькуляторы", None)], "Калькуляторы: размер шины ETRTO, передачи и скорость, длина цепи, длина спиц, давление", js="calc.js?v=3")
for t_, a_ in [("Калькулятор размера шины ETRTO", "tyre"), ("Калькулятор передач, gear inches и скорости", "gear"), ("Калькулятор длины цепи", "chain"), ("Калькулятор длины спиц", "spoke"), ("Давление в шинах — ориентир", "pressure"), ("Окружность колеса для велокомпьютера (коды размера колеса)", "wheelsize")]:
    idx(t_, f"calc/#{a_}", "Калькулятор", t_)

# ---------------- Troubleshooting
R = Rof("trouble/")
tcn = dict(TCATS3)
def tlinks(t, R):
    out = []
    if t["guides"]: out.append("<span><b>Инструкции:</b> " + ", ".join(f'<a href="{R}guides/{g}/">{html.escape(G[g]["title"])}</a>' for g in t["guides"]) + "</span>")
    if t["parts"]: out.append("<span><b>Детали:</b> " + ", ".join(f'<a href="{R}parts/{p}/">{html.escape(P[p]["ru"])}</a>' for p in t["parts"]) + "</span>")
    if t["tools"]: out.append("<span><b>Инструмент:</b> " + ", ".join(f'<a href="{R}tools/{x}/">{html.escape(T[x]["ru"])}</a>' for x in t["tools"]) + "</span>")
    for k, ids in (("guide", t["guides"]), ("part", t["parts"]), ("tool", t["tools"])):
        for i in ids: path_of(k, i)
    return '<div class="tl">' + "".join(out) + "</div>"
tcards = "".join(f'''<details class="tcard" id="{t["id"]}" data-c="{t["cat"]}"><summary>{html.escape(t["title"])}<span class="tk">{tcn[t["cat"]]}</span></summary><p class="signs">{inline(t["signs"], R)}</p><ol class="causes">''' + "".join(f"<li><b>{inline(c, R)}</b>{inline(d, R)}</li>" for c, d in t["causes"]) + f"</ol>{tlinks(t, R)}</details>" for t in TROUBLE)
tf = '<div class="filters" id="tf"><button data-c="all" class="on">Все</button>' + "".join(f'<button data-c="{c}">{n}</button>' for c, n in TCATS3) + "</div>"
body = f"""<h1>Что случилось? Поиск неисправностей</h1><p class="lead">Выберите симптом — увидите вероятные причины от самых частых к редким, что проверить и ссылки на инструкции, детали и инструмент. Начинайте с простого: большинство проблем — это грязь, смазка, давление и регулировка.</p>
<div class="tfbar"><input id="tq" type="search" placeholder="Опишите проблему: скрип, цепь слетает, тормоз трёт…" aria-label="Фильтр симптомов"><span id="tn" class="muted small"></span></div>{tf}<div class="tcards">{tcards}</div>
<div class="warn"><b>⚠ Важно</b><ul><li>Если что-то не так с тормозами, рулём, вилкой или рамой (трещины, люфт, утечка) — не ездите до ремонта.</li><li>Причины перечислены как вероятные, а не единственно возможные. Если не уверены — покажите велосипед мастеру.</li></ul></div>"""
page("trouble/", "Что случилось? Поиск неисправностей", body, [("Что случилось?", None)], "Поиск неисправностей велосипеда: скрипы, передачи, тормоза, колёса, подвеска, планетарные втулки, e-bike", js="extra.js?v=1")
idx("Что случилось? Поиск неисправностей", "trouble/", "Раздел", "неисправность симптом диагностика скрип не работает сломалось")
for t in TROUBLE: idx(t["title"], f"trouble/#{t['id']}", "Неисправность", t["signs"] + " " + " ".join(c for c, d in t["causes"]))
# ---------------- Maintenance checklist
R = Rof("maintenance/")
msecs = ""
for sid, sn, items in MAINT:
    lis = "".join(f'<li><label><input type="checkbox" id="m-{sid}-{i}"> <span>{html.escape(x)}</span></label></li>' for i, x in enumerate(items))
    lk = ", ".join(f'<a href="{R}guides/{g}/">{html.escape(G[g]["title"])}</a>' for g in MAINT_LINKS[sid])
    for g in MAINT_LINKS[sid]: path_of("guide", g)
    msecs += f'<section><h2>{sn}</h2><ul>{lis}</ul><p class="mlinks no-print">Инструкции: {lk}</p></section>'
body = f"""<h1>Чек-лист обслуживания велосипеда</h1><p class="lead">Что проверять перед каждой поездкой, раз в неделю, в месяц и в сезон. Отметки сохраняются в этом браузере; лист можно распечатать и повесить в мастерской. Интервалы общие — для конкретных узлов (вилка, тормоза, планетарная втулка, e-bike) действуют рекомендации производителя.</p>
<div class="mbtns"><button id="mprint" class="pri">🖨 Распечатать</button><button id="mreset">Сбросить отметки</button></div>
<p class="print-only">Вело-вселенная · avtomaster24bot-lab.github.io/velo-universe/maintenance/ · Велосипед: ____________ Дата: ________</p>
<div class="mcheck">{msecs}</div><p class="no-print">Что-то не так? — <a href="{R}trouble/">поиск неисправностей</a>. Моменты затяжки — <a href="{R}a/torque-table/">таблица</a>.</p>"""
page("maintenance/", "Чек-лист обслуживания", body, [("Чек-лист ТО", None)], "Чек-лист обслуживания велосипеда: перед поездкой, раз в неделю, в месяц, в сезон — с печатью", js="extra.js?v=1")
idx("Чек-лист обслуживания (для печати)", "maintenance/", "Раздел", "обслуживание ТО регламент проверка перед поездкой неделя месяц сезон печать " + " ".join(" ".join(i) for _, _, i in MAINT))
# home
R = ""
sec = [("trouble/", "Что случилось?", f"{len(TROUBLE)} симптомов: причины и что делать", "worn-pads"),
       ("history/", "История", f"{len(HISTORY)} вех: от дрезины 1817 года до e-bike", "penny"),
       ("anatomy/", "Устройство", f"Интерактивная схема и {len(PARTS)} деталей", "crankset"),
       ("types/", "Типы велосипедов", f"{len(TYPES)} типов: шоссе, МТБ, город, BMX…", "mtb"),
       ("guides/", "Инструкции", f"{len(GUIDES)} пошаговых инструкций", "nexus7"),
       ("tools/", "Инструмент", f"{len(TOOLS)} инструментов: что и зачем", "park-tools"),
       ("makers/", "Производители", f"{len(MAKERS)} брендов и стран", "rear-derailleur"),
       ("build/", "Собрать самому", "Совместимость и порядок сборки", "chain-tool"),
       ("glossary/", "Словарь", "Термины RU / EN с объяснением", "valves"),
       ("compat/", "Совместимость", "Скорости, барабаны, каретки, колонки, тормоза, оси", "headset-exploded"),
       ("calc/", "Калькуляторы", "Шины, передачи, цепь, спицы, давление, велокомпьютер", "wheel-build"),
       ("suspension/", "Подвеска", "RockShox, Fox, SR Suntour, Lefty, настройка сага", "fox-float"),
       ("ebike/", "Электровелосипеды", "Bosch, Shimano, Yamaha, Panasonic, Bafang, батареи", "bosch-cx"),
       ("buy/", "Покупка и подбор", "Б/у японский велосипед, размер рамы", "bridgestone"),
       ("frames/", "Рамостроение", "Муфты, TIG, пайка, карбон, бамбук", "lugs-head"),
       ("maintenance/", "Чек-лист обслуживания", "Перед поездкой, неделя, месяц, сезон — можно распечатать", "torque-click")]
cards = "".join(card(R, h, t, s, i) for h, t, s, i in sec)
path_g = ["m-check", "nexus-tube", "sag-setup", "chain-clean", "rd-adjust", "sa3-tube", "wheel-true", "wheel-build", "lefty-service"]
pg = "".join(f'<a class="pathstep" href="guides/{g}/">{badge(G[g]["level"])}<span>{html.escape(G[g]["title"])}</span></a>' for g in path_g)
body = f"""<section class="hero"><div><h1>Вело-вселенная</h1><p class="lead">Всё о велосипедах в одном месте: история, устройство, названия деталей, инструмент и пошаговые инструкции — от замены камеры на планетарной втулке до разбора вилки Cannondale Lefty.</p>
<p class="stats"><span><b>{len(HISTORY)}</b> вех истории</span><span><b>{len(PARTS)}</b> деталей</span><span><b>{len(TYPES)}</b> типов</span><span><b>{len(TOOLS)}</b> инструментов</span><span><b>{len(GUIDES)}</b> инструкций</span><span><b>{len(terms)}</b> терминов</span><span><b>{len(ARTICLES)}</b> статей</span><span><b>6</b> калькуляторов</span></p></div>
<div class="herosvg">{DIAGRAMS['anatomy'][1](R)}</div></section>
<h2>Разделы</h2><div class="grid">{cards}</div>
<h2>Мастерская: от простого к сложному</h2><div class="path">{pg}</div>
<h2>С чего начать</h2><div class="grid three"><a class="card" href="anatomy/"><div><h3>Не знаю, как что называется</h3><p>Откройте схему и нажмите на деталь.</p></div></a><a class="card" href="guides/nexus-tube/"><div><h3>Проколол колесо на городском велосипеде</h3><p>Замена камеры на втулке Shimano Nexus.</p></div></a><a class="card" href="tools/"><div><h3>Собираю набор инструмента</h3><p>Что купить в первую очередь.</p></div></a></div>"""
page("index.html", "Энциклопедия и мастерская велосипеда", body, (), "Вело-вселенная: история, устройство, типы велосипедов, инструмент и пошаговые инструкции по ремонту")
page("offline/", "Нет соединения", '<h1>Нет соединения с интернетом</h1><p class="lead">Эта страница ещё не сохранена для офлайн-чтения. Открытые раньше страницы, калькуляторы, поиск неисправностей и чек-лист доступны без сети.</p><p><a href="../">На главную</a> · <a href="../trouble/">Что случилось?</a> · <a href="../calc/">Калькуляторы</a> · <a href="../maintenance/">Чек-лист</a></p>')
import time as _t
open(os.path.join(SITE, "sw.js"), "w").write(open(os.path.join(ROOT, "tools/sw.template.js")).read().replace("__V__", _t.strftime("%Y%m%d%H%M%S")))
page("404.html", "Страница не найдена", '<h1>Страница не найдена</h1><p>Попробуйте поиск вверху или вернитесь на <a href="/velo-universe/">главную</a>.</p>')
for h, t, s, i in sec: idx(t, h, "Раздел", s)
f404 = os.path.join(SITE, "404.html"); open(f404, "w").write(open(f404).read().replace("<head>", '<head><base href="/velo-universe/">', 1))
json.dump(SEARCH, open(os.path.join(SITE, "search.json"), "w"), ensure_ascii=False, separators=(",", ":"))
if errors:
    print("\n".join(sorted(set(errors)))); sys.exit(1)
print("OK", "parts", len(PARTS), "tools", len(TOOLS), "guides", len(GUIDES), "types", len(TYPES), "history", len(HISTORY), "makers", len(MAKERS), "terms", len(terms), "photos", len(CRED), "search", len(SEARCH))
