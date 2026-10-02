#!/usr/bin/env python3
"""월드커피포럼 뉴스레터 빌드 스크립트.

content/volXX.json (원고) → emails/volXX.html (스티비 붙여넣기용 메일 HTML)
                          → newsletters.json (미리보기 페이지 목록)

사용법: python3 build.py
외부 패키지 없이 파이썬 3.8+ 표준 라이브러리만 사용합니다.
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"
EMAILS = ROOT / "emails"      # 완성형 HTML (미리보기용)
STIBEE = ROOT / "stibee"      # 스티비 코드 상자 붙여넣기용 본문 조각

# ── 브랜드 토큰 (Vol.3 기준) ─────────────────────────────────────────────
LIME = "#99F637"      # 핵심 전환 CTA (홈페이지·예매)
PURPLE = "#4004b0"    # 개별 소식 CTA, 카드 제목
TEXT = "#000000"
SPEAKER_GREEN = "#2FA51F"  # 연사 이름 (연두는 흰 배경에서 안 읽혀 진한 초록 사용)
GRAY = "#747579"
FONT = ("AppleSDGothic, apple sd gothic neo, noto sans korean, noto sans korean regular, "
        "noto sans cjk kr, noto sans cjk, nanum gothic, malgun gothic, dotum, arial, "
        "helvetica, MS Gothic, sans-serif")

# ── 공통 자산 (Vol.3에서 재사용) ──────────────────────────────────────────
ASSETS = {
    "header": "https://img2.stibee.com/14802_3595437_1789536690880736789.gif",
    "divider_top": "https://img2.stibee.com/14802_3571771_1788147093764633846.gif",
    "divider_mid": "https://img2.stibee.com/14802_3571771_1788147114051324733.gif",
    "divider_bottom": "https://img2.stibee.com/14802_3571771_1788156256675401376.gif",
    "ticket_banner": "https://img2.stibee.com/14802_3595437_1789521954558632150.png",
    "closing_character": "https://img2.stibee.com/14802_3595437_1789452284806237261.png",
}
LINKS = {
    "HOME": "https://www.wclforum.org/kr/",
    "TICKET": "https://booking.naver.com/booking/5/bizes/1235751",
    "INSTAGRAM": "https://www.instagram.com/wcf_coffeeforum/",
    "FACEBOOK": "https://www.facebook.com/worldcoffeeforum",
    "YOUTUBE": "https://www.youtube.com/channel/UCVt0lo1net8megxBx84B25g",
    "LINKTREE": "https://linktr.ee/WorldCoffeeForum",
}


def url(value):
    """'TICKET' 같은 키는 실제 링크로, 그 외는 그대로 (미정 링크는 {{KEY}} 형태로 둠)."""
    if not value:
        return "#"
    return LINKS.get(value, value)


def rich(text):
    """원고의 간단 표기를 HTML로: 빈 줄=문단, 줄바꿈=<br>, **굵게**, [[보라색 강조]]."""
    parts = []
    for para in str(text).strip().split("\n\n"):
        p = html.escape(para, quote=False)
        p = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", p)
        p = re.sub(r"\[\[(.+?)\]\]", rf'<span style="color:{PURPLE};">\1</span>', p)
        p = p.replace("\n", "<br>")
        parts.append(p)
    return parts


def paragraphs(text, align="left", size=16):
    return "".join(
        f'<p style="margin:0 0 14px;text-align:{align};font-size:{size}px;line-height:1.7;">{p}</p>'
        for p in rich(text))


# ── 블록 뼈대 ──────────────────────────────────────────────────────────
def row(inner, pad="0"):
    return (f'<tr><td style="padding:{pad};font-family:{FONT};color:{TEXT};'
            f'word-break:break-word;">{inner}</td></tr>\n')


def two_col(left, right, pad="15px"):
    cell = ('<div class="col" style="display:inline-block;vertical-align:top;width:50%;'
            f'min-width:280px;max-width:315px;box-sizing:border-box;padding:{pad};text-align:left;">')
    return (f'<tr><td style="font-size:0;text-align:center;font-family:{FONT};color:{TEXT};">'
            f'{cell}{left}</div>{cell}{right}</div></td></tr>\n')


def img(src, width="100%", alt="", link=None):
    tag = (f'<img src="{html.escape(src)}" width="{630 if width == "100%" else width}" alt="{html.escape(alt)}" '
           f'style="display:block;width:{width if width == "100%" else str(width) + "px"};max-width:100%;'
           'height:auto;border:0;">')
    return f'<a href="{html.escape(url(link))}" target="_blank">{tag}</a>' if link else tag


def placeholder(label, height=300, width="100%"):
    """아직 없는 이미지 자리. 디자인 시안이 오면 block에 "src"를 넣으면 교체됩니다."""
    w = "100%" if width == "100%" else f"{width}px"
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="width:{w};max-width:100%;">'
            f'<tr><td class="ph" height="{height}" style="height:{height}px;background:#F1ECFF;'
            f'border:2px dashed #B7A4F0;text-align:center;vertical-align:middle;font-family:{FONT};'
            f'font-size:13px;line-height:1.6;color:{PURPLE};padding:12px;">'
            f'<b>IMAGE</b><br>{html.escape(label)}</td></tr></table>')


def picture(block, default_h=300, width="100%"):
    if block.get("src"):
        return img(url(block["src"]) if block["src"] not in ASSETS else ASSETS[block["src"]],
                   width, block.get("alt", ""), block.get("link"))
    return placeholder(block.get("placeholder", "이미지"), block.get("h", default_h), width)


def button(label, link, color="lime"):
    bg, fg = (LIME, "#000000") if color == "lime" else (PURPLE, "#ffffff")
    return (f'<table role="presentation" align="center" cellpadding="0" cellspacing="0" '
            f'style="margin:0 auto;border-collapse:separate;"><tr><td align="center" '
            f'style="background:{bg};border-radius:500px;">'
            f'<a href="{html.escape(url(link))}" target="_blank" style="display:inline-block;'
            f'padding:19px 24px;font-family:{FONT};font-size:16px;line-height:1;color:{fg};'
            f'text-decoration:none;">{html.escape(label)}</a></td></tr></table>')


# ── 모듈 (M1–M10 + 확장) ─────────────────────────────────────────────────
def m_header(b):          # M1 헤더 배너
    return row(img(ASSETS["header"], alt="World Coffee Forum 2026"))


def m_image(b):           # M2 대표 비주얼 / M3 섹션 타이틀 배너
    pad = "0 15px" if b.get("inset") else "0"
    return row(picture(b, b.get("h", 360)), pad)


def m_text(b):            # 가운데/왼쪽 정렬 본문
    return row(paragraphs(b["text"], b.get("align", "center")), "15px 15px 1px")


def m_spacer(b):
    return f'<tr><td height="{b.get("h", 20)}" style="height:{b.get("h", 20)}px;font-size:0;">&nbsp;</td></tr>\n'


def m_story(b):           # M4 2단 스토리 (reverse=true면 텍스트가 왼쪽)
    pic = picture(b, 285, 285)
    title = (f'<p style="margin:0 0 8px;font-size:17px;line-height:1.5;color:{PURPLE};">'
             f'<b>{html.escape(b["title"])}</b></p>') if b.get("title") else ""
    txt = title + paragraphs(b["text"])
    return two_col(txt, pic) if b.get("reverse") else two_col(pic, txt)


def m_body_cta(b):        # M5 1단 본문 + 메인 CTA
    out = row(paragraphs(b["text"], b.get("align", "left")), "15px 15px 0")
    if b.get("cta"):
        out += row(button(b["cta"], b.get("link"), b.get("color", "lime")), "20px 15px 15px")
    return out


def m_card(b):            # M6 2단 소식 카드
    pic = picture(b, 285, 285)
    txt = (f'<p style="margin:0 0 6px;font-size:16px;line-height:1.6;color:{PURPLE};">{html.escape(b["title"])}</p>'
           + paragraphs(b["text"]))
    if b.get("cta"):
        txt += f'<div style="padding-top:6px;">{button(b["cta"], b.get("link"), b.get("color", "purple"))}</div>'
    return two_col(pic, txt)


def m_ticket(b):          # M7 티켓 배너 + 예매 CTA
    out = ""
    if b.get("headline"):
        out += row(f'<p style="margin:0;text-align:center;font-size:20px;line-height:1.5;"><b>'
                   f'{"<br>".join(rich(b["headline"]))}</b></p>', "20px 15px 5px")
    if b.get("banner") is False:      # 배너 없이 문구+버튼만
        pass
    elif b.get("src") or b.get("placeholder"):
        out += row(picture(b, 240), "0 15px")
    else:
        out += row(img(ASSETS["ticket_banner"], alt="얼리버드 티켓"), "0 15px")
    if b.get("text"):
        out += row(paragraphs(b["text"], "center", 14), "12px 15px 0")
    out += row(button(b.get("cta", "티켓 예매 바로가기"), b.get("link", "TICKET")), "20px 15px 25px")
    return out


def m_divider(b):         # M8 구분 GIF
    return row(img(ASSETS[b.get("style", "divider_top")], alt=""))


def m_closing(b):         # M9 2단 클로징
    pic = img(ASSETS["closing_character"], 285, "월드커피포럼 캐릭터")
    return two_col(paragraphs(b["text"]), pic)


def m_footer(b):          # M10 SNS + 푸터
    icons = [("HOME", "homepage2"), ("INSTAGRAM", "instagram"), ("FACEBOOK", "facebook"),
             ("YOUTUBE", "youtube"), ("LINKTREE", "homepage")]
    sns = "".join(
        f'<a href="{LINKS[k]}" target="_blank" style="display:inline-block;padding:0 10px;">'
        f'<img src="https://resource.stibee.com/editor/icon/sns/{i}-snsA.png" height="30" '
        f'style="height:30px;width:auto;vertical-align:middle;border:0;" alt="{k.title()}"></a>'
        for k, i in icons)
    foot = (f'<div style="text-align:center;font-size:12px;line-height:1.7;color:{GRAY};">'
            'World Coffee Forum<br>info@wclforum.org<br>'
            '5, Baekjegobun-ro 9-gil, Songpa-gu, Seoul 02-6000-6720<br>'
            f'<a href="$%unsubscribe%$" style="color:{GRAY};text-decoration:underline;">수신거부</a>&nbsp;'
            f'<a href="$%unsubscribe%$" style="color:{GRAY};text-decoration:underline;">Unsubscribe</a></div>')
    return (row(f'<div style="text-align:center;">{sns}</div>', "15px")
            + row(img(ASSETS["divider_bottom"], alt=""))
            + row(foot, "15px"))


def m_qa(b):              # 무물 Q&A 목록
    items = "".join(
        f'<tr><td style="padding:14px 0;border-bottom:1px solid #E6E0F5;font-family:{FONT};">'
        f'<p style="margin:0 0 6px;font-size:16px;line-height:1.6;color:{PURPLE};"><b>Q. {html.escape(q["q"])}</b></p>'
        f'<p style="margin:0;font-size:15px;line-height:1.7;color:{TEXT};">A. {"<br>".join(rich(q["a"]))}</p></td></tr>'
        for q in b["items"])
    return row(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{items}</table>', "5px 15px 15px")


def m_stats(b):           # 숫자로 보는 포럼
    cell = ('<div class="col" style="display:inline-block;vertical-align:top;width:50%;max-width:157px;'
            'box-sizing:border-box;padding:10px 6px;text-align:center;">')
    cells = "".join(
        f'{cell}<div style="font-size:30px;line-height:1.2;color:{PURPLE};font-family:{FONT};"><b>{html.escape(s["value"])}</b></div>'
        f'<div style="font-size:13px;line-height:1.5;color:{GRAY};font-family:{FONT};">{html.escape(s["label"])}</div></div>'
        for s in b["items"])
    return f'<tr><td style="font-size:0;text-align:center;padding:10px 9px;">{cells}</td></tr>\n'


def m_notice(b):          # 강조 박스 (긴급 공지·마감 안내)
    return row(f'<div style="background:#F5FFE8;border-left:5px solid {LIME};padding:16px 18px;">'
               f'{paragraphs(b["text"], "left", 15)}</div>', "10px 15px")


def m_band(b):            # 보라 섹션 타이틀 띠 (이미지 배너가 없을 때)
    return row(f'<div style="background:{PURPLE};padding:16px 15px;text-align:center;font-size:20px;'
               f'line-height:1.4;color:#ffffff;"><b>{html.escape(b["text"])}</b></div>', "10px 0")


def m_speaker(b):         # 연사 소개 (사진 + 발표 제목 + 하이라이트 태그 + 이름 + 약력)
    right = bool(b.get("reverse"))            # true면 사진이 오른쪽, 글은 오른쪽 정렬
    align = "right" if right else "left"
    bg = "#F2F2F2" if b.get("shade") else "#FFFFFF"
    p = lambda css, inner: f'<p style="margin:0;text-align:{align};{css}">{inner}</p>'
    txt = ""
    if b.get("headline"):
        txt += p("margin-bottom:12px;font-size:18px;line-height:1.45;color:#111111;",
                 "<b>" + "<br>".join(rich(b["headline"])) + "</b>")
    if b.get("tag"):
        txt += p("margin-bottom:10px;", f'<span style="display:inline-block;background:{LIME};padding:4px 10px;'
                 f'font-size:13px;line-height:1.5;color:#111111;"><b>{html.escape(b["tag"])}</b></span>')
    txt += p(f"margin-bottom:8px;font-size:22px;line-height:1.3;color:{SPEAKER_GREEN};",
             f'<b>{html.escape(b["name"])}</b>')
    if b.get("desc"):
        txt += p("margin-bottom:8px;font-size:13px;line-height:1.65;color:#444444;", "<br>".join(rich(b["desc"])))
    for d in b.get("details", []):
        txt += p("font-size:12px;line-height:1.7;color:#777777;",
                 html.escape(f"{d} |" if right else f"| {d}"))
    cell = ('<div style="display:inline-block;vertical-align:middle;width:50%;min-width:280px;max-width:315px;'
            'box-sizing:border-box;padding:{pad};text-align:{al};">')
    pic = cell.format(pad="20px 15px", al="center") + picture(b, 285, 285) + "</div>"
    body = cell.format(pad="20px 18px", al=align) + txt + "</div>"
    inner = body + pic if right else pic + body
    return (f'<tr><td style="background:{bg};font-size:0;text-align:center;font-family:{FONT};'
            f'color:{TEXT};word-break:keep-all;">{inner}</td></tr>\n')


MODULES = {
    "header": m_header, "image": m_image, "text": m_text, "spacer": m_spacer,
    "story": m_story, "body_cta": m_body_cta, "card": m_card, "ticket": m_ticket,
    "divider": m_divider, "closing": m_closing, "footer": m_footer,
    "qa": m_qa, "stats": m_stats, "notice": m_notice,
    "band": m_band, "speaker": m_speaker,
}


def render(vol):
    body = "".join(MODULES[b["type"]](b) for b in vol["blocks"])
    pre = html.escape(vol["preheader"])
    return f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(vol["subject"])}</title>
<style>@media only screen and (max-width:640px){{.col{{max-width:100%!important;width:100%!important;}}}}</style>
</head>
<body style="width:100%;margin:0;padding:0;background:#ffffff;">
<div style="display:none;max-height:0;overflow:hidden;font-size:0;line-height:0;">{pre}</div>
<div style="width:100%;padding:40px 0;">
<table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;width:94%;max-width:630px;background:#ffffff;">
{body}</table>
</div>
</body></html>
"""


