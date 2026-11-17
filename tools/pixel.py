"""Pixel-art SVG helpers for the profile images: a 5x7 font, sprites, cards, chips and frames.

Everything is drawn as merged runs of square cells, so the SVGs stay small and crisp at any size.
"""
import math

# ---------- palette ----------
ROOM = '#07100B'
PANEL = '#0B1511'
PANEL_L = '#12201A'
FELT = '#0F5A3A'
FELT_L = '#167349'
FELT_D = '#0B4229'
FELT_DOT = '#13663F'
WOOD_D = '#2A170E'
WOOD = '#5A331E'
WOOD_L = '#7E4B2C'
GOLD_L = '#FFE7A3'
GOLD = '#F2C14E'
GOLD_D = '#C98B22'
GOLD_DD = '#6E4410'
CREAM = '#F6F0E1'
CREAM_D = '#D9CEB4'
MUTED = '#9C9584'
RED = '#D7263D'
RED_D = '#8E1726'
BLACK = '#17171C'
WINE = '#3B0D15'

# ---------- shared animation css ----------
CSS = (
    '.tw{animation:tw 2.4s steps(1) infinite}@keyframes tw{0%,100%{opacity:1}40%{opacity:.2}70%{opacity:.7}}'
    '.st0{animation-delay:0s}.st1{animation-delay:-.6s}.st2{animation-delay:-1.2s}.st3{animation-delay:-1.8s}'
    '.bob{animation:bob 1.4s ease-in-out infinite}.bob2{animation:bob 1.4s ease-in-out infinite;animation-delay:-.7s}'
    '@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}'
    '.spin{transform-box:fill-box;transform-origin:50% 50%;animation:spin 1.8s ease-in-out infinite}'
    '@keyframes spin{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.08)}}'
    '.blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}'
    '.shine{animation:shine 4.5s linear infinite}@keyframes shine{0%{transform:skewX(-20deg) translateX(-500px)}45%,100%{transform:skewX(-20deg) translateX(2200px)}}'
    '.glow{animation:glow 6s ease-in-out infinite}@keyframes glow{0%,100%{opacity:.5}50%{opacity:1}}'
    '.nudge{animation:nudge 1s ease-in-out infinite}@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}'
)

