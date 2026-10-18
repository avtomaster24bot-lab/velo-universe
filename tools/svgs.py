import math
def _label(R, x, y, tx, ty, text, href, anchor="start"):
    # leader line from point (x,y) to label (tx,ty)
    a = f'<a href="{R}{href}" class="hot"><line x1="{x}" y1="{y}" x2="{tx}" y2="{ty}" class="lead"/><circle cx="{x}" cy="{y}" r="4" class="dot"/>'
    pad = 4
    a += f'<text x="{tx + (pad if anchor=="start" else -pad)}" y="{ty+4}" text-anchor="{anchor}" class="lbl">{text}</text></a>'
    return a

def spokes(cx, cy, r, n=18):
    s = ""
    for i in range(n):
        a = 2*math.pi*i/n
        s += f'<line x1="{cx}" y1="{cy}" x2="{cx+r*math.cos(a):.1f}" y2="{cy+r*math.sin(a):.1f}" class="thin"/>'
    return s

def anatomy(R):
    P = lambda p: f"parts/{p}/"
    rw, fw, bb = (230, 360), (690, 360), (420, 375)
    seat, ht_top, ht_bot = (385, 175), (610, 165), (625, 225)
    s = ['<svg viewBox="-190 30 1290 530" class="diagram" role="img" aria-label="Схема велосипеда с подписями деталей">']
    for c in (rw, fw):
        s.append(f'<circle cx="{c[0]}" cy="{c[1]}" r="150" class="tyre"/><circle cx="{c[0]}" cy="{c[1]}" r="138" class="rim"/>')
        s.append(spokes(c[0], c[1], 136, 24))
        s.append(f'<circle cx="{c[0]}" cy="{c[1]}" r="12" class="hubc"/>')
    # rotors
    s.append(f'<circle cx="{rw[0]}" cy="{rw[1]}" r="38" class="rotor"/>')
    # frame
    fr = [(seat, bb), (bb, ht_bot), (seat, ht_top), (ht_top, ht_bot), (bb, rw), (seat, rw)]
    for a, b in fr:
        s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" class="tube"/>')
    # fork
    s.append(f'<path d="M{ht_bot[0]} {ht_bot[1]} L{ht_bot[0]+10} {ht_bot[1]+40} Q{fw[0]-25} {fw[1]-60} {fw[0]} {fw[1]}" class="fork"/>')
    # seatpost & saddle
    s.append(f'<line x1="{seat[0]}" y1="{seat[1]}" x2="{seat[0]-12}" y2="{seat[1]-45}" class="post"/>')
    s.append(f'<path d="M{seat[0]-70} {seat[1]-50} Q{seat[0]-15} {seat[1]-62} {seat[0]+35} {seat[1]-52} L{seat[0]+30} {seat[1]-42} Q{seat[0]-20} {seat[1]-40} {seat[0]-68} {seat[1]-40} Z" class="saddle"/>')
    # stem + bar
    s.append(f'<line x1="{ht_top[0]}" y1="{ht_top[1]}" x2="{ht_top[0]-3}" y2="{ht_top[1]-25}" class="post"/>')
    s.append(f'<line x1="{ht_top[0]-3}" y1="{ht_top[1]-25}" x2="{ht_top[0]+45}" y2="{ht_top[1]-38}" class="post"/>')
    s.append(f'<path d="M{ht_top[0]+45} {ht_top[1]-38} q 10 -6 -25 -10" class="bar"/>')
    # chainring, crank, pedal
    s.append(f'<circle cx="{bb[0]}" cy="{bb[1]}" r="48" class="ring"/><circle cx="{bb[0]}" cy="{bb[1]}" r="10" class="hubc"/>')
    s.append(f'<line x1="{bb[0]}" y1="{bb[1]}" x2="{bb[0]+40}" y2="{bb[1]+72}" class="crank"/><rect x="{bb[0]+22}" y="{bb[1]+68}" width="38" height="10" rx="3" class="pedal"/>')
    # cassette + chain
    s.append(f'<circle cx="{rw[0]}" cy="{rw[1]}" r="26" class="ring"/>')
    s.append(f'<line x1="{rw[0]}" y1="{rw[1]-26}" x2="{bb[0]}" y2="{bb[1]-48}" class="chain"/>')
    s.append(f'<path d="M{rw[0]} {rw[1]+26} L{rw[0]+8} {rw[1]+52} L{rw[0]+22} {rw[1]+78} L{bb[0]} {bb[1]+48}" class="chain"/>')
    # derailleur
    s.append(f'<circle cx="{rw[0]+8}" cy="{rw[1]+46}" r="7" class="pulley"/><circle cx="{rw[0]+22}" cy="{rw[1]+78}" r="7" class="pulley"/><line x1="{rw[0]+5}" y1="{rw[1]+12}" x2="{rw[0]+22}" y2="{rw[1]+78}" class="cage"/>')
    # front caliper
    s.append(f'<rect x="{fw[0]-40}" y="{fw[1]-48}" width="22" height="14" rx="3" class="caliper" transform="rotate(25 {fw[0]-29} {fw[1]-41})"/>')
    s.append(f'<circle cx="{fw[0]}" cy="{fw[1]}" r="34" class="rotor"/>')
    L = []
    L.append(_label(R, seat[0]-20, seat[1]-50, 250, 70, "Седло", P("saddle"), "end"))
    L.append(_label(R, seat[0]-6, seat[1]-25, 250, 110, "Подседельный штырь", P("seatpost"), "end"))
    L.append(_label(R, seat[0], seat[1]+3, 250, 150, "Подседельный хомут", P("seat-clamp"), "end"))
    L.append(_label(R, 500, 170, 500, 60, "Рама (верхняя труба)", P("frame"), "middle"))
    L.append(_label(R, ht_top[0]+30, ht_top[1]-36, 700, 70, "Руль", P("handlebar")))
    L.append(_label(R, ht_top[0]+15, ht_top[1]-28, 700, 100, "Вынос", P("stem")))
    L.append(_label(R, ht_top[0]+2, ht_top[1]+5, 700, 130, "Рулевая колонка", P("headset")))
    L.append(_label(R, ht_bot[0]+3, ht_bot[1]-15, 760, 165, "Рулевой стакан", P("headtube")))
    L.append(_label(R, ht_bot[0]+30, ht_bot[1]+70, 800, 210, "Вилка", P("fork")))
    L.append(_label(R, fw[0]-28, fw[1]-40, 860, 250, "Тормозной суппорт", P("disc-brake")))
    L.append(_label(R, fw[0]+24, fw[1]+24, 860, 420, "Тормозной диск", P("rotor")))
    L.append(_label(R, fw[0], fw[1], 860, 360, "Втулка", P("hub")))
    L.append(_label(R, fw[0]+105, fw[1]-95, 860, 300, "Обод", P("rim")))
    L.append(_label(R, fw[0]+60, fw[1]+138, 860, 470, "Покрышка", P("tyre")))
    L.append(_label(R, fw[0]-60, fw[1]+70, 700, 540, "Спицы", P("spokes"), "middle"))
    L.append(_label(R, 530, 300, 560, 270, "Нижняя труба", P("frame")))
    L.append(_label(R, bb[0], bb[1], 470, 540, "Каретка", P("bb"), "middle"))
    L.append(_label(R, bb[0]-35, bb[1]+30, 330, 540, "Звезда", P("chainring"), "middle"))
    L.append(_label(R, bb[0]+25, bb[1]+45, 600, 500, "Шатун", P("crankset")))
    L.append(_label(R, bb[0]+50, bb[1]+73, 600, 470, "Педаль", P("pedals")))
    L.append(_label(R, 320, 395, 230, 540, "Цепь", P("chain"), "middle"))
    L.append(_label(R, rw[0]-18, rw[1]-18, 60, 230, "Кассета", P("cassette"), "end"))
    L.append(_label(R, rw[0]+22, rw[1]+78, 60, 500, "Задний переключатель", P("rear-derailleur"), "end"))
    L.append(_label(R, rw[0]+6, rw[1]+12, 60, 450, "Петух", P("hanger"), "end"))
    L.append(_label(R, rw[0], rw[1], 60, 360, "Дропаут / ось", P("dropouts"), "end"))
    L.append(_label(R, 300, 265, 60, 190, "Верхние перья", P("frame"), "end"))
    L.append(_label(R, 320, 370, 60, 290, "Нижние перья", P("frame"), "end"))
    L.append(_label(R, 400, 270, 300, 230, "Подседельная труба", P("frame"), "end"))
    L.append(_label(R, rw[0]-37, rw[1]+5, 60, 400, "Ротор", P("rotor"), "end"))
    s += L
    s.append('</svg>')
    return "".join(s)