# 스티비 'HTML 코드 상자'가 저장하지 않는 태그 (편집기 안내 문구 기준)
STIBEE_FORBIDDEN = ["html", "head", "body", "style", "script", "iframe", "audio", "video",
                    "embed", "object", "noscript", "meta", "form", "input", "button", "title", "link"]


def stibee_snippet(full_html):
    """완성형 메일 HTML → 스티비 코드 상자에 붙여넣을 수 있는 본문 조각.

    - <body> 안쪽만 남기고 금지 태그(<style>, <meta> 등)와 주석을 제거
    - 숨김 프리헤더 제거 (스티비 '프리헤더' 입력란에 따로 넣음)
    - 바깥 여백은 스티비가 주므로 0으로
    """
    m = re.search(r"<body[^>]*>(.*)</body>", full_html, flags=re.S | re.I)
    s = m.group(1) if m else full_html
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    for tag in ("style", "script", "title", "noscript"):
        s = re.sub(rf"<{tag}\b.*?</{tag}>", "", s, flags=re.S | re.I)
    s = re.sub(r"</?(?:meta|link|html|head|body)\b[^>]*>", "", s, flags=re.I)
    s = re.sub(r'<div style="[^"]*display:\s*none[^"]*">.*?</div>', "", s, count=1, flags=re.S)
    s = s.replace("padding:40px 0;", "padding:0;").replace("width:94%;max-width:630px",
                                                             "width:100%;max-width:630px")
    s = s.strip() + "\n"
    bad = [t for t in STIBEE_FORBIDDEN if re.search(rf"<{t}\b", s, flags=re.I)]
    if bad:
        raise SystemExit(f"스티비 금지 태그가 남아 있습니다: {bad}")
    return s


