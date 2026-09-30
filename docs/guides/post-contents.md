---
id: guide-post-contents
title: 콘텐츠 API 적재 가이드
category: guide
summary: scripts/post_contents.py로 project·contact·service 모듈 CSV를 우리기획 API(POST /contents)에 한 행씩 보내는 방법 — 모듈별 요청 형식, date_start KST→UTC 변환, 빈 값 생략, 환경변수로만 받는 API 주소·키, dry-run 기본값, 실패 행 재시도.
keywords: [post_contents.py, API, POST /contents, x-key, WOORI_API_KEY, WOORI_API_BASE_URL, dry-run, --send, --only, --skip, date_start, KST, UTC, 프로젝트, 담당자, 서비스, content_raw, --name-field, --content-raw-as-string]
related_files: [scripts/post_contents.py, docs/spec/import-csv-spec.md]
last_updated: 2026-09-30
---

# 콘텐츠 API 적재 가이드

`build_import_csv.py`가 만든 모듈 CSV를 행마다 `POST {BASE_URL}/contents`로 보낸다. Python 3 표준 라이브러리만 쓴다.

## 실행

```bash
# API 주소와 키는 환경변수로만 넘긴다 (공개 저장소 — 값은 어디에도 적지 않는다)
export WOORI_API_BASE_URL='<API 주소>'
export WOORI_API_KEY='<x-key>'

python3 scripts/post_contents.py service                  # dry-run: 보낼 JSON만 출력
python3 scripts/post_contents.py service --only <idx> --send   # 한 건만 먼저 보내 본다
python3 scripts/post_contents.py service --send           # 전체 전송
```

적재 순서는 업체 → 담당자·프로젝트 → 서비스다. 서비스의 `parent_idx`가 가리키는 프로젝트가 먼저 있어야 한다.

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `module` | 없음(필수) | `project`, `contact`, `service` |
| `--csv` | `data/import/<module>_module.csv` | 입력 CSV |
| `--base-url` | `$WOORI_API_BASE_URL` | API 주소 (`/contents`가 붙는다). `--send`일 때 필수 |
| `--key` | `$WOORI_API_KEY` | `x-key` 헤더 값. `--send`일 때 필수 |
| `--send` | 꺼짐 | 실제로 전송한다. 없으면 dry-run |
| `--only IDX` / `--skip IDX` | 없음 | 해당 `idx` 행만 처리 / 건너뛴다. 여러 번 줄 수 있다 |
| `--limit N` | 없음 | 앞에서부터 N행만 처리한다 |
| `--timeout` | `30` | 요청당 제한 시간(초) |
| `--name-field` | `name` | 담당자 이름을 보낼 키(`name` 또는 `title`). contact 전용 |
| `--content-raw-as-string` | 꺼짐 | `content_raw`를 JSON 객체 대신 문자열로 보낸다. service 전용 |

## 요청 형식

공통 헤더는 `accept: application/json`, `Content-Type: application/json`, `x-key`다.
**CSV 값이 비어 있으면 그 키를 넣지 않는다.** 아래 값은 가짜다.

| 모듈 | 보내는 키 (순서대로) |
|---|---|
| project | `idx`, `module_idx`, `company_idx`, `title`, `status`, `date_start`, `date_end` |
| contact | `idx`, `module_idx`, `company_idx`, `name`, `contact`, `email` |
| service | `idx`, `module_idx`, `parent_idx`, `company_idx`, `title`, `status`, `type`, `date_start`, `date_end`, `url`, `is_hidden`, `content_raw` |

```json
{
  "idx": "01900000-0000-7000-8000-000000000004",
  "module_idx": "01a05702-067e-729b-85ab-deb5b0836082",
  "parent_idx": "01900000-0000-7000-8000-000000000003",
  "company_idx": "01900000-0000-7000-8000-000000000001",
  "title": "예시 서비스",
  "status": 1,
  "type": 1,
  "date_start": "2024-05-19T15:00:00",
  "url": "service.example.test",
  "is_hidden": 1,
  "content_raw": {"accounts": [{"type": "FTP", "host": "host.example.test", "id": "example-ftp", "pw": "example-only"}]}
}
```

- `status`, `type`, `is_hidden`은 정수로 보낸다.
- `date_start`·`date_end`는 CSV의 `YYYY-MM-DD`를 **KST 자정으로 보고 UTC로 바꾼** 값이다(`2024-05-20` → `2024-05-19T15:00:00`).
- 서비스 `url`에 도메인이 여러 개면 CSV 그대로 쉼표로 이은 문자열이다.

## 결과와 재시도

행마다 `OK`/`ERR`, HTTP 코드, `idx`, 제목(담당자는 이름)을 출력한다. 실패가 있어도 나머지 행은 계속 보내고, 끝에 실패한 `idx` 목록을 출력한 뒤 exit 1로 끝난다. 실패한 행은 `--only <idx>`로 다시 보낸다.

## 보안

- API 주소·키, 실제 요청 샘플, 전송 로그는 코드·문서·커밋·이슈에 넣지 않는다. 공개 저장소다.
- 서비스 요청에는 평문 계정이 들어간다. dry-run 출력도 화면에서만 보고 파일로 남기지 않는다.