def geometry(R):
    rw, fw, bb = (180, 330), (640, 330), (390, 352)
    seat, htt, htb = (350, 120), (570, 110), (590, 175)
    s = ['<svg viewBox="-10 60 990 445" class="diagram" role="img" aria-label="Геометрия рамы">']
    for c in (rw, fw): s.append(f'<circle cx="{c[0]}" cy="{c[1]}" r="130" class="rim ghost"/>')
    for a, b in [(seat,bb),(bb,htb),(seat,htt),(htt,htb),(bb,rw),(seat,rw)]:
        s.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" class="tube"/>')
    s.append(f'<path d="M{htb[0]} {htb[1]} L{htb[0]+12} {htb[1]+40} Q{fw[0]-20} {fw[1]-55} {fw[0]} {fw[1]}" class="fork"/>')
    # stack (vertical from bb to htt height) & reach
    s.append(f'<line x1="{htt[0]}" y1="{bb[1]}" x2="{htt[0]}" y2="{htt[1]}" class="dim"/><text x="{htt[0]+8}" y="240" class="dl">Stack (стек)</text>')
    s.append(f'<line x1="{bb[0]}" y1="{htt[1]}" x2="{htt[0]}" y2="{htt[1]}" class="dim"/><text x="{(bb[0]+htt[0])//2}" y="{htt[1]-8}" text-anchor="middle" class="dl">Reach (рич)</text>')
    s.append(f'<line x1="{bb[0]}" y1="{bb[1]}" x2="{bb[0]}" y2="{htt[1]}" class="dimg"/>')
    s.append(f'<line x1="{bb[0]}" y1="{bb[1]}" x2="{htt[0]}" y2="{bb[1]}" class="dimg"/>')
    # wheelbase
    s.append(f'<line x1="{rw[0]}" y1="455" x2="{fw[0]}" y2="455" class="dim"/><line x1="{rw[0]}" y1="{rw[1]}" x2="{rw[0]}" y2="460" class="dimg"/><line x1="{fw[0]}" y1="{fw[1]}" x2="{fw[0]}" y2="460" class="dimg"/><text x="{(rw[0]+fw[0])//2}" y="448" text-anchor="middle" class="dl">Колёсная база</text>')
    # chainstay
    s.append(f'<text x="{(rw[0]+bb[0])//2}" y="{(rw[1]+bb[1])//2+24}" text-anchor="middle" class="dl">Длина нижних перьев</text>')
    # BB drop
    s.append(f'<line x1="{rw[0]}" y1="{rw[1]}" x2="{fw[0]}" y2="{fw[1]}" class="dimg"/><line x1="{bb[0]+30}" y1="{rw[1]}" x2="{bb[0]+30}" y2="{bb[1]}" class="dim"/><text x="{bb[0]+36}" y="{bb[1]+2}" class="dl">Занижение каретки</text>')
    # head angle arc
    s.append(f'<path d="M{htb[0]+40} {htb[1]+105} A40 40 0 0 0 {htb[0]+24} {htb[1]+67}" class="dim"/><text x="{htb[0]+50}" y="{htb[1]+95}" class="dl">Угол рулевой трубы</text>')
    s.append(f'<line x1="{htb[0]-10}" y1="{htb[1]+105}" x2="{htb[0]+90}" y2="{htb[1]+105}" class="dimg"/><line x1="{htb[0]}" y1="{htb[1]}" x2="{htb[0]+38}" y2="{htb[1]+120}" class="dimg"/>')
    # seat angle
    s.append(f'<text x="{seat[0]-150}" y="{seat[1]+30}" class="dl">Угол подседельной трубы</text><line x1="{seat[0]-30}" y1="{seat[1]+35}" x2="{seat[0]+8}" y2="{seat[1]+50}" class="dimg"/>')
    # trail
    s.append(f'<line x1="{fw[0]}" y1="{fw[1]}" x2="{fw[0]}" y2="460" class="dimg"/><line x1="{htb[0]+38+ (460-htb[1]-120)*0.3:.0f}" y1="460" x2="{fw[0]}" y2="460" class="dim acc"/><text x="{fw[0]+10}" y="470" class="dl">Трейл</text>')
    s.append('</svg>')
    return "".join(s)