def main():
    EMAILS.mkdir(exist_ok=True)
    STIBEE.mkdir(exist_ok=True)
    manifest = []
    for path in sorted(CONTENT.glob("vol*.json")):
        vol = json.loads(path.read_text(encoding="utf-8"))
        entry = {k: v for k, v in vol.items() if k != "blocks"}
        full = EMAILS / f"{vol['id']}.html"
        if vol.get("blocks"):
            full.write_text(render(vol), encoding="utf-8")
        (STIBEE / f"{vol['id']}.html").write_text(
            stibee_snippet(full.read_text(encoding="utf-8")), encoding="utf-8")
        entry["file"] = f"emails/{vol['id']}.html"
        entry["stibee"] = f"stibee/{vol['id']}.html"
        manifest.append(entry)
        print(f"  {vol['id']}  {vol.get('send_date', '')}  {vol['subject']}")
    (ROOT / "newsletters.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"built {len(manifest)} newsletters")
    build_standalone(manifest)


def build_standalone(manifest):
    """메일로 공유하거나 Claude 아티팩트로 올릴 수 있는 단일 파일 미리보기."""
    bundle = {"list": manifest,
              "html": {m["id"]: (ROOT / m["file"]).read_text(encoding="utf-8")
                       for m in manifest if (ROOT / m["file"]).exists()},
              "stibee": {m["id"]: (ROOT / m["stibee"]).read_text(encoding="utf-8")
                         for m in manifest}}
    data = json.dumps(bundle, ensure_ascii=False).replace("</", "<\\/")
    page = (ROOT / "index.html").read_text(encoding="utf-8")
    for tag in (r"<!doctype html>", r"<html[^>]*>", r"</html>", r"</?head>", r"</?body>"):
        page = re.sub(tag, "", page, flags=re.I)
    page = page.replace("<script>", f"<script>window.__NEWSLETTERS__={data};</script>\n<script>", 1)
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    (out / "preview-standalone.html").write_text(page.strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
