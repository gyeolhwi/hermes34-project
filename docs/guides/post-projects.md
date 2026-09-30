---
id: guide-post-projects
title: 프로젝트 API 적재 가이드
category: guide
summary: scripts/post_projects.py로 project_module.csv의 프로젝트를 우리기획 API(POST /contents)에 한 행씩 보내는 방법 — 요청 형식, date_start KST→UTC 변환, 환경변수로 넘기는 API 키, dry-run 기본값, 실패 행 재시도.
keywords: [post_projects.py, API, POST /contents, x-key, WOORI_API_KEY, WOORI_API_BASE_URL, dry-run, --send, --only, date_start, KST, UTC, 프로젝트 적재]
related_files: [scripts/post_projects.py, docs/spec/import-csv-spec.md]
last_updated: 2026-09-30
---

# 프로젝트 API 적재 가이드

`build_import_csv.py`가 만든 `project_module.csv`를 행마다 `POST {BASE_URL}/contents`로 보낸다. Python 3 표준 라이브러리만 쓴다.

## 실행

```bash
# 1) dry-run: 보낼 JSON만 한 줄씩 출력한다 (기본값)
python3 scripts/post_projects.py

# 2) 한 건만 먼저 보내 본다
export WOORI_API_KEY='<x-key>'
python3 scripts/post_projects.py --only <idx> --send

# 3) 전체 전송
python3 scripts/post_projects.py --send
```

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--csv` | `data/import/project_module.csv` | 입력 CSV |
| `--base-url` | `$WOORI_API_BASE_URL` 또는 `https://woori-dev.doweb.kr:3000` | API 주소 (`/contents`가 붙는다) |
| `--key` | `$WOORI_API_KEY` | `x-key` 헤더 값. `--send`일 때 필수 |
| `--send` | 꺼짐 | 실제로 전송한다. 없으면 dry-run |
| `--only IDX` | 없음 | 해당 `idx` 행만 처리한다. 여러 번 줄 수 있다 |
| `--limit N` | 없음 | 앞에서부터 N행만 처리한다 |
| `--timeout` | `30` | 요청당 제한 시간(초) |

## 요청 형식

```json
{
  "idx": "<프로젝트 idx>",
  "module_idx": "01a05701-ed99-7cfa-841e-ec6f6c9922a0",
  "company_idx": "<업체 idx>",
  "title": "<프로젝트명>",
  "status": 1,
  "date_start": "2022-12-19T15:00:00"
}
```

- `status`는 정수로 보낸다.
- `date_start`는 CSV의 `YYYY-MM-DD`를 **KST 자정으로 보고 UTC로 바꾼** 값이다(`2022-12-20` → `2022-12-19T15:00:00`). CSV가 비어 있으면 키를 넣지 않는다.
- 헤더는 `accept: application/json`, `Content-Type: application/json`, `x-key`다.

## 결과와 재시도

행마다 `OK`/`ERR`, HTTP 코드, `idx`, 제목을 출력한다. 실패가 있어도 나머지 행은 계속 보내고, 끝에 실패한 `idx` 목록을 출력한 뒤 exit 1로 끝난다. 실패한 행은 `--only <idx>`로 다시 보낸다.

적재 순서상 업체(`company_idx`)가 API 쪽에 먼저 있어야 한다.

## 보안

API 키는 코드·문서·커밋에 넣지 않고 환경변수로만 넘긴다. 공개 저장소다.
