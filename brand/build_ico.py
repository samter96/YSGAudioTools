# -*- coding: utf-8 -*-
"""파비콘 ICO 생성 — SVG 를 거치지 않고 **기하를 직접 래스터라이즈**한다.

왜 SVG→ICO 변환을 쓰지 않나
  · 이 PC 에 SVG 렌더러(cairosvg 등)가 없다. PIL 만 있다
  · 마크가 단순 폴리곤 3개라 직접 그리는 편이 오히려 정확하다 —
    변환기의 곡선 근사·힌팅을 거치지 않는다
  · build_brand.py 와 **같은 수식**을 쓰므로 SVG 와 ICO 가 어긋날 수 없다

안티에일리어싱: 목표 크기의 8배로 그린 뒤 LANCZOS 로 축소한다. 16px 같은
작은 칸에서 획 끝(폭 1.9/24)이 살아남으려면 이 정도 감독이 필요하다.
"""
import io
import math
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from PIL import Image, ImageDraw

OUT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(OUT), "assets")

# build_brand.py 와 동일한 확정 파라미터 — 한쪽만 고치면 SVG 와 어긋난다
CX = 12.0
REACH = 9.9            # 세 획 공통 길이 (대칭)
W0, W1 = 5.2, 1.2
SPREAD = 60.0

#  세로 중심 보정 — build_brand.py 의 같은 이름 계산과 **반드시 같은 식**이다.
#  아래 획만 곧게 내려가서 원점을 12 에 두면 잉크가 아래로 쏠린다. 식을 고칠 때는
#  두 파일을 함께 고쳐야 한다 (SVG 와 ICO 가 어긋나면 파비콘만 삐뚤어진다).
_INK_TOP = (12.0 - REACH * math.cos(math.radians(SPREAD))
            - (W1 / 2) * math.sin(math.radians(SPREAD)))
_INK_BOTTOM = 12.0 + REACH
CY = 12.0 - ((_INK_TOP + _INK_BOTTOM) / 2 - 12.0)
STROKES = [(90.0, REACH), (270.0 - SPREAD, REACH), (270.0 + SPREAD, REACH)]

CYAN = (52, 224, 232)
BLUE = (44, 107, 224)
INDIGO = (27, 42, 107)
AMBER = (255, 180, 84)
BG_TOP = (20, 28, 43)
BG_BOTTOM = (7, 10, 15)

SS = 8          # 초과표본 배율
SIZES = [16, 24, 32, 48, 64, 128, 256]


def unit(deg):
    r = math.radians(deg)
    return (math.cos(r), math.sin(r))


def wedge_points(deg, end, scale, w0=W0, w1=W1):
    """build_brand.stroke_path 와 같은 네 점 (좌우 대칭 평평 마감)"""
    d = unit(deg)
    p = (-d[1], d[0])
    a = (CX, CY)
    b = (CX + d[0] * end, CY + d[1] * end)
    a1 = (a[0] + p[0] * w0 / 2, a[1] + p[1] * w0 / 2)
    a2 = (a[0] - p[0] * w0 / 2, a[1] - p[1] * w0 / 2)
    b1 = (b[0] + p[0] * w1 / 2, b[1] + p[1] * w1 / 2)
    b2 = (b[0] - p[0] * w1 / 2, b[1] - p[1] * w1 / 2)
    return [tuple(v * scale for v in pt) for pt in (a1, b1, b2, a2)]


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def rounded_rect_mask(size, radius):
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1],
                                           radius=radius, fill=255)
    return mask


