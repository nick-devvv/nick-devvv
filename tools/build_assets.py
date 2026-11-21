#!/usr/bin/env python3
"""Builds every image in assets/ for the profile README.

    python3 tools/build_assets.py

Edit the data below (projects, awards) or the drawings, re-run, and commit the new files in assets/.
"""
import random
from pathlib import Path

from pixel import (CREAM, CREAM_D, FELT, FELT_D, FELT_DOT, FELT_L, GOLD, GOLD_D, GOLD_DD, GOLD_L, MUTED, PANEL,
                   PANEL_L, RED, RED_D, ROOM, SMALL_SUITS, WINE, WOOD, WOOD_D, WOOD_L, BLACK, card, card_pal, chip_face,
                   chip_stack, ellipse, frame, path, runs, sprite, svg, text, text_bands, text_clip, text_width)

OUT = Path(__file__).resolve().parents[1] / 'assets'
NAME_BANDS = [(0, 1, GOLD_L), (2, 4, GOLD), (5, 6, GOLD_D)]
CHIP_COLORS = {'red': (RED, RED_D), 'blue': ('#2F6FE0', '#1B4396'), 'black': ('#2B2B33', '#121216'),
               'green': ('#1F9D55', '#126235'), 'gold': (GOLD, GOLD_D), 'silver': ('#C9CED6', '#7D8592'),
               'bronze': ('#D08A4E', '#8A5428'), 'orange': ('#FF6A1F', '#B4440E')}


def chip(x, y, u, color, cls='spin', centre=None):
    base, dark = CHIP_COLORS[color]
    pal = {'a': base, 'w': CREAM, 'd': dark, 'b': base}
    g = sprite(chip_face(11), pal, x, y, u)
    if centre:
        g += text(centre, x + 5.5 * u, y + 2 * u, u, CREAM, anchor='middle')
    return f'<g class="{cls}">{g}</g>' if cls else g


def suit_stars(n, w, h, avoid, seed, u=4, colors=None):
    """Tiny suit symbols scattered like stars, twinkling."""
    rnd = random.Random(seed)
    out, tries = [], 0
    colors = colors or [(CREAM, '.55'), (RED, '.8'), (GOLD, '.6')]
    while len(out) < n and tries < 2000:
        tries += 1
        x, y = rnd.randrange(16, w - 40, 4), rnd.randrange(12, h - 24, 4)
        if any(ax <= x <= bx and ay <= y <= by for ax, ay, bx, by in avoid):
            continue
        s = rnd.choice('SHDC')
        col, op = colors[0] if s in 'SC' else colors[rnd.randrange(1, len(colors))]
        out.append(f'<g class="tw st{len(out) % 4}" opacity="{op}">{path(runs(cells(SMALL_SUITS[s]), u, x, y), col)}</g>')
    return ''.join(out)


def cells(rows):
    return {(i, j) for j, r in enumerate(rows) for i, c in enumerate(r) if c == '#'}


# ===================================================================== hero
def hero():
    W, H = 1600, 520
    b = [f'<rect width="{W}" height="{H}" fill="{ROOM}"/>']
    # spotlight from above
    spot = ''.join(f'M{800 - (60 + y * 0.9) // 4 * 4} {y}h{2 * ((60 + y * 0.9) // 4 * 4)}v8h-{2 * ((60 + y * 0.9) // 4 * 4)}z'
                   for y in range(0, 300, 8))
    b.append(f'<path class="glow" fill="{CREAM}" fill-opacity=".06" d="{spot}"/>')
    b.append(suit_stars(34, W, 250, [(380, 20, 1220, 250), (90, 180, 720, 246), (1010, 180, 1400, 246)], 7))
    # name + subtitle
    name = 'NICK DEV'
    sc = 16
    nx, ny = W / 2, 40
    b.append(path(text_clip(name, nx + 8, ny + 8, sc, 'middle'), WINE))
    b.append(text_bands(name, nx, ny, sc, NAME_BANDS, 'middle'))
    b.append(f'<clipPath id="nm"><path d="{text_clip(name, nx, ny, sc, "middle")}"/></clipPath>'
             f'<g clip-path="url(#nm)"><rect class="shine" x="0" y="0" width="70" height="{H}" fill="#fff" opacity=".55"/></g>')
    b.append(text('ECON + DATA SCIENCE', 400, 196, 5, GOLD, 'middle'))
    b.append(text('UC BERKELEY', 1200, 196, 5, GOLD, 'middle'))
    b.append(path(runs(cells(SMALL_SUITS['S']), 5, 800 - 12.5, 197), CREAM))
    # table: rail, gold trim, felt
    cy, y0 = 700, 252
    b.append(path(ellipse(800, cy, 900, cy - y0, y0, H), WOOD_D))
    b.append(path(ellipse(800, cy, 884, cy - y0 - 8, y0 + 8, H), WOOD))
    b.append(path(ellipse(800, cy, 868, cy - y0 - 20, y0 + 20, H), WOOD_L))
    b.append(path(ellipse(800, cy, 852, cy - y0 - 28, y0 + 28, H), WOOD))
    b.append(path(ellipse(800, cy, 836, cy - y0 - 40, y0 + 40, H), GOLD_D))
    b.append(path(ellipse(800, cy, 828, cy - y0 - 44, y0 + 44, H), FELT_D))
    b.append(path(ellipse(800, cy, 812, cy - y0 - 52, y0 + 52, H), FELT))
    b.append(f'<path class="glow" fill="{FELT_L}" fill-opacity=".7" d="{ellipse(800, 640, 520, 300, 300, H)}"/>')
    dots = {(x, y) for y in range(0, 56) for x in range(0, 400) if (x + y * 3) % 9 == 0}
    b.append(f'<clipPath id="felt"><path d="{ellipse(800, cy, 812, cy - y0 - 52, y0 + 52, H)}"/></clipPath>'
             f'<g clip-path="url(#felt)" opacity=".5">{path(runs(dots, 4, 0, 296), FELT_DOT)}</g>')
    # dealer button
    b.append(f'<g class="bob2">{sprite(chip_face(9), {"a": CREAM, "w": CREAM_D, "d": CREAM_D, "b": CREAM}, 1108, 318, 4)}'
             f'{text("D", 1126, 330, 2, BLACK, "middle")}</g>')
    # chip stacks
    stacks = [(232, 440, ['red', 'black', 'red', 'blue'], 6), (300, 452, ['blue', 'blue', 'green'], 4),
              (1248, 448, ['black', 'red', 'gold'], 5), (1316, 436, ['green', 'red'], 7)]
    for i, (x, y, cols, n) in enumerate(stacks):
        b.append(f'<g class="{"bob" if i % 2 else "bob2"}">{chip_stack(n, [CHIP_COLORS[c] for c in cols], x, y)}</g>')
    b.append(chip(388, 330, 4, 'red'))
    b.append(f'<g style="animation-delay:-.9s">{chip(1180, 404, 4, "gold")}</g>')
    # a royal flush of spades, dealt, flipped, then swept away
    b.append(royal_flush(W))
    body = (f'<path fill="{GOLD_DD}" d="{frame(0, 0, W, H)}"/><clipPath id="fr"><path d="{frame(4, 4, W - 8, H - 8)}"/></clipPath>'
            f'<g clip-path="url(#fr)">{"".join(b)}</g>')
    return svg(W, H, body, 'NICK DEV. Econ + Data Science at UC Berkeley.', FLUSH_CSS)


