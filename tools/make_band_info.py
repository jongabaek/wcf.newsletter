"""5호 띠(band_origin.png)·인포 바(info_origin.png) 원본에서 글자만 바꿔 새 띠·인포 바를 만든다. 인포 바는 630px 폭에 꽉 차게(원본 픽셀을 잘라 이어 붙임).

사용: python3 tools/make_band_info.py <출력 접두어> "<띠 문구>" "<프로그램명>" "<날짜>" "<장소>" ["<버튼 문구>"]
예:   python3 tools/make_band_info.py assets/vol06/sca "월커포에서 만나는 국제 표준 스페셜티 커피 커리큘럼" "SCA 교육" "11. 12(목) – 14(토)" "코엑스 컨퍼런스룸 317호"
필요: Pretendard SemiBold(띠, PRETENDARD_DIR 환경변수 또는 ../fonts/... ), Noto Sans CJK KR Bold/Regular(인포 바).
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = f"{R}/assets/vol05/"
PRE = os.environ.get("PRETENDARD_DIR", "/tmp/claude-0/-home-claude/b93c95e6-daf2-5a01-82c4-574d4f274998/scratchpad/fonts/package/dist/public/static")
N = "/usr/share/fonts/opentype/noto/NotoSansCJK-"
PURPLE, PANEL = (64, 4, 176, 255), (244, 243, 249, 255)
out, band_txt, name, date, place = sys.argv[1:6]
btn = sys.argv[6] if len(sys.argv) > 6 else "지금 사전등록하기"

band = Image.open(V + "band_origin.png").convert("RGBA"); d = ImageDraw.Draw(band)
d.rectangle((60, 95, 1200, 170), fill=PURPLE)
F = ImageFont.truetype(f"{PRE}/Pretendard-SemiBold.otf", 47); b = F.getbbox(band_txt)
d.text((628.5 - (b[2] - b[0]) / 2 - b[0], 110 - b[1]), band_txt, font=F, fill=(255, 255, 255, 255))
band.save(os.path.join(os.path.dirname(out), "band_" + os.path.basename(out)) + ".png")

info = Image.open(V + "info_origin.png").convert("RGBA"); d = ImageDraw.Draw(info)
sep = info.crop((360, 55, 380, 108))
d.rectangle((112, 52, 650, 108), fill=PANEL); d.rectangle((112, 110, 650, 160), fill=PANEL)
def put(t, font, x, top, col):
    bb = font.getbbox(t); d.text((x - bb[0], top - bb[1]), t, font=font, fill=col); return x + (bb[2] - bb[0])
FB = ImageFont.truetype(N + "Bold.ttc", 30, index=1); FR = ImageFont.truetype(N + "Regular.ttc", 30, index=1)
x = put(name, FB, 122, 65, PURPLE)
info.paste(sep, (x + 14, 55))
put(date, FR, x + 48, 67, (26, 26, 26, 255))
put(place, FR, 122, 121, (26, 26, 26, 255))
arrow = info.crop((1120, 80, 1165, 140))
d.rectangle((725, 74, 1175, 146), fill=PURPLE)
bb = FB.getbbox(btn); tw = bb[2] - bb[0]; gx = 949.5 - (tw + 25 + 21) / 2
put(btn, FB, gx, 98, (255, 255, 255, 255)); info.paste(arrow, (int(gx + tw + 25 - 11), 80))
W, H = info.size                                    # 630px 꽉 차게: 원본 픽셀만 잘라 이어 붙임
full = Image.new("RGBA", (W, H), (0, 0, 0, 0))
full.paste(info.crop((28, 0, 640, H)), (0, 0)); full.paste(info.crop((640, 0, 696, H)), (612, 0)); full.paste(info.crop((640, 0, 1232, H)), (668, 0))
full.save(os.path.join(os.path.dirname(out), "info_" + os.path.basename(out)) + ".png")
print("ok")
