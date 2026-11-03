"""현황판(board) 블록을 날짜별 흰 배경 PNG로 뽑는다(다크모드에서도 글자가 보이게). 630px 폭에 꽉 차게(보라 날짜 블록이 왼쪽 끝, 선이 오른쪽 끝까지), 2배 = 1260px. 패널·여백 없음.

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
    inner = build.m_board({**board, "days": [day], "pad": "0"})
    pages.append(f'<div id="d{i}" style="width:630px;box-sizing:border-box;background:#FFFFFF;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">'
                 f'{inner}</table></div><div style="height:20px"></div>')
pages.append("</body></html>")
tmp = tempfile.mkdtemp()
open(f"{tmp}/b.html", "w").write("".join(pages))
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();"
      "const p=await b.newPage({viewport:{width:630,height:900},deviceScaleFactor:2});"
      f"await p.goto('file://{tmp}/b.html');await p.waitForTimeout(800);"
      f"for(let i=0;i<{len(board['days'])};i++){{await (await p.$('#d'+i)).screenshot({{path:'{tmp}/d'+i+'.png',omitBackground:true}});}}"
      "await b.close()})()")
subprocess.run(["node", "-e", js], check=True)
for i, day in enumerate(board["days"]):
    out = Image.open(f"{tmp}/d{i}.png")
    assert out.size[0] == 1260, out.size
    bb = out.getbbox()                 # 위아래 빈 줄 잘라냄(폭은 1260 그대로)
    out = out.crop((0, bb[1], 1260, bb[3]))
    out.save(f"{prefix}_{day['num']}.png")
    print(f"{prefix}_{day['num']}.png", out.size)
