#!/usr/bin/env python3
"""Vol.5 '두 번째 챔피언' 블라인드 이미지 생성 (Vol.4 인스타 '올해의 연사는?' 스타일).

사용법: python3 tools/make_blind_champion.py [Pretendard 폰트 폴더]
- 문구는 아래 TITLE / TAGS / BAR 를 고친 뒤 다시 실행
- 결과: assets/vol05/blind_champion.png (630px 폭 2배 해상도), assets/vol05/logo_blind.png
"""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "vol05"
FONT_DIR = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
LIME, BLACK, WHITE = (0x99, 0xF6, 0x37), (0, 0, 0), (255, 255, 255)

TITLE = "챔피언 라이브, 두 번째 주인공은?"
TAGS = [  # (문구, 중심 x, 중심 y) — 2배 해상도 좌표
    ("세계 무대의 챔피언", 900, 430),
    ("11.14(토) 13:30", 330, 600),
    ("단 한 번의 라이브", 920, 800),
    ("곧 공개됩니다", 360, 940),
]
BAR = "WCF 인스타그램을 팔로우하고 두 번째 챔피언을 가장 먼저 만나보세요!"


def font(weight, size):
    if FONT_DIR and (FONT_DIR / f"Pretendard-{weight}.otf").exists():
        return ImageFont.truetype(str(FONT_DIR / f"Pretendard-{weight}.otf"), size)
    return ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", size, index=1)


def silhouette(W, H, S=4):
    """사람 상반신 실루엣(머리·목·둥근 어깨·팔), 머리에 연두 물음표. 좌표는 820×900 기준."""
    k = W / 820 * S
    P = lambda *pts: [(x * k, y * k) for x, y in pts]
    im = Image.new("L", (W * S, H * S), 0)
    d = ImageDraw.Draw(im)
    d.ellipse(P((332, 62), (488, 255)), fill=255)                       # 머리
    d.polygon(P((372, 220), (448, 220), (458, 315), (362, 315)), fill=255)  # 목
    d.ellipse(P((170, 290), (650, 520)), fill=255)                       # 어깨 곡선
    d.polygon(P((172, 405), (648, 405), (676, 900), (144, 900)), fill=255)  # 몸통+팔
    for (x0, y0, x1, y1) in ((250, 520, 262, 900), (570, 520, 558, 900)):  # 팔과 몸통 사이 틈
        d.line(P((x0, y0), (x1, y1)), fill=0, width=int(9 * k))
    d.polygon(P((376, 300), (444, 300), (410, 372)), fill=0)             # 셔츠 깃(V)
    im = im.resize((W, H), Image.LANCZOS)
    return im, (410 * W // 820, 158 * W // 820, 80 * W // 820)


def main():
    W, H = 1260, 1220
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    f = font("ExtraBold", 68)
    tw = d.textlength(TITLE, font=f)
    d.text(((W - tw) / 2, 70), TITLE, font=f, fill=BLACK)

    mask, (hx, hy, hr) = silhouette(820, 900)
    ox, oy = (W - 820) // 2, 190
    img.paste(Image.new("RGB", mask.size, BLACK), (ox, oy), mask)
    q = font("ExtraBold", int(hr * 1.5))
    qb = d.textbbox((0, 0), "?", font=q)
    d.text((ox + hx - (qb[0] + qb[2]) / 2, oy + hy - (qb[1] + qb[3]) / 2), "?", font=q, fill=LIME)

    tf = font("SemiBold", 44)
    for text, cx, cy in TAGS:
        b = d.textbbox((0, 0), text, font=tf)
        tw, th = b[2] - b[0], b[3] - b[1]
        x0, y0 = cx - tw / 2 - 26, cy - th / 2 - 20
        d.rectangle((x0, y0, x0 + tw + 52, y0 + th + 40), fill=LIME, outline=BLACK, width=3)
        d.text((x0 + 26 - b[0], y0 + 20 - b[1]), text, font=tf, fill=BLACK)

    bf = font("Bold", 38)
    b = d.textbbox((0, 0), BAR, font=bf)
    bw, bh = b[2] - b[0], b[3] - b[1]
    x0, y0 = (W - bw) / 2 - 28, 1110
    d.rectangle((x0, y0, x0 + bw + 56, y0 + bh + 36), fill=BLACK, outline=LIME, width=3)
    d.text((x0 + 28 - b[0], y0 + 18 - b[1]), BAR, font=bf, fill=WHITE)
    img.save(OUT / "blind_champion.png", optimize=True)

    # 세션 시간표용 '?' 로고 타일 (다른 로고와 같은 360×180)
    t = Image.new("RGB", (360, 180), LIME)
    td = ImageDraw.Draw(t)
    lf = font("ExtraBold", 110)
    b = td.textbbox((0, 0), "?", font=lf)
    td.text(((360 - b[2] - b[0]) / 2, (180 - b[3] - b[1]) / 2), "?", font=lf, fill=BLACK)
    t.save(OUT / "logo_blind.png", optimize=True)
    print("saved", OUT / "blind_champion.png")


if __name__ == "__main__":
    main()