# ---------- fonts ----------
F5 = {
    'A': ['.###.', '#...#', '#...#', '#####', '#...#', '#...#', '#...#'],
    'B': ['####.', '#...#', '#...#', '####.', '#...#', '#...#', '####.'],
    'C': ['.###.', '#...#', '#....', '#....', '#....', '#...#', '.###.'],
    'D': ['####.', '#...#', '#...#', '#...#', '#...#', '#...#', '####.'],
    'E': ['#####', '#....', '#....', '####.', '#....', '#....', '#####'],
    'F': ['#####', '#....', '#....', '####.', '#....', '#....', '#....'],
    'G': ['.###.', '#...#', '#....', '#.###', '#...#', '#...#', '.####'],
    'H': ['#...#', '#...#', '#...#', '#####', '#...#', '#...#', '#...#'],
    'I': ['#####', '..#..', '..#..', '..#..', '..#..', '..#..', '#####'],
    'J': ['..###', '...#.', '...#.', '...#.', '...#.', '#..#.', '.##..'],
    'K': ['#...#', '#..#.', '#.#..', '##...', '#.#..', '#..#.', '#...#'],
    'L': ['#....', '#....', '#....', '#....', '#....', '#....', '#####'],
    'M': ['#...#', '##.##', '#.#.#', '#.#.#', '#...#', '#...#', '#...#'],
    'N': ['#...#', '#...#', '##..#', '#.#.#', '#..##', '#...#', '#...#'],
    'O': ['.###.', '#...#', '#...#', '#...#', '#...#', '#...#', '.###.'],
    'P': ['####.', '#...#', '#...#', '####.', '#....', '#....', '#....'],
    'Q': ['.###.', '#...#', '#...#', '#...#', '#.#.#', '#..#.', '.##.#'],
    'R': ['####.', '#...#', '#...#', '####.', '#.#..', '#..#.', '#...#'],
    'S': ['.####', '#....', '#....', '.###.', '....#', '....#', '####.'],
    'T': ['#####', '..#..', '..#..', '..#..', '..#..', '..#..', '..#..'],
    'U': ['#...#', '#...#', '#...#', '#...#', '#...#', '#...#', '.###.'],
    'V': ['#...#', '#...#', '#...#', '#...#', '#...#', '.#.#.', '..#..'],
    'W': ['#...#', '#...#', '#...#', '#.#.#', '#.#.#', '#.#.#', '.#.#.'],
    'X': ['#...#', '#...#', '.#.#.', '..#..', '.#.#.', '#...#', '#...#'],
    'Y': ['#...#', '#...#', '.#.#.', '..#..', '..#..', '..#..', '..#..'],
    'Z': ['#####', '....#', '...#.', '..#..', '.#...', '#....', '#####'],
    '0': ['.###.', '#...#', '#..##', '#.#.#', '##..#', '#...#', '.###.'],
    '1': ['..#..', '.##..', '..#..', '..#..', '..#..', '..#..', '.###.'],
    '2': ['.###.', '#...#', '....#', '...#.', '..#..', '.#...', '#####'],
    '3': ['####.', '....#', '....#', '.###.', '....#', '....#', '####.'],
    '4': ['...#.', '..##.', '.#.#.', '#..#.', '#####', '...#.', '...#.'],
    '5': ['#####', '#....', '####.', '....#', '....#', '#...#', '.###.'],
    '6': ['.###.', '#....', '#....', '####.', '#...#', '#...#', '.###.'],
    '7': ['#####', '....#', '...#.', '..#..', '.#...', '.#...', '.#...'],
    '8': ['.###.', '#...#', '#...#', '.###.', '#...#', '#...#', '.###.'],
    '9': ['.###.', '#...#', '#...#', '.####', '....#', '....#', '.###.'],
    ' ': ['...', '...', '...', '...', '...', '...', '...'],
    '+': ['.....', '..#..', '..#..', '#####', '..#..', '..#..', '.....'],
    '-': ['.....', '.....', '.....', '#####', '.....', '.....', '.....'],
    '.': ['.', '.', '.', '.', '.', '.', '#'],
    ',': ['..', '..', '..', '..', '..', '.#', '#.'],
    '!': ['#', '#', '#', '#', '#', '.', '#'],
    '?': ['.###.', '#...#', '....#', '...#.', '..#..', '.....', '..#..'],
    '$': ['..#..', '.####', '#.#..', '.###.', '..#.#', '####.', '..#..'],
    '/': ['....#', '...#.', '...#.', '..#..', '.#...', '.#...', '#....'],
    ':': ['.', '#', '.', '.', '.', '#', '.'],
    "'": ['#', '#', '.', '.', '.', '.', '.'],
    '&': ['.##..', '#..#.', '#.#..', '.#...', '#.#.#', '#..#.', '.##.#'],
    'x': ['.....', '.....', '#...#', '.#.#.', '..#..', '.#.#.', '#...#'],
    '*': ['..', '..', '..', '##', '##', '..', '..'],
    '>': ['#....', '##...', '###..', '####.', '###..', '##...', '#....'],
    '^': ['.....', '..#..', '.###.', '#####', '.....', '.....', '.....'],
    'v': ['.....', '.....', '.....', '#####', '.###.', '..#..', '.....'],
}
# '*' is a centred dot (a "·" separator); 'x' is a times sign; '>' is a play triangle; '^' and 'v' are up/down ticks

F3 = {  # 3x5 card ranks
    'A': ['.#.', '#.#', '###', '#.#', '#.#'],
    'K': ['#.#', '#.#', '##.', '#.#', '#.#'],
    'Q': ['.##.', '#..#', '#..#', '#.#.', '.#.#'],
    'J': ['..#', '..#', '..#', '#.#', '.#.'],
    '1': ['.#', '##', '.#', '.#', '.#'],
    '0': ['###', '#.#', '#.#', '#.#', '###'],
    '9': ['###', '#.#', '###', '..#', '###'],
}