def gradient_wedge(canvas_size, deg, end, ramp):
    """획 하나를 그린다. 중심→끝 방향으로 색이 변해야 하므로, 방향에 수직인
    띠를 여러 장 겹쳐 근사한다 (PIL 에는 선형 그라디언트가 없다)."""
    layer = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    scale = canvas_size / 24.0
    pts = wedge_points(deg, end, scale)
    shape = Image.new("L", (canvas_size, canvas_size), 0)
    ImageDraw.Draw(shape).polygon(pts, fill=255)

    d = unit(deg)
    steps = 48
    grad = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    # 진행 방향으로 얇은 사각 띠를 이어 붙인다
    span = end * scale
    p = (-d[1], d[0])
    half = canvas_size            # 띠를 충분히 넓게
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        color = lerp(ramp[0], ramp[1], (t0 + t1) / 2)
        c0 = (CX * scale + d[0] * span * t0, CY * scale + d[1] * span * t0)
        c1 = (CX * scale + d[0] * span * t1 + d[0] * 2, CY * scale + d[1] * span * t1 + d[1] * 2)
        quad = [
            (c0[0] + p[0] * half, c0[1] + p[1] * half),
            (c1[0] + p[0] * half, c1[1] + p[1] * half),
            (c1[0] - p[0] * half, c1[1] - p[1] * half),
            (c0[0] - p[0] * half, c0[1] - p[1] * half),
        ]
        gd.polygon(quad, fill=color + (255,))
    layer.paste(grad, (0, 0), shape)
    return layer


def render(size):
    big = size * SS
    scale = big / 24.0

    # 배경 — 위에서 아래로 어두워지는 세로 그라디언트
    bg = Image.new("RGBA", (big, big))
    bd = ImageDraw.Draw(bg)
    for y in range(big):
        bd.line([(0, y), (big, y)], fill=lerp(BG_TOP, BG_BOTTOM, y / max(1, big - 1)) + (255,))
    bg.putalpha(rounded_rect_mask(big, int(big * 28 / 128)))

    # 중심 발광 — 방사형을 원 여러 개로 근사
    glow = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    rings = 26
    r_max = 7.4 * scale
    for i in range(rings, 0, -1):
        t = i / rings
        r = r_max * t
        alpha = int(150 * (1 - t) ** 1.7)
        gd.ellipse([CX * scale - r, CY * scale - r, CX * scale + r, CY * scale + r],
                   fill=CYAN + (alpha,))
    bg.alpha_composite(glow)

    ramps = [(CYAN, BLUE), (BLUE, INDIGO), (CYAN, BLUE)]
    for (deg, end), ramp in zip(STROKES, ramps):
        bg.alpha_composite(gradient_wedge(big, deg, end, ramp))

    # 윤곽 — 끝이 어두워도 형태가 남게 (SVG 와 같은 이유)
    outline = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    od = ImageDraw.Draw(outline)
    for deg, end in STROKES:
        od.polygon(wedge_points(deg, end, scale),
                   outline=CYAN + (110,), width=max(1, int(scale * 0.20)))
    bg.alpha_composite(outline)

    # 중심 앰버 한 점
    dot = 0.72 * scale
    ImageDraw.Draw(bg).ellipse(
        [CX * scale - dot, CY * scale - dot, CX * scale + dot, CY * scale + dot],
        fill=AMBER + (255,))

    return bg.resize((size, size), Image.LANCZOS)


frames = [render(s) for s in SIZES]
ico = os.path.join(ASSETS, "favicon-ysg.ico")
frames[-1].save(ico, format="ICO",
                sizes=[(s, s) for s in SIZES])
png = os.path.join(ASSETS, "favicon-ysg.png")
frames[-1].save(png, format="PNG")

print("ICO 생성: %s (%d bytes) — %s" % (
    os.path.basename(ico), os.path.getsize(ico), " ".join(str(s) for s in SIZES)))
print("PNG 생성: %s (%d bytes)" % (os.path.basename(png), os.path.getsize(png)))

# 작은 칸에서 획이 살아남았는지 확인 — 16px 에서 시안 화소가 몇 개인지 센다
small = frames[0].convert("RGBA")
cyanish = sum(1 for px in small.getdata()
              if px[3] > 40 and px[2] > 90 and px[1] > 60)
print("16px 안에서 마크 화소 %d / %d (%.0f%%) — 형태가 남았는지 확인"
      % (cyanish, 16 * 16, cyanish / (16 * 16) * 100))