def drivetrain(R):
    P = lambda p: f"parts/{p}/"
    s = ['<svg viewBox="-190 10 1180 380" class="diagram" role="img" aria-label="Схема трансмиссии">']
    # chainring big at right, cassette at left
    cr, cs = (590, 190), (200, 170)
    for r in (105, 80): s.append(f'<circle cx="{cr[0]}" cy="{cr[1]}" r="{r}" class="ring"/>')
    for r in (60, 50, 41, 33, 26, 20): s.append(f'<circle cx="{cs[0]}" cy="{cs[1]}" r="{r}" class="ring thin2"/>')
    s.append(f'<circle cx="{cr[0]}" cy="{cr[1]}" r="12" class="hubc"/><circle cx="{cs[0]}" cy="{cs[1]}" r="9" class="hubc"/>')
    s.append(f'<line x1="{cs[0]}" y1="{cs[1]-41}" x2="{cr[0]}" y2="{cr[1]-105}" class="chain"/>')
    s.append(f'<path d="M{cs[0]+20} {cs[1]+38} L{cs[0]+30} {cs[1]+100} L{cs[0]+55} {cs[1]+160} L{cr[0]} {cr[1]+105}" class="chain"/>')
    s.append(f'<circle cx="{cs[0]+28}" cy="{cs[1]+95}" r="10" class="pulley"/><circle cx="{cs[0]+55}" cy="{cs[1]+160}" r="10" class="pulley"/><path d="M{cs[0]+10} {cs[1]+60} L{cs[0]+55} {cs[1]+160}" class="cage"/>')
    s.append(f'<path d="M{cr[0]-60} {cr[1]-110} l40 -8 l6 26 l-40 8 z" class="caliper"/>')
    s.append(f'<line x1="{cr[0]}" y1="{cr[1]}" x2="{cr[0]+70}" y2="{cr[1]+120}" class="crank"/>')
    s.append(_label(R, cr[0]+90, cr[1]-30, 730, 60, "Звёзды (шатуны)", P("chainring")))
    s.append(_label(R, cr[0]+50, cr[1]+90, 730, 330, "Шатун", P("crankset")))
    s.append(_label(R, cr[0], cr[1], 730, 230, "Каретка (вал)", P("bb")))
    s.append(_label(R, cr[0]-40, cr[1]-108, 520, 25, "Передний переключатель", P("front-derailleur"), "end"))
    s.append(_label(R, 400, 98, 330, 62, "Цепь — верхняя (рабочая) ветвь", P("chain"), "end"))
    s.append(_label(R, cs[0]-50, cs[1]-20, 60, 60, "Кассета", P("cassette"), "end"))
    s.append(_label(R, cs[0], cs[1], 60, 170, "Барабан втулки", P("freehub"), "end"))
    s.append(_label(R, cs[0]+28, cs[1]+95, 60, 260, "Верхний ролик", P("rear-derailleur"), "end"))
    s.append(_label(R, cs[0]+55, cs[1]+160, 60, 340, "Натяжной ролик", P("rear-derailleur"), "end"))
    s.append(f'<text x="410" y="372" class="dl" text-anchor="middle">Нижняя ветвь цепи (ненагруженная) проходит через ролики переключателя</text>')
    s.append('</svg>')
    return "".join(s)