SUITS = {
    'S': ['....#....', '...###...', '..#####..', '.#######.', '#########', '#########', '.##.#.##.', '....#....', '...###...'],
    'H': ['.##...##.', '####.####', '#########', '#########', '.#######.', '..#####..', '...###...', '....#....', '.........'],
    'D': ['....#....', '...###...', '..#####..', '.#######.', '#########', '.#######.', '..#####..', '...###...', '....#....'],
    'C': ['...###...', '..#####..', '..#####..', '.##.#.##.', '#########', '#########', '.##.#.##.', '....#....', '...###...'],
}
SMALL_SUITS = {
    'S': ['..#..', '.###.', '#####', '#####', '..#..'],
    'H': ['.#.#.', '#####', '#####', '.###.', '..#..'],
    'D': ['..#..', '.###.', '#####', '.###.', '..#..'],
    'C': ['.###.', '.###.', '#####', '#####', '..#..'],
}


def glyph_cells(s, font=F5):
    cells, cx = set(), 0
    for ch in s:
        g = font.get(ch) or font.get(ch.upper()) or font[' ']
        for j, row in enumerate(g):
            for i, c in enumerate(row):
                if c == '#':
                    cells.add((cx + i, j))
        cx += len(g[0]) + 1
    return cells, max(cx - 1, 0)


def text_width(s, scale, font=F5):
    return glyph_cells(s, font)[1] * scale


# ---------- path building ----------
def runs(cells, u, ox=0, oy=0):
    """Merge cells (x, y) into horizontal runs and return an SVG path string."""
    rows = {}
    for x, y in cells:
        rows.setdefault(y, []).append(x)
    out = []
    for y in sorted(rows):
        xs = sorted(set(rows[y]))
        start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            w = (prev - start + 1) * u
            out.append(f'M{fmt(ox + start * u)} {fmt(oy + y * u)}h{fmt(w)}v{fmt(u)}h-{fmt(w)}z')
            if x is not None:
                start = prev = x
    return ''.join(out)


def fmt(v):
    v = round(v, 2)
    return str(int(v)) if v == int(v) else str(v)


def path(d, fill, extra=''):
    return f'<path fill="{fill}" d="{d}"{extra}/>' if d else ''


def text(s, x, y, scale, fill, anchor='start', font=F5, extra=''):
    cells, w = glyph_cells(s, font)
    if anchor == 'middle':
        x -= w * scale / 2
    elif anchor == 'end':
        x -= w * scale
    return path(runs(cells, scale, x, y), fill, extra)


def text_bands(s, x, y, scale, bands, anchor='start', font=F5):
    """Text whose rows are coloured in bands: bands = [(first_row, last_row, colour), ...]."""
    cells, w = glyph_cells(s, font)
    if anchor == 'middle':
        x -= w * scale / 2
    out = []
    for a, b, col in bands:
        out.append(path(runs({c for c in cells if a <= c[1] <= b}, scale, x, y), col))
    return ''.join(out)


def text_clip(s, x, y, scale, anchor='start', font=F5):
    cells, w = glyph_cells(s, font)
    if anchor == 'middle':
        x -= w * scale / 2
    return runs(cells, scale, x, y)


def sprite(rows, pal, x, y, u, cls=None, style=None):
    by = {}
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in pal and pal[ch]:
                by.setdefault(pal[ch], set()).add((i, j))
    inner = ''.join(path(runs(c, u, x, y), col) for col, c in by.items())
    attrs = (f' class="{cls}"' if cls else '') + (f' style="{style}"' if style else '')
    return f'<g{attrs}>{inner}</g>'


def grid(w, h, fill='.'):
    return [[fill] * w for _ in range(h)]


def stamp(g, rows, x, y, ch=None, flip=False):
    rows = [r[::-1] for r in rows[::-1]] if flip else rows
    for j, row in enumerate(rows):
        for i, c in enumerate(row):
            if c != '.' and 0 <= y + j < len(g) and 0 <= x + i < len(g[0]):
                g[y + j][x + i] = ch or c


def rows_of(g):
    return [''.join(r) for r in g]


# ---------- shapes ----------
def frame(x, y, w, h, s=8):
    """A rectangle with stepped pixel corners."""
    return (f'M{x + 2 * s} {y}h{w - 4 * s}v{s}h{s}v{s}h{s}v{h - 4 * s}h-{s}v{s}h-{s}v{s}h-{w - 4 * s}'
            f'v-{s}h-{s}v-{s}h-{s}v-{h - 4 * s}h{s}v-{s}h{s}z')


