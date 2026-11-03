"""현황판(board) 블록을 날짜별 투명 배경 PNG로 뽑는다 (5호 카드 톤: 연회색 둥근 패널, 1260px 폭 = 좌우 28px 여백).

사용: python3 tools/render_board_png.py tools/data/vol06_sca_board.json assets/vol06/board_sca
  → assets/vol06/board_sca_12.png, _13.png, _14.png (날짜 num이 파일 끝에 붙음)
필요: playwright(크로미움), Noto Sans CJK KR 글꼴.
"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import build
from PIL import Image

src, prefix = sys.argv[1], sys.argv[2]
repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
board = json.load(open(src))
pages = ['<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:transparent}'
         '*{font-family:"Noto Sans CJK KR",sans-serif!important}</style></head><body>']
for i, day in enumerate(board["days"]):
    day = json.loads(json.dumps(day))
    for it in day["items"]:
        it["photos"] = [p.replace("https://jongabaek.github.io/wcf.newsletter/", f"file://{repo}/") if p else p
                        for p in it.get("photos", [])]
    inner = build.m_board({**board, "days": [day]})
    pages.append(f'<div id="d{i}" style="width:602px;box-sizing:border-box;background:#F6F5FA;border-radius:18px;'
                 f'padding:14px 14px 10px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">'
                 f'{inner}</table></div><div style="height:20px"></div>')
pages.append("</body></html>")
tmp = tempfile.mkdtemp()
open(f"{tmp}/b.html", "w").write("".join(pages))
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();"
      "const p=await b.newPage({viewport:{width:640,height:900},deviceScaleFactor:2});"
      f"await p.goto('file://{tmp}/b.html');await p.waitForTimeout(800);"
      f"for(let i=0;i<{len(board['days'])};i++){{await (await p.$('#d'+i)).screenshot({{path:'{tmp}/d'+i+'.png',omitBackground:true}});}}"
      "await b.close()})()")
subprocess.run(["node", "-e", js], check=True)
for i, day in enumerate(board["days"]):
    im = Image.open(f"{tmp}/d{i}.png")
    out = Image.new("RGBA", (1260, im.size[1]), (0, 0, 0, 0))
    out.alpha_composite(im, (28, 0))
    out.save(f"{prefix}_{day['num']}.png")
    print(f"{prefix}_{day['num']}.png", out.size)