def wheel(R):
    P = lambda p: f"parts/{p}/"
    s = ['<svg viewBox="100 10 760 410" class="diagram" role="img" aria-label="Разрез колеса: обод, покрышка, камера">']
    cx = 300
    s.append(f'<path d="M{cx-150} 120 C{cx-170} 20 {cx+170} 20 {cx+150} 120" class="tyreX"/>')
    s.append(f'<path d="M{cx-150} 120 L{cx-150} 200 L{cx-110} 200 M{cx+150} 120 L{cx+150} 200 L{cx+110} 200" class="tyreX"/>')
    s.append(f'<circle cx="{cx}" cy="138" r="80" class="tubeX"/>')
    s.append(f'<path d="M{cx-160} 190 L{cx-160} 260 Q{cx} 330 {cx+160} 260 L{cx+160} 190 L{cx+140} 190 L{cx+140} 230 Q{cx} 240 {cx-140} 230 L{cx-140} 190 Z" class="rimX"/>')
    s.append(f'<path d="M{cx-120} 226 Q{cx} 236 {cx+120} 226" class="tape"/>')
    s.append(f'<rect x="{cx-10}" y="240" width="20" height="60" class="nipple"/><line x1="{cx}" y1="300" x2="{cx}" y2="410" class="spokeX"/>')
    s.append(f'<rect x="{cx+60}" y="200" width="12" height="150" class="valveX"/>')
    s.append(_label(R, cx+120, 40, 560, 40, "Покрышка (протектор, корд)", P("tyre")))
    s.append(_label(R, cx+148, 170, 560, 110, "Борт покрышки", P("tyre")))
    s.append(_label(R, cx+70, 120, 560, 160, "Камера", P("tube")))
    s.append(_label(R, cx+110, 228, 560, 210, "Ободная лента", P("rim")))
    s.append(_label(R, cx+155, 250, 560, 260, "Обод (полки и колодец)", P("rim")))
    s.append(_label(R, cx+72, 330, 560, 320, "Ниппель (вентиль)", P("valve")))
    s.append(_label(R, cx+8, 285, 560, 365, "Ниппель спицы", P("spokes")))
    s.append(_label(R, cx, 390, 560, 405, "Спица → к втулке", P("spokes")))
    s.append('</svg>')
    return "".join(s)

