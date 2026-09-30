# WCF Newsletter 2026

월드커피포럼 뉴스레터 Vol.4–11 초안과 미리보기.

- 미리보기: `https://jongabaek.github.io/wcf.newsletter/` (Pages 설정 후)
- 원고: `content/volXX.json` → `python3 build.py` → `emails/volXX.html`

## 처음 한 번만 설정

1. **Settings → Pages → Build and deployment → Source**를 `GitHub Actions`로 바꿉니다.
2. main에 push하면 Actions 탭에서 `Deploy preview to GitHub Pages`가 돌고, 1~2분 뒤 위 주소에 반영됩니다.

## 수정하고 반영하기

```bash
python3 build.py        # 원고 → HTML
git add -A && git commit -m "vol04: 연사 확정 반영" && git push
```

Claude Code에서 작업할 때는 "Vol.4 신규 연사를 ○○로 바꾸고 푸시해 줘"처럼 말하면 됩니다.
작업 규칙은 `CLAUDE.md`에 있습니다.

## 스티비로 옮기기

미리보기 페이지에서 회차를 고르고 **HTML 복사** → 스티비 이메일 편집기의 HTML 블록(또는 HTML 에디터)에 붙여넣기.
발송 전 대괄호·이미지 자리·미정 링크 개수가 모두 0인지 확인하세요.
