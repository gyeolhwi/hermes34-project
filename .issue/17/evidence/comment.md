## 작업 리포트 — 프로젝트 CSV → POST /contents 전송 스크립트

화면이 없는 CLI 스크립트라서 캡처 대신 실행 결과를 남깁니다.

### 전후
| | 이전 | 이후 |
|---|---|---|
| API 적재 수단 | 없음 ([before/scripts.txt](before/scripts.txt)) | `scripts/post_projects.py` |
| 키 관리 | 샘플 curl에 키가 박혀 있음 | `WOORI_API_KEY` 환경변수 / `--key` 로만 받음 |
| 기본 동작 | — | dry-run (보낼 JSON만 출력), `--send` 일 때만 전송 |

### 검증
- dry-run 234건. `전북CBS` 행이 `project_post_sample.md` 의 JSON과 **완전히 같음** (`date_start` `2022-12-20` → `2022-12-19T15:00:00`, KST→UTC) — [after/dry-run.txt](after/dry-run.txt)
- 키 없이 `--send` → 에러 메시지 + exit 1 — [after/dry-run.txt](after/dry-run.txt)
- 로컬 목 서버 전송: `x-key`·`accept`·`Content-Type` 헤더와 본문이 샘플대로 도착, 201 → OK, 400 → ERR + 실패 idx 출력 + exit 1 — [after/mock-send.txt](after/mock-send.txt)
- `git grep` 결과 저장소에 API 키 문자열 없음

### 실서버 전송 전 확인할 것
- 234건 중 119건은 `date_start`가 비어 있어 키 자체를 넣지 않음. API가 이 필드를 필수로 받는지 확인 필요
- `status=0`(원본 값 없음) 73건 — API가 `0`을 허용하는지 확인 필요
- 실서버(`woori-dev`)에는 아직 보내지 않음
