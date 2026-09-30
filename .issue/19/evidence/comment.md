## 작업 리포트 — 담당자·서비스 모듈 전송 추가

CLI 스크립트라서 캡처 대신 실행 결과를 남깁니다. 실데이터 값(연락처·계정)은 증거에 넣지 않았습니다.

### 전후
| | 이전 | 이후 |
|---|---|---|
| 전송 가능한 모듈 | project (`post_projects.py`) | project·contact·service (`post_contents.py <module>`) |
| API 주소 | 스크립트 기본값으로 박혀 있음 | `WOORI_API_BASE_URL` / `--base-url`로만 받음 (코드·문서에서 제거) |
| 빈 값 | 날짜만 생략 | 모든 선택 필드를 비어 있으면 생략 |
| 이미 보낸 행 제외 | 불가 | `--skip IDX` |

### 검증 — [after/verify.txt](after/verify.txt)
- 프로젝트 234건 dry-run 출력이 #17 스크립트와 **바이트 단위로 동일** (md5 일치) → 이미 보낸 프로젝트와 형식 차이 없음
- 담당자·서비스 샘플 행이 검수용 샘플과 일치 (서비스는 키 순서까지)
- 주소 없이 / 키 없이 `--send` → 각각 에러 + exit 1
- 로컬 목 서버에 세 모듈 모두 201, 서비스 `content_raw`는 JSON 객체로 도착
- 저장소·증거에 API 주소·키·서비스 비밀번호 0건

### 검수 대기
- 담당자 이름 키 `name` / `title` → `--name-field`
- 서비스 `content_raw` 객체 / 문자열 → `--content-raw-as-string`
- 실서버 전송은 사용자 검수 후