FLUSH_CSS = ''


def royal_flush(W):
    global FLUSH_CSS
    u = 6
    cw, chh, gap = 15 * u, 23 * u, 22
    ranks = ['10', 'J', 'Q', 'K', 'A']
    total = 5 * cw + 4 * gap
    x0, y = (W - total) // 2, 318
    T = 10.0
    css, out = [], []
    for i, r in enumerate(ranks):
        x = x0 + i * (cw + gap)
        dx, dy = 800 - (x + cw / 2), -60
        t_in = 0.2 + i * 0.3
        t_flip = 2.4 + i * 0.35
        pct = lambda t: f'{t / T * 100:.2f}%'
        css.append(f'.d{i}{{animation:d{i} {T}s cubic-bezier(.2,.8,.3,1) infinite}}'
                   f'@keyframes d{i}{{0%,{pct(t_in - 0.01)}{{opacity:0;transform:translate({dx:.0f}px,{dy}px)}}'
                   f'{pct(t_in + 0.6)},{pct(8.6)}{{opacity:1;transform:translate(0,0)}}'
                   f'{pct(9.4)},100%{{opacity:0;transform:translate(0,40px)}}}}')
        css.append(f'.b{i},.f{i}{{transform-box:fill-box;transform-origin:50% 50%}}'
                   f'.b{i}{{animation:b{i} {T}s linear infinite}}@keyframes b{i}{{0%,{pct(t_flip)}{{transform:scaleX(1)}}{pct(t_flip + 0.15)},100%{{transform:scaleX(0)}}}}'
                   f'.f{i}{{animation:f{i} {T}s linear infinite}}@keyframes f{i}{{0%,{pct(t_flip + 0.15)}{{transform:scaleX(0)}}{pct(t_flip + 0.3)},100%{{transform:scaleX(1)}}}}')
        back = sprite(card('A', 'S', back=True), card_pal('S'), x, y, u, cls=f'b{i}')
        face = sprite(card(r, 'S'), card_pal('S'), x, y, u, cls=f'f{i}')
        glow = f'<path class="hl" fill="{GOLD}" d="M{x - 4} {y - 4}h{cw + 8}v{chh + 8}h-{cw + 8}z"/>'
        out.append(f'<g class="d{i}">{glow}{back}{face}</g>')
    css.append(f'.hl{{opacity:0;animation:hl {T}s steps(1) infinite}}@keyframes hl{{0%,{4.4 / T * 100:.1f}%{{opacity:0}}'
               f'{4.5 / T * 100:.1f}%,{8.6 / T * 100:.1f}%{{opacity:.9}}{8.7 / T * 100:.1f}%,100%{{opacity:0}}}}')
    FLUSH_CSS = ''.join(css)
    return ''.join(out)



# ===================================================================== project tiles
TW, TH, SCENE_H = 800, 500, 336
JSON_DIR = Path(__file__).resolve().parent

CHECK = ['........##', '.......###', '##....###.', '###..###..', '.######...', '..####....', '...##.....']
CROSS = ['##....##', '###..###', '.######.', '..####..', '..####..', '.######.', '###..###', '##....##']
PIN = ['..#####..', '.#######.', '###...###', '###...###', '###...###', '.#######.', '..#####..', '...###...', '...###...', '....#....', '....#....']
REX = ['...........aaaaaaaa...', '..........abbbbbbbba..', '.........abbbbbbbbbba.', '.........abbbbbccabba.',
       '.........abbbbbcaabba.', '.........abbbbbbbbbba.', '.........abbbbbbaaaaa.', '.........abbbbbacaca..',
       '.........abbbbbaaaaa..', '..a......abbbbbba.....', '..aa....abbbbbbba.....', '..aba..abbbbbbbbaaccc.',
       '...abaabbbbbbbbbabacc.', '....abbbdddbbbbbaaacc.', '.....abbdddbbbba...cc.', '......abbdddbbba......',
       '.......abbaaabba......', '.......aba...aba......', '......aaba..aaba......', '......aaaa..aaaa......']