def hub(R):
    P = lambda p: f"parts/{p}/"
    s = ['<svg viewBox="-90 20 970 345" class="diagram" role="img" aria-label="Разрез насыпной втулки">']
    s.append('<rect x="60" y="170" width="700" height="20" class="axle"/>')
    s.append('<path d="M220 120 L220 100 L250 100 L260 140 L560 140 L570 100 L600 100 L600 120 L590 150 L230 150 Z" class="shell"/>')
    s.append('<path d="M220 240 L220 260 L250 260 L260 220 L560 220 L570 260 L600 260 L600 240 L590 210 L230 210 Z" class="shell"/>')
    for x in (232, 588):
        for y in (158, 202): s.append(f'<circle cx="{x}" cy="{y}" r="9" class="ball"/>')
    s.append('<path d="M180 160 L210 160 L245 170 L245 190 L210 200 L180 200 Z" class="cone"/><path d="M640 160 L610 160 L575 170 L575 190 L610 200 L640 200 Z" class="cone"/>')
    s.append('<rect x="160" y="158" width="16" height="44" class="nut"/><rect x="644" y="158" width="16" height="44" class="nut"/>')
    for x in (232, 588):
        s.append(f'<circle cx="{x}" cy="106" r="5" class="hole"/><circle cx="{x}" cy="254" r="5" class="hole"/>')
    s.append(_label(R, 400, 180, 400, 330, "Ось", P("hub"), "middle"))
    s.append(_label(R, 400, 145, 400, 40, "Корпус втулки", P("hub"), "middle"))
    s.append(_label(R, 232, 106, 200, 62, "Фланец со спицевыми отверстиями", P("spokes"), "end"))
    s.append(_label(R, 588, 158, 700, 70, "Шарики подшипника", P("hub")))
    s.append(_label(R, 610, 195, 720, 260, "Конус", P("hub")))
    s.append(_label(R, 652, 200, 720, 300, "Контргайка", P("hub")))
    s.append(_label(R, 168, 200, 90, 300, "Контргайка", P("hub"), "end"))
    s.append(_label(R, 200, 195, 130, 260, "Конус", P("hub"), "end"))
    s.append(f'<text x="410" y="355" text-anchor="middle" class="dl">Шарики катятся между чашками корпуса и конусами; конус регулирует преднатяг — см. «Обслуживание насыпной втулки»</text>')
    s.append('</svg>')
    return "".join(s)

