# 월드커피포럼 뉴스레터 저장소

2026 월드커피포럼(WCF) 뉴스레터 Vol.4–11 원고와 스티비 발송용 HTML을 관리합니다.
GitHub Pages에 미리보기 페이지가 올라가 있고, main에 push하면 1~2분 뒤 자동 반영됩니다.

## 구조

- `content/volXX.json` — 원고. **수정은 항상 여기서** 합니다.
- `build.py` — 원고를 `emails/volXX.html`과 `newsletters.json`으로 변환. 모듈(M1–M10) 템플릿이 들어 있음.
- `emails/volXX.html` — 빌드 결과(완성형 HTML, 미리보기용). 직접 고치지 않습니다.
  예외: `emails/vol03.html`은 실제 발송된 원본이라 빌드 대상이 아니며 수정 금지.
- `stibee/volXX.html` — 빌드 결과(스티비 **HTML 코드 상자**용 본문 조각). 코드 상자는 `<html> <head> <body> <style> <script> <iframe> <meta> <form> <input> <button>` 등을 저장하지 않으므로 이 태그들을 뺀 버전입니다. build.py가 금지 태그가 남으면 에러를 냅니다.
- `index.html` — 미리보기 페이지. `dist/preview-standalone.html`은 공유용 단일 파일(빌드 시 생성, git 제외).

## 작업 순서 (매번)

1. `content/volXX.json` 수정
2. `python3 build.py` 실행 — 에러 없이 끝나는지 확인
3. 커밋 메시지에 회차를 적고 main에 push (예: `vol04: 신규 연사 3명 반영`)

## 원고 JSON 규칙

- 최상위 필드: `id, vol, send_date, weekday, title, main, status, subject, preheader, note, assets, blocks`
- `status`: `초안` → `검토중` → `확정` → `발송 완료`
- 미확정 정보는 `[대괄호]`로 남겨 둡니다. 미리보기에서 노란색으로 표시되고 개수가 집계됩니다.
- 미정 링크는 `{{LINEUP_URL}}`처럼 대문자 키로 둡니다. 확정되면 실제 URL로 교체.
- 링크 약어: `HOME`, `TICKET`, `INSTAGRAM`, `FACEBOOK`, `YOUTUBE`, `LINKTREE` (build.py의 LINKS)
- 본문 표기: 빈 줄 = 문단, 줄바꿈 = `<br>`, `**굵게**`, `[[보라색 강조]]`

## 블록(type) 목록

| type | 모듈 | 주요 필드 |
| --- | --- | --- |
| header | M1 헤더 GIF | – |
| image | M2 대표 비주얼 / M3 섹션 타이틀 | `src` 또는 `placeholder`+`h`, `link`, `inset` |
| text | 가운데 정렬 소개문 | `text`, `align` |
| spacer | 여백 | `h` |
| story | M4 2단 스토리 | `src`/`placeholder`, `title`, `text`, `reverse` |
| body_cta | M5 본문 + 버튼 | `text`, `cta`, `link`, `color`(lime/purple), `align` |
| card | M6 소식 카드 | `src`/`placeholder`, `title`, `text`, `cta`, `link` |
| ticket | M7 티켓 배너 + 예매 버튼 | `headline`, `text`, `cta`, `link`(기본 TICKET), `banner:false`, `src`/`placeholder` |
| divider | M8 구분 GIF | `style`: divider_top / divider_mid |
| closing | M9 클로징 + 캐릭터 | `text` (마지막 문장은 다음 호 예고) |
| footer | M10 SNS + 주소 + 수신거부 | – |
| qa | 무물 Q&A | `items: [{q, a}]` |
| stats | 숫자 타일 | `items: [{value, label}]` |
| notice | 강조 박스(긴급 공지) | `text` |
| band | 보라 섹션 타이틀 띠(배너 이미지 대용) | `text` |
| speaker | 연사 소개(사진+발표 제목+연두 태그+이름+약력) | `headline`, `tag`, `name`, `desc`, `details[]`, `src`/`placeholder`, `reverse`(사진 오른쪽), `shade`(회색 배경) |

이미지가 준비되면 `placeholder`를 지우고 `"src": "https://img2.stibee.com/..."`를 넣습니다
(스티비에 이미지를 먼저 업로드해 URL을 받습니다).

## 디자인 규칙 (Vol.3 기준)

- 모바일 대응은 `<style>` 미디어쿼리 없이 인라인 스타일만으로 합니다(2단 칸은 `display:inline-block; width:50%; min-width:280px; max-width:315px` — 스티비 코드 상자처럼 630px보다 좁은 칸에서도 2단을 유지하고, 560px 미만 모바일에서는 한 줄씩 쌓임). 모듈에 새 `<style>`을 추가하지 마세요.

- 폭 630px, 2단 블록은 315px씩, 모바일에서 1단 전환
- 연두 `#99F637` 버튼 = 핵심 전환(전체 라인업·예매). **한 호에 연두 버튼 최대 2개**
- 보라 `#4004b0` 버튼 = 개별 소식 상세. 카드 제목도 보라
- 톤: 대화체("~했습니다", "~만나보세요"), 이모지는 문단당 1개 이내
- Vol.4–10은 티켓 블록 필수, Vol.11은 제외
- 일정 전제: 개막 11/11(수)~11/14(토), 얼리버드 마감 10/30(금)