def outline(g, fill_keys, key='k'):
    H, W = len(g), len(g[0])
    filled = {(x, y) for y in range(H) for x in range(W) if g[y][x] in fill_keys}
    for y in range(H):
        for x in range(W):
            if g[y][x] == '.' and any((x + dx, y + dy) in filled for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                g[y][x] = key
    return g


def house():
    W, H = 18, 17
    g = [['.'] * W for _ in range(H)]
    for y in range(0, 7):
        for x in range(W):
            if abs(x - 8.5) <= y + 2.5:
                g[y][x] = 'r' if y < 6 else 'R'
    for y in range(7, H):
        for x in range(2, W - 2):
            g[y][x] = 'c'
    for y in range(10, H):
        for x in (7, 8, 9):
            g[y][x] = 'd'
    for y in (9, 10, 11):
        for x in (3, 4, 12, 13):
            g[y][x] = 'w'
    for y in range(1, 4):
        g[y][13] = 'r'
        g[y][14] = 'r'
    return outline(g, 'rRcdw')


def coat():
    W, H = 22, 23
    g = [['.'] * W for _ in range(H)]
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            body = 5 <= x <= 16 and y >= 2
            shoulder = 3 <= x <= 18 and 2 <= y <= 4
            sleeve = (2 <= x <= 4 or 17 <= x <= 19) and 3 <= y <= 15
            if body or shoulder or sleeve:
                g[y][x] = 'c'
            if sleeve and y >= 14:
                g[y][x] = 'C'
            if body and y == 12:
                g[y][x] = 'C'
            if y <= 3 and 8 <= x <= 13:
                g[y][x] = '.'
            if x in (10, 11) and y >= 4 and body:
                g[y][x] = 'z' if y % 2 else 'Z'
    return outline(g, 'cCzZ')


def ht_css(name, T, delay=0.0, rise=40):
    return (f'.{name}{{opacity:0;animation:{name} {T}s ease-out infinite;animation-delay:{delay}s}}'
            f'@keyframes {name}{{0%{{opacity:0;transform:translateY(0)}}10%{{opacity:1}}60%{{opacity:1;transform:translateY(-{rise}px)}}'
            f'75%,100%{{opacity:0;transform:translateY(-{rise + 10}px)}}}}')


def appear_css(name, T, t_on, t_off=None, frm='translateY(-24px)'):
    t_off = t_off or T * 0.92
    a, b, c = t_on / T * 100, (t_on + 0.35) / T * 100, t_off / T * 100
    return (f'.{name}{{animation:{name} {T}s cubic-bezier(.3,1.5,.6,1) infinite}}'
            f'@keyframes {name}{{0%,{a:.1f}%{{opacity:0;transform:{frm}}}{b:.1f}%,{c:.1f}%{{opacity:1;transform:none}}'
            f'{min(c + 4, 100):.1f}%,100%{{opacity:0;transform:none}}}}')


def scene_clawback():
    import json
    g = json.load(open(JSON_DIR / 'clawdia.json'))
    rows = [''.join('.' if c in (None, 's') else c for c in r) for r in g]
    pal = {'k': '#0A1124', 'o': '#FF6A1F', 'w': '#FFFAF2', 'x': '#B87512', 'y': '#FFE9A8', 'g': '#F7BE3E', 'd': '#DB9A22'}
    out = [f'<g class="bob">{sprite(rows, pal, 56, 92, 10)}</g>']
    css = [ht_css('ht', 3.0, 0.4, 36)]
    out.append(f'<g class="ht">{text("+$630", 166, 92, 5, GOLD, "middle")}</g>')
    for i, (x, y, cols, n) in enumerate([(520, 284, ['red', 'black'], 3), (600, 278, ['blue', 'green'], 4), (680, 288, ['gold', 'red'], 2)]):
        out.append(f'<g class="sl sl{i}">{chip_stack(n, [CHIP_COLORS[c] for c in cols], x, y, u=6)}</g>')
    css.append('.sl{animation:sl 3s cubic-bezier(.5,0,.75,0) infinite}.sl1{animation-delay:-1s}.sl2{animation-delay:-2s}'
               '@keyframes sl{0%{opacity:0;transform:translateX(40px)}15%{opacity:1}80%{opacity:1;transform:translateX(-250px)}90%,100%{opacity:0;transform:translateX(-270px)}}')
    return ''.join(out), ''.join(css)


def scene_boneify():
    pal = {'a': '#22170F', 'b': '#5B8C3E', 'c': '#FFFAF2', 'd': '#D9E3A5'}
    out = [f'<g class="bob">{sprite(REX, pal, 70, 126, 9)}</g>']
    px, py, pw, ph = 420, 98, 260, 222
    out.append(path(f'M{px + 8} {py + 8}h{pw}v{ph}h-{pw}z', '#08321F'))
    out.append(path(f'M{px} {py}h{pw - 32}v8h8v8h8v8h8v8h8v{ph - 32}h-{pw}z', CREAM))
    out.append(path(f'M{px + pw - 32} {py}h8v24h24v8h-32z', CREAM_D))
    css, T = [], 6.0
    lines = [180, 150, 196, 128, 170, 140]
    for i, w in enumerate(lines):
        y = py + 40 + i * 28
        out.append(path(f'M{px + 24} {y}h{w}v12h-{w}z', '#CFC3A6'))
        ok = i != 3
        mark = sprite(CHECK if ok else CROSS, {'#': '#1F9D55' if ok else RED}, px + pw - 52, y - 8, 4)
        out.append(f'<g class="mk{i}">{mark}</g>')
        css.append(appear_css(f'mk{i}', T, 0.5 + i * 0.7, frm='scale(1.6)').replace(f'.mk{i}{{', f'.mk{i}{{transform-box:fill-box;transform-origin:50% 50%;'))
    scan = f'M{px + 12} {py + 32}h{pw - 24}v26h-{pw - 24}z'
    out.append(f'<path class="scan" fill="#A8D672" fill-opacity=".28" d="{scan}"/>')
    steps = ''.join(f'{(0.5 + i * 0.7) / T * 100:.1f}%{{transform:translateY({i * 28}px)}}' for i in range(6))
    css.append(f'.scan{{animation:scan {T}s steps(1) infinite}}@keyframes scan{{0%{{transform:translateY(0)}}{steps}90%,100%{{opacity:0;transform:translateY(140px)}}}}')
    return ''.join(out), ''.join(css)


def scene_picky():
    rnd = random.Random(3)
    dots = []
    for gy in range(4, 80):
        for gx in range(2, 196):
            if (gx % 4 == 0 and gy % 4 == 0) or gy in (30, 31, 56, 57) or gx in (60, 61, 128, 129):
                if rnd.random() < 0.55:
                    dots.append((gx, gy))
    out = [f'<g opacity=".3">{path(runs(set(dots), 4, 0, 0), CREAM)}</g>']
    css, T = [], 3.6
    pins = [(180, 150, '#2F6FE0', 0.0), (360, 96, GOLD, 0.35), (560, 170, '#FF5C8A', 0.7)]
    for i, (x, y, col, d) in enumerate(pins):
        out.append(f'<g class="pin{i}">{sprite(PIN, {"#": col}, x, y, 6)}{path(f"M{x + 18} {y + 18}h18v18h-18z", CREAM)}</g>')
        css.append(appear_css(f'pin{i}', T, 0.2 + d, T * 0.9, 'translateY(-60px)'))
    for i in range(3):
        out.append(f'<g class="hh hh{i}">{path(runs(cells(SMALL_SUITS["H"]), 5, 592 + i * 28 - 28, 150), "#FF5C8A")}</g>')
    css.append(ht_css('hh', 2.4, 0, 60) + '.hh1{animation-delay:.8s}.hh2{animation-delay:1.6s}')
    return ''.join(out), ''.join(css)


def scene_claimos():
    pal = {'r': '#C8423A', 'R': '#8E2B25', 'c': CREAM, 'd': '#6B3E24', 'w': '#7FB7FF', 'k': '#122018'}
    out = [f'<g class="bob">{sprite(house(), pal, 70, 130, 9)}</g>']
    px, py = 336, 70
    out.append(path(f'M{px + 8} {py + 8}h200v236h-200z', '#08321F'))
    out.append(path(f'M{px} {py}h200v236h-200z', CREAM))
    for i, w in enumerate([140, 110, 150, 96, 128]):
        out.append(path(f'M{px + 24} {py + 30 + i * 26}h{w}v10h-{w}z', '#CFC3A6'))
    css, T = [], 4.0
    stamp = path(frame(px + 22, py + 168, 156, 52, 4), RED) + path(frame(px + 30, py + 176, 140, 36, 4), CREAM) + text('APPEAL WON', px + 100, py + 186, 2, RED, 'middle')
    out.append(f'<g class="stp">{stamp}</g>')
    css.append(appear_css('stp', T, 0.8, T * 0.9, 'scale(1.8)').replace('.stp{', '.stp{transform-box:fill-box;transform-origin:50% 50%;'))
    out.append(chip_stack(3, [CHIP_COLORS['gold']], 610, 290))
    for i in range(3):
        out.append(f'<g class="cn cn{i}">{chip(620 + i * 6, 60, 4, "gold", cls=None, centre="$")}</g>')
    css.append('.cn{opacity:0;animation:cn 2.4s cubic-bezier(.5,0,1,.6) infinite}.cn1{animation-delay:.8s}.cn2{animation-delay:1.6s}'
               '@keyframes cn{0%{opacity:0;transform:translateY(0)}10%{opacity:1}70%{opacity:1;transform:translateY(176px)}75%,100%{opacity:0;transform:translateY(176px)}}')
    return ''.join(out), ''.join(css)


def scene_deltadesk():
    out = [path(f'M0 0h{TW}v{SCENE_H}h-{TW}z', '#06140E')]
    gridl = ''.join(f'M0 {y}h{TW}v2h-{TW}z' for y in range(80, 300, 40)) + ''.join(f'M{x} 72h2v236h-2z' for x in range(0, TW, 80))
    out.append(path(gridl, '#0E2A1D'))
    rnd = random.Random(11)
    price, candles = 190.0, []
    for i in range(40):
        o = price
        c = o + rnd.uniform(-34, 36)
        hi, lo = max(o, c) + rnd.uniform(6, 20), min(o, c) - rnd.uniform(6, 20)
        price = min(max(c, 100), 280)
        candles.append((o, c, hi, lo))
    def candle_set(ox):
        g_up, g_dn = [], []
        for i, (o, c, hi, lo) in enumerate(candles):
            x = ox + i * 40 + 10
            top, bot = 372 - max(o, c), 372 - min(o, c)
            body = f'M{x} {top:.0f}h20v{max(bot - top, 4):.0f}h-20z'
            wick = f'M{x + 8} {372 - hi:.0f}h4v{hi - lo:.0f}h-4z'
            (g_up if c >= o else g_dn).append(wick + body)
        return path(''.join(g_up), '#2ECC71') + path(''.join(g_dn), '#E5484D')
    out.append(f'<g class="tape">{candle_set(0)}{candle_set(1600)}</g>')
    css = ['.tape{animation:tape 16s linear infinite}@keyframes tape{100%{transform:translateX(-1600px)}}']
    tick = ''
    x = 0
    for sym, up in [('SPY', 1), ('QQQ', 0), ('AAPL', 1), ('NVDA', 1), ('TSLA', 0), ('MSFT', 1), ('AMZN', 0), ('META', 1)] * 2:
        tick += text(sym, x, 302, 3, CREAM_D) + text('^' if up else 'v', x + text_width(sym, 3) + 10, 302, 3, '#2ECC71' if up else '#E5484D')
        x += text_width(sym, 3) + 64
    out.append(path(f'M0 292h{TW}v36h-{TW}z', '#0A1F15'))
    out.append(f'<g class="tick">{tick}</g>')
    css.append(f'.tick{{animation:tick 10s linear infinite}}@keyframes tick{{100%{{transform:translateX(-{x // 2}px)}}}}')
    return ''.join(out), ''.join(css)


def scene_secondlook():
    pal = {'c': '#C9A777', 'C': '#A2845A', 'z': '#5A4632', 'Z': '#D9C39C', 'k': '#1E140C'}
    out = [f'<g class="bob">{sprite(coat(), pal, 90, 70, 11)}</g>']
    ring = frame(186, 150, 76, 76, 8)
    out.append(f'<path class="blink" fill="none" stroke="#E5484D" stroke-width="6" d="{ring}"/>')
    css, T = [], 4.5
    for i, (label, col) in enumerate([('REPAIR', '#E5484D'), ('TRADE IN', GOLD), ('BUY NEW', CREAM_D)]):
        y = 92 + i * 72
        tag = path(frame(440, y, 250, 52, 4), col) + path(f'M456 {y + 22}h8v8h-8z', '#0F5A3A') + text(label, 484, y + 15, 3, '#0B1511')
        out.append(f'<g class="tg{i}">{tag}</g>')
        css.append(appear_css(f'tg{i}', T, 0.3 + i * 0.45, T * 0.9, 'translateX(40px)'))
    out.append(f'<g class="tgk">{sprite(CHECK, {"#": "#2ECC71"}, 706, 100, 4)}</g>')
    css.append(appear_css('tgk', T, 2.0, T * 0.9, 'scale(1.6)'))
    return ''.join(out), ''.join(css)


WRENCH = ['##...##', '##...##', '###.###', '.#####.', '..###..', '..###..', '..###..', '..###..',
          '..###..', '..###..', '..###..', '.#####.', '.#####.', '..###..']


def scene_plumb():
    """A copper pipe leaking coins. A wrench clamps each leak in turn and the money stops."""
    T, py = 6.0, 150
    cu_l, cu, cu_d, cu_k = '#F2AE7E', '#C8733F', '#8A4622', '#2A150A'
    out, css = [], []

    def pipe_seg(x, w, y0, y1):
        return (path(f'M{x} {y0 - 4}h{w}v{y1 - y0 + 8}h-{w}z', cu_k) + path(f'M{x} {y0}h{w}v{y1 - y0}h-{w}z', cu)
                + path(f'M{x} {y0 + 4}h{w}v8h-{w}z', cu_l) + path(f'M{x} {y1 - 12}h{w}v12h-{w}z', cu_d))
    out.append(pipe_seg(-8, TW + 16, py, py + 48))
    for fx in (140, 400, 600):
        out.append(pipe_seg(fx, 32, py - 12, py + 60))
        out.append(path(f'M{fx + 12} {py - 4}h8v8h-8z' + f'M{fx + 12} {py + 44}h8v8h-8z', cu_k))
    cracks = [(300, 1.6), (500, 3.0), (690, 4.4)]
    pct = lambda t: f'{min(max(t, 0), T) / T * 100:.2f}%'
    for i, (cx, p) in enumerate(cracks):
        out.append(path(f'M{cx - 12} {py + 28}h8v4h8v4h8v4h-8v4h-8v4h-8z' + f'M{cx + 12} {py + 24}h4v8h-4z', cu_k))
        k = 0
        while k * 0.9 < p - 0.4:
            s = k * 0.9
            name = f'dp{i}{k}'
            out.append(f'<g class="{name}">{chip(cx - 16, py + 50, 3, "gold", cls=None, centre="$")}</g>')
            css.append(f'.{name}{{opacity:0;animation:{name} {T}s cubic-bezier(.5,0,1,.6) infinite}}'
                       f'@keyframes {name}{{0%,{pct(s - .01)}{{opacity:0;transform:translateY(0)}}{pct(s)}{{opacity:1;transform:translateY(0)}}'
                       f'{pct(s + .6)}{{opacity:1;transform:translateY(84px)}}{pct(s + .7)},100%{{opacity:0;transform:translateY(88px)}}}}')
            k += 1
        clamp = (path(f'M{cx - 20} {py - 12}h40v72h-40z', GOLD_DD) + path(f'M{cx - 16} {py - 8}h32v64h-32z', GOLD)
                 + path(f'M{cx - 16} {py - 8}h32v8h-32z', GOLD_L) + path(f'M{cx - 8} {py + 20}h16v8h-16z', GOLD_DD))
        out.append(f'<g class="cl{i}">{clamp}</g>')
        css.append(appear_css(f'cl{i}', T, p, 5.6, 'scale(1.5)').replace(f'.cl{i}{{', f'.cl{i}{{transform-box:fill-box;transform-origin:50% 50%;'))
        out.append(f'<g class="pl{i}">{text("+$", cx - 54, py - 46, 4, GOLD_L, "middle")}</g>')
        css.append(f'.pl{i}{{opacity:0;animation:pl{i} {T}s ease-out infinite}}'
                   f'@keyframes pl{i}{{0%,{pct(p)}{{opacity:0;transform:translateY(0)}}{pct(p + .15)}{{opacity:1}}'
                   f'{pct(p + 1.1)}{{opacity:1;transform:translateY(-18px)}}{pct(p + 1.4)},100%{{opacity:0;transform:translateY(-20px)}}}}')
    # puddle of coins under the pipe
    for i, (cx, _) in enumerate(cracks):
        out.append(chip_stack(2 - i % 2, [CHIP_COLORS['gold']], cx - 34, 318, u=5))
    # the wrench hops to each leak just before it gets clamped
    out.append(f'<g class="wr">{sprite(WRENCH, {"#": "#C9CED6"}, 0, py - 82, 5)}</g>')
    kf = [f'0%,{pct(.6)}{{opacity:0;transform:translateX({cracks[0][0] - 18}px)}}']
    for i, (cx, p) in enumerate(cracks):
        kf.append(f'{pct(p - .5)}{{opacity:1;transform:translateX({cx - 18}px) translateY(0)}}'
                  f'{pct(p - .15)}{{opacity:1;transform:translateX({cx - 18}px) translateY(14px)}}'
                  f'{pct(p + .1)}{{opacity:1;transform:translateX({cx - 18}px) translateY(0)}}')
    kf.append(f'{pct(5.0)},100%{{opacity:0;transform:translateX({cracks[-1][0] + 40}px)}}')
    css.append(f'.wr{{animation:wr {T}s ease-in-out infinite}}@keyframes wr{{{"".join(kf)}}}')
    return ''.join(out), ''.join(css)


def night_bot(color):
    """The Afterhours crew bot (the team's own design): a hovering gumdrop with a dark visor,
    one LED bar and an antenna. Keys: b body, d shade, h highlight, v visor, l LED, s antenna, t tip, k outline."""
    W, H = 18, 19
    g = [['.'] * W for _ in range(H)]
    spans = {4: (5, 10), 5: (3, 12), 6: (2, 13), 7: (1, 14)}
    for y in range(4, 17):
        a, b = spans.get(y, (0, 15) if y == 15 else (1, 14))
        for x in range(a, b + 1):
            g[y + 1][x + 1] = 'd' if (x >= b - 1 or y >= 15) else 'b'
    for x in range(3, 13):
        for y in (8, 9, 10):
            g[y + 1][x + 1] = 'v'
    for x in range(5, 11):
        g[10][x + 1] = 'l'
    for x, y in ((4, 6), (5, 6), (3, 7)):
        g[y + 1][x + 1] = 'h'
    for y in (2, 3):
        g[y + 1][10] = 's'
    for x in (10, 11):
        for y in (0, 1):
            g[y + 1][x] = 't'
    g = outline(g, 'bdhvlst')
    return [''.join(r) for r in g]


def scene_afterhours():
    out = [path(f'M0 {i * 56}h{TW}v56h-{TW}z', c) for i, c in
           enumerate(['#0B0820', '#0F0B29', '#130E33', '#17113D', '#1B1447', '#1F1750'])]
    css = []
    rnd = random.Random(5)
    stars = [(rnd.randrange(20, 760, 4), rnd.randrange(16, 180, 4)) for _ in range(26)]
    for i, (x, y) in enumerate(stars):
        out.append(f'<g class="tw st{i % 4}">{path(f"M{x} {y}h4v4h-4z", CREAM if i % 3 else "#39E8FF")}</g>')
    # moon
    moon = {(x, y) for y in range(13) for x in range(13) if (x - 6) ** 2 + (y - 6) ** 2 <= 40}
    bite = {(x, y) for y in range(13) for x in range(13) if (x - 9) ** 2 + (y - 4) ** 2 <= 22}
    out.append(path(runs(moon - bite, 4, 620, 30), '#FFF3C4'))
    # skyline with lit windows
    bldg = [(0, 214, 96), (100, 246, 70), (176, 200, 110), (292, 232, 84), (380, 190, 120), (506, 238, 90), (600, 206, 104), (708, 228, 100)]
    win_cols = ['#FFC93B', '#8F6BFF', '#FF3BD4', '#39E8FF']
    for bi, (x, y, w) in enumerate(bldg):
        out.append(path(f'M{x} {y}h{w}v{SCENE_H - y}h-{w}z', '#120D2C' if bi % 2 else '#160F36'))
        out.append(path(f'M{x} {y}h{w}v4h-{w}z', '#2A1F5E'))
        for wy in range(y + 16, SCENE_H - 12, 24):
            for wx in range(x + 12, x + w - 16, 20):
                if rnd.random() < 0.45:
                    col = rnd.choice(win_cols)
                    cls = f' class="tw st{rnd.randrange(4)}"' if rnd.random() < 0.35 else ''
                    out.append(f'<g{cls}>{path(f"M{wx} {wy}h8v10h-8z", col)}</g>')
    # neon OPEN sign
    out.append(path(frame(510, 262, 84, 34, 4), '#FF3BD4') + path(frame(514, 266, 76, 26, 4), '#1A0A2E'))
    out.append(f'<g class="blink">{text("OPEN", 552, 272, 2, "#FF3BD4", "middle")}</g>')
    # the crew: three bots hovering
    T = 2.4
    for i, (x, col) in enumerate([(40, '#FF3BD4'), (190, '#39E8FF'), (340, '#FFC93B')]):
        y = 92
        pal = {'b': col, 'd': shade(col, .62), 'h': '#FFFFFF', 'v': '#07060F', 'l': '#E9FBFF', 's': '#3A3F55', 't': col, 'k': '#05040C'}
        ring = ellipse(x + 72, y + 168, 52, 10, y + 158, y + 180)
        bot = sprite(night_bot(col), pal, x, y, 8)
        scan = f'<path class="scan{i}" fill="#FFFFFF" d="M{x + 48} {y + 80}h16v8h-16z"/>'
        out.append(f'<path class="glow" fill="{col}" fill-opacity=".35" d="{ring}"/>')
        out.append(f'<g class="{"bob" if i % 2 == 0 else "bob2"}">{bot}{scan}</g>')
        css.append(f'.scan{i}{{animation:scan{i} {T}s ease-in-out infinite;animation-delay:-{i * .5}s}}'
                   f'@keyframes scan{i}{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(32px)}}}}')
    # the owner says yes
    TT = 5.0
    b1 = path(frame(494, 112, 262, 48, 4), '#FF3BD4') + path(frame(498, 116, 254, 40, 4), '#1A0A2E') + text('2 FIXES READY', 625, 128, 3, '#FFE3F7', 'middle')
    b2 = path(frame(600, 176, 136, 48, 4), '#39FF9F') + text('YES 1', 668, 192, 3, '#062414', 'middle')
    out.append(f'<g class="ms1">{b1}</g><g class="ms2">{b2}</g>')
    css.append(appear_css('ms1', TT, 0.6, TT * 0.9, 'translateY(16px)') + appear_css('ms2', TT, 1.8, TT * 0.9, 'translateY(16px)'))
    return ''.join(out), ''.join(css)


def tile(name, tagline, accent, scene, badge=None, corner=('A', 'S'), cta=None):
    body, css = scene()
    W, H = TW, TH
    felt = ''.join(f'M0 {y}h{W}v{SCENE_H // 6}h-{W}z' for y in range(0, SCENE_H, SCENE_H // 6))
    bands = [path(f'M0 {i * 56}h{W}v56h-{W}z', c) for i, c in enumerate(['#0B4229', '#0C4A2E', '#0D5232', '#0E5836', '#0F5C38', '#0F5E3A'])]
    texture = {(x, y) for y in range(0, 84) for x in range(0, 200) if (x + y * 3) % 9 == 0}
    inner = (''.join(bands) + f'<g opacity=".45">{path(runs(texture, 4), FELT_DOT)}</g>' + body
             + path(f'M0 {SCENE_H}h{W}v{H - SCENE_H}h-{W}z', PANEL)
             + path(''.join(f'M{x} {SCENE_H}h8v4h-8z' for x in range(16, W - 16, 16)), GOLD_D)
             + path(text_clip(name, 40, 368, 8), shade(accent))
             + text(name, 36, 364, 8, accent)
             + text(tagline, 38, 440, 3, CREAM_D))
    if badge:
        label, color = badge
        bw = 72 + text_width(label, 3) + 18
        inner += (path(frame(20, 20, bw, 60, 4), '#000000" fill-opacity=".55') + chip(28, 28, 4, color)
                  + text(label, 84, 39, 3, CREAM))
    if cta:
        cw = text_width(cta, 3) + 74
        cx = W - 36 - cw
        inner += (path(frame(cx, 360, cw, 48, 4), '#4A0B13') + path(frame(cx + 2, 360, cw - 4, 42, 4), RED)
                  + f'<g class="nudge">{text(">", cx + 18, 374, 3, CREAM)}</g>' + text(cta, cx + 46, 374, 3, CREAM))
    r, s = corner
    inner += f'<g class="bob2">{sprite(card(r, s), card_pal(s), W - 45 - 24, 22, 3)}</g>'
    full = (f'<path fill="{shade(accent, .45)}" d="{frame(0, 0, W, H)}"/><clipPath id="t"><path d="{frame(4, 4, W - 8, H - 8)}"/></clipPath>'
            f'<g clip-path="url(#t)">{inner}</g>')
    return svg(W, H, full, f'{name}: {tagline.lower()}', css)


def shade(hexcol, k=.5):
    h = hexcol.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return '#%02X%02X%02X' % (int(r * k), int(g * k), int(b * k))


PROJECTS = [
    # slug, name, tagline, accent, scene, badge, corner card, tag (README order, 2 per row; corners run A down to 7)
    ('plumb', 'PLUMB', 'AGENTS FIND THE MONEY A SHOP IS LOSING', '#F2AE7E', scene_plumb, ('1ST PLACE', 'gold'), ('A', 'S'), None),
    ('afterhours', 'AFTERHOURS', 'A NIGHT CREW OF BOTS FOR SMALL SHOPS', '#FF3BD4', scene_afterhours, ('1ST BEST DESIGN * TOP 4', 'gold'), ('K', 'H'), 'PLAY'),
    ('boneify', 'BONEIFY', 'CHECKS AI ANSWERS AGAINST THE SOURCE', '#A8D672', scene_boneify, ('1ST ADOBE TRACK * 2ND OVERALL', 'gold'), ('Q', 'D'), 'PLAY'),
    ('picky', 'PICKY', 'EVERYONE AGREES ON FOOD', '#FF5C8A', scene_picky, ('2ND PLACE', 'silver'), ('J', 'C'), 'PLAY'),
    ('claimos', 'CLAIM OS', 'AGENTS APPEAL YOUR PROPERTY TAXES', '#4FD1C5', scene_claimos, ('4TH PLACE', 'bronze'), ('10', 'S'), 'PLAY'),
    ('clawback', 'CLAWBACK', 'AGENTS CLAW BACK YOUR SLA CREDITS', '#FF6A1F', scene_clawback, None, ('9', 'H'), 'PLAY'),
    ('deltadesk', 'DELTADESK', 'QUANT PAPER-TRADING DESK', '#4EA8FF', scene_deltadesk, None, ('8', 'D'), 'CODE'),
    ('secondlook', 'SECOND LOOK', 'REPAIR OR TRADE IN, NOT BUY NEW', '#E5484D', scene_secondlook, None, ('7', 'C'), 'PLAY'),
]



# ===================================================================== buttons and awards
def btn_all():
    W, H = 560, 112
    b = [path(frame(0, 0, W, H), GOLD_DD), path(frame(4, 4, W - 8, H - 12), GOLD), path(f'M12 {H - 22}h{W - 24}v8h-{W - 24}z', GOLD_D)]
    label = 'ALL PROJECTS'
    tw = text_width(label, 6)
    x = (W - tw) / 2 - 22
    b.append(text(label, x, 31, 6, '#2A1A06'))
    b.append(f'<g class="nudge">{text(">", x + tw + 24, 31, 6, "#2A1A06")}</g>')
    b.append(f'<clipPath id="bt"><path d="{frame(4, 4, W - 8, H - 12)}"/></clipPath>'
             f'<g clip-path="url(#bt)"><rect class="shine" x="0" y="0" width="60" height="{H}" fill="#fff" opacity=".35"/></g>')
    return svg(W, H, ''.join(b), 'All projects')


MEDAL = {'gold': [(0, 1, GOLD_L), (2, 4, GOLD), (5, 6, GOLD_D)],
         'silver': [(0, 1, '#F4F6FA'), (2, 4, '#C9CED6'), (5, 6, '#8F97A3')],
         'bronze': [(0, 1, '#F6C9A0'), (2, 4, '#D08A4E'), (5, 6, '#9A5E2E')]}


def award(place, title, event, project, accent, metal):
    W, H = 800, 240
    b = [path(frame(0, 0, W, H), shade(MEDAL[metal][2][2], .8)), f'<clipPath id="a"><path d="{frame(4, 4, W - 8, H - 8)}"/></clipPath>']
    inner = [path(f'M0 0h{W}v{H}h-{W}z', PANEL)]
    inner.append(path(ellipse(120, 120, 120, 120, 0, H), '#0E2A1D'))
    inner.append(suit_stars(9, W, H, [(0, 0, 250, H), (230, 30, 790, 200)], len(title), u=3))
    inner.append(f'<g class="spin">{sprite(chip_face(11), {"a": CHIP_COLORS[metal][0], "w": CREAM, "d": CHIP_COLORS[metal][1], "b": CHIP_COLORS[metal][0]}, 54, 54, 12)}'
                 f'{text(place, 120, 92, 8, CREAM, "middle")}</g>')
    inner.append(path(text_clip(title, 264, 52, 7), '#000') + text_bands(title, 260, 48, 7, MEDAL[metal]))
    lines = [event] if isinstance(event, str) else list(event)
    y0 = 124 if len(lines) == 1 else 112
    for k, line in enumerate(lines):
        inner.append(text(line, 262, y0 + k * 30, 3, CREAM_D))
    inner.append(text(project, 262, y0 + 30 * len(lines) + 10, 4, accent))
    b.append(f'<g clip-path="url(#a)">{"".join(inner)}</g>')
    return svg(W, H, ''.join(b), f'{title.title()}, {", ".join(lines).title()}, for {project.title()}')


AWARDS = [
    # file, place number, title, event (one line, or a list of two), project, accent, metal
    ('award-plumb', '1', '1ST PLACE', 'CLAWMAX.AI BUILD NIGHT * SF', 'PLUMB', '#F2AE7E', 'gold'),
    ('award-afterhours', '1', '1ST PLACE', ['BEST DESIGN * TOP 4 FINALIST', 'GROK BOT HACKATHON'], 'AFTERHOURS', '#FF3BD4', 'gold'),
    ('award-boneify-adobe', '1', '1ST PLACE', 'ADOBE TRACK * DREXATHON 2026', 'BONEIFY', '#A8D672', 'gold'),
    ('award-boneify-overall', '2', '2ND PLACE', 'OVERALL * DREXATHON 2026', 'BONEIFY', '#A8D672', 'silver'),
    ('award-picky', '2', '2ND PLACE', 'HACK WITH CLAUDE * UC BERKELEY', 'PICKY', '#FF5C8A', 'silver'),
    ('award-claimos', '4', '4TH PLACE', 'YC x NAIVE HACKATHON * SF', 'CLAIM OS', '#4FD1C5', 'bronze'),
]



def btn_credit():
    """Small credit button: inspired by Smaran, my co-founder."""
    W, H = 640, 112
    b = [path(frame(0, 0, W, H), GOLD_DD), path(frame(4, 4, W - 8, H - 12), PANEL_L), path(f'M12 {H - 22}h{W - 24}v8h-{W - 24}z', PANEL)]
    b.append(f'<g class="bob">{sprite(card("A", "H"), card_pal("H"), 30, 16, 3)}</g>')
    b.append(text('INSPIRED BY SMARAN', 100, 24, 4, GOLD))
    b.append(text('MY CO-FOUNDER', 100, 62, 3, CREAM_D))
    b.append(f'<g class="nudge">{text(">", W - 60, 38, 4, GOLD)}</g>')
    b.append(f'<clipPath id="bt"><path d="{frame(4, 4, W - 8, H - 12)}"/></clipPath>'
             f'<g clip-path="url(#bt)"><rect class="shine" x="0" y="0" width="50" height="{H}" fill="#fff" opacity=".12"/></g>')
    return svg(W, H, ''.join(b), 'Inspired by Smaran, my co-founder')

if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    (OUT / 'hero.svg').write_text(hero())
    for slug, name, tagline, accent, scene, badge, corner, cta in PROJECTS:
        (OUT / f'tile-{slug}.svg').write_text(tile(name, tagline, accent, scene, badge, corner, cta))
    (OUT / 'btn-all.svg').write_text(btn_all())
    (OUT / 'btn-smaran.svg').write_text(btn_credit())
    for f, *a in AWARDS:
        (OUT / f'{f}.svg').write_text(award(*a))
    for f in sorted(OUT.glob('*.svg')):
        print(f'{f.name:28s} {f.stat().st_size // 1024:4d} KB')