def fork(R):
    P = lambda p: f"parts/{p}/"
    s = ['<svg viewBox="-70 10 1200 430" class="diagram" role="img" aria-label="Схема вилки">']
    # Conventional suspension fork front view
    s.append('<rect x="190" y="20" width="24" height="120" class="tube2"/>')
    s.append('<path d="M110 140 L294 140 L284 170 L120 170 Z" class="crown"/>')
    s.append('<rect x="125" y="170" width="26" height="110" class="stanch"/><rect x="253" y="170" width="26" height="110" class="stanch"/>')
    s.append('<rect x="120" y="250" width="36" height="150" rx="6" class="lower"/><rect x="248" y="250" width="36" height="150" rx="6" class="lower"/>')
    s.append('<path d="M156 270 Q202 225 248 270" class="arch"/>')
    s.append('<circle cx="138" cy="398" r="9" class="hubc"/><circle cx="266" cy="398" r="9" class="hubc"/><line x1="138" y1="398" x2="266" y2="398" class="axle2"/>')
    s.append(_label(R, 202, 50, 320, 40, "Шток (steerer)", P("fork")))
    s.append(_label(R, 280, 155, 330, 120, "Корона", P("suspension-fork")))
    s.append(_label(R, 279, 210, 330, 200, "Стакан (верхняя нога)", P("suspension-fork")))
    s.append(_label(R, 248, 258, 330, 245, "Сальник / пыльник", P("suspension-fork")))
    s.append(_label(R, 202, 248, 330, 285, "Арка", P("suspension-fork")))
    s.append(_label(R, 284, 340, 330, 340, "Нижняя нога (lower)", P("suspension-fork")))
    s.append(_label(R, 266, 398, 330, 400, "Ось / дропауты", P("thru-axle")))
    s.append(f'<text x="202" y="432" class="dl" text-anchor="middle">Двуногая вилка (вид спереди)</text>')
    s.append(f'<text x="80" y="200" class="dl small" text-anchor="end">пружина</text><text x="80" y="215" class="dl small" text-anchor="end">в одной ноге,</text><text x="80" y="230" class="dl small" text-anchor="end">демпфер в другой</text>')
    # Lefty schematic
    s.append('<rect x="640" y="20" width="24" height="90" class="tube2"/>')
    s.append('<rect x="612" y="110" width="80" height="18" rx="4" class="crown"/><rect x="612" y="200" width="80" height="18" rx="4" class="crown"/>')
    s.append('<rect x="660" y="100" width="34" height="200" rx="5" class="stanch"/><rect x="664" y="270" width="26" height="110" rx="4" class="lower"/>')
    s.append('<circle cx="640" cy="390" r="44" class="rim ghost"/><line x1="640" y1="390" x2="690" y2="380" class="axle2"/><circle cx="640" cy="390" r="8" class="hubc"/>')
    s.append(_label(R, 692, 119, 760, 110, "Верхний зажим", P("fork")))
    s.append(_label(R, 692, 209, 760, 200, "Нижний зажим", P("fork")))
    s.append(_label(R, 694, 250, 760, 250, "Внешняя труба (нога)", f"guides/lefty-service/"))
    s.append(_label(R, 690, 320, 760, 310, "Телескоп (у классических — игольчатые подшипники)", f"guides/lefty-service/"))
    s.append(_label(R, 680, 382, 760, 380, "Консольная ось", P("hub")))
    s.append(f'<text x="660" y="432" class="dl" text-anchor="middle">Односторонняя вилка Lefty (упрощённо)</text>')
    s.append('</svg>')
    return "".join(s)