def ellipse(cx, cy, rx, ry, y0, y1, step=4):
    out = []
    for y in range(int(y0), int(y1), step):
        yy = y + step / 2 - cy
        if abs(yy) >= ry:
            continue
        hw = round(rx * math.sqrt(1 - (yy / ry) ** 2) / step) * step
        if hw > 0:
            out.append(f'M{fmt(cx - hw)} {y}h{fmt(2 * hw)}v{step}h-{fmt(2 * hw)}z')
    return ''.join(out)


def card(rank, suit, back=False):
    """A 15x23 playing card as rows of palette keys: o outline, c cream, r suit colour, b/B back reds."""
    W, H = 15, 23
    g = grid(W, H)
    for y in range(H):
        for x in range(W):
            if (x in (0, W - 1) and y in (0, 1, H - 2, H - 1)) or (y in (0, H - 1) and x in (0, 1, W - 2, W - 1)):
                continue
            edge = x in (0, W - 1) or y in (0, H - 1) or (x in (1, W - 2) and y in (1, H - 2))
            g[y][x] = 'o' if edge else 'c'
    if back:
        for y in range(2, H - 2):
            for x in range(2, W - 2):
                g[y][x] = 'B' if (x + y) % 4 == 0 or (x - y) % 4 == 0 else 'b'
        return rows_of(g)
    rk = glyph_rows(rank)
    stamp(g, rk, 2, 2, 'r')
    stamp(g, SUITS[suit], 3, 7, 'r')
    stamp(g, rk, W - 2 - len(rk[0]), H - 7, 'r', flip=True)
    return rows_of(g)


def glyph_rows(s):
    cells, w = glyph_cells(s, F3)
    out = []
    for j in range(5):
        out.append(''.join('#' if (i, j) in cells else '.' for i in range(w)))
    return out


def card_pal(suit):
    return {'o': '#B9AE95', 'c': CREAM, 'r': RED if suit in 'HD' else BLACK, 'b': '#B32032', 'B': '#7E1424'}


def chip_face(size=11):
    """A chip seen from the front: a ring with edge stripes. Keys: a base, w stripe, d inner ring, b centre."""
    g = grid(size, size)
    c = (size - 1) / 2
    R = size / 2 - 0.1
    for y in range(size):
        for x in range(size):
            r = math.hypot(x - c, y - c)
            if r > R:
                continue
            if r > R - 1.6:
                ang = (math.atan2(y - c, x - c) + math.pi) / (2 * math.pi)
                g[y][x] = 'w' if int(ang * 8) % 2 == 0 else 'a'
            elif r > R - 2.6:
                g[y][x] = 'd'
            else:
                g[y][x] = 'b'
    return rows_of(g)


def chip_stack(n, colors, x, y, u=4, w=13):
    """A side-view stack of n chips, bottom chip at y (top-left of its band). colors: list of (base, dark)."""
    out = []
    for k in range(n):
        base, dark = colors[k % len(colors)]
        cy = y - k * 3 * u
        band = set()
        dk = set()
        st = set()
        for i in range(w):
            band.add((i, 0))
            dk.add((i, 1))
            if i in (2, 3, 6, 9, 10):
                st.add((i, 0))
        out.append(path(runs(band - st, u, x, cy), base) + path(runs(st, u, x, cy), CREAM) + path(runs(dk, u, x, cy), dark))
    top_y = y - (n - 1) * 3 * u - 2 * u
    base, dark = colors[(n - 1) % len(colors)]
    top = {(i, 0) for i in range(1, w - 1)} | {(i, 1) for i in range(w)}
    inner = {(i, 1) for i in range(3, w - 3)} | {(i, 0) for i in range(4, w - 4)}
    out.append(path(runs(top - inner, u, x, top_y), base) + path(runs(inner, u, x, top_y), CREAM))
    return ''.join(out)


def svg(w, h, body, title, css=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges"><title>{title}</title><style>{CSS}{css}</style>{body}</svg>\n')
