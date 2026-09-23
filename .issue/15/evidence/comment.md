## 작업 리포트 — docs 프론트매터 체계와 INDEX.md

문서만 바뀌어서 화면 캡처 대신 구조 전후와 기계 검증 결과를 남깁니다.

### 전후
| | 이전 | 이후 |
|---|---|---|
| docs 문서 | 6개 (완전 중복 1쌍, 옛 규칙 잔존) | 3개 (`overview/structure`, `spec/import-csv-spec`, `guides/build-import-csv`) |
| 프론트매터 | 없음 | 3개 모두 `id·title·category·summary·keywords·related_files·last_updated` |
| 중앙 색인 | 없음 | 루트 `INDEX.md` (라우팅 규칙 + 문서 목록 YAML) |
| README | 옛 문서 링크 8개 | 한눈 요약·빠른 시작·문서 안내·폴더 구조 |
| examples | `2999-12-31`, 프로젝트 `content_raw.source`, 서비스 `tags`·`content` | 최신 명세(빈 `date_end`, FTP 전용 `host`, 최소 입력) |

### 삭제한 문서와 이관 내용
- `wr-content-erd.md` — `doweb-content-structure.md`와 완전 중복 → 삭제
- `doweb-content-structure.md`, `wr-content-module-fields.md`(역할·관계) → `docs/overview/structure.md`
- `wr-content-module-fields.md`(인계본 대응표) → 명세 10장, 옛 규칙 포함한 필드표는 명세와 중복이라 삭제
- `data-integrity-check.md` → 명세 9장 체크리스트와 중복, 옛 규칙 → 삭제
- `service-sheet-api-field-mapping.md` → 구조 문서와 중복 → 삭제
- `wr-import-field-spec.md` → `docs/spec/import-csv-spec.md`로 이동(대상 선택 규칙을 현행 서비스 기준으로 갱신, 10장 인계본 대응 추가)

### 검증
- docs 모든 `.md` 프론트매터 7개 필드 존재, `related_files` 경로 모두 존재
- `INDEX.md` 항목 = 실제 docs 파일 (1:1)
- README·INDEX·docs의 상대 링크 깨짐 0건
- 옛 규칙(`도메인주소,호스팅주소`, `content_raw.source`, `2999-12-31` 사용) 0건 (금지 문구 1곳만 존재)
- 예시 CSV 4개를 스크립트 `validate()`로 검사 → 오류 0, 스크립트 writer로 생성해 형식 일치
- 실데이터 스크립트 실행 검증 통과(동작 변화 없음)