def planetary(R):
    P = lambda p: f"parts/{p}/"
    s = ['<svg viewBox="70 10 870 390" class="diagram" role="img" aria-label="Схема планетарной передачи">']
    cx, cy = 260, 200
    s.append(f'<circle cx="{cx}" cy="{cy}" r="170" class="ringgear"/><circle cx="{cx}" cy="{cy}" r="150" class="ringin"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="52" class="sun"/>')
    pts=[]
    for i in range(4):
        a = math.pi/4 + i*math.pi/2
        x, y = cx+101*math.cos(a), cy+101*math.sin(a); pts.append((x,y))
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="47" class="planet"/><circle cx="{x:.1f}" cy="{y:.1f}" r="7" class="hubc"/>')
    s.append('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x,y in pts) + '" class="carrier"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="12" class="hubc"/>')
    s.append(_label(R, cx+150, cy-50, 470, 60, "Коронная шестерня (эпицикл)", P("igh")))
    s.append(_label(R, pts[0][0], pts[0][1], 470, 330, "Сателлиты", P("igh")))
    s.append(_label(R, cx+30, cy-20, 470, 160, "Солнечная шестерня (на оси)", P("igh")))
    s.append(_label(R, (pts[0][0]+pts[3][0])/2, (pts[0][1]+pts[3][1])/2, 470, 250, "Водило", P("igh")))
    s.append(f'<text x="470" y="380" class="dl">Блокируя одно звено и ведя другое, втулка меняет передачу</text>')
    s.append('</svg>')
    return "".join(s)
DIAGRAMS = {"anatomy": ("Схема велосипеда", anatomy), "geometry": ("Геометрия рамы", geometry), "drivetrain": ("Трансмиссия", drivetrain),
            "wheel": ("Колесо в разрезе", wheel), "hub": ("Втулка в разрезе", hub), "fork": ("Вилки: обычная и Lefty", fork), "planetary": ("Планетарная передача", planetary)}

def lacing(R):
    s = ['<svg viewBox="0 0 960 380" class="diagram" role="img" aria-label="Схемы спицовки: радиальная, в два креста, в три креста">']
    panels = [(0, "Радиальная (0 крестов)"), (2, "В два креста"), (3, "В три креста")]
    n = 16  # отверстий на одном фланце (колесо на 32 спицы)
    for pi, (k, name) in enumerate(panels):
        cx, cy, Rr, rh = 160 + pi * 320, 180, 140, 34
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{Rr}" class="rim"/><circle cx="{cx}" cy="{cy}" r="{rh}" class="ring"/>')
        for j in range(n):
            a = 2 * math.pi * j / n
            hx, hy = cx + rh * math.cos(a), cy + rh * math.sin(a)
            d = 1 if j % 2 == 0 else -1
            b = a + d * k * 2 * math.pi / n
            rx, ry = cx + Rr * math.cos(b), cy + Rr * math.sin(b)
            cls = "spk1" if d == 1 else "spk2"
            s.append(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{rx:.1f}" y2="{ry:.1f}" class="{cls}"/>')
            s.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="2.5" class="hubc"/>')
        s.append(f'<text x="{cx}" y="350" text-anchor="middle" class="dl">{name}</text>')
    s.append('<text x="480" y="374" text-anchor="middle" class="dl small">Показан один фланец колеса на 32 спицы (16 спиц). Зелёные — ведущие, оранжевые — ведомые спицы.</text></svg>')
    return "".join(s)
DIAGRAMS["lacing"] = ("Схемы спицовки колеса", lacing)
