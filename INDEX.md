# 문서 색인

질문을 받으면 이 파일을 가장 먼저 읽는다. `summary`와 `keywords`로 관련 문서를 고른 뒤 해당 `path`만 연다.
문서를 추가·삭제·수정하면 이 색인과 해당 문서의 프론트매터(`last_updated`)를 함께 갱신한다.

## 라우팅 규칙

| 질문 유형 | 먼저 볼 문서 |
|---|---|
| 테이블·모듈 관계, 모듈 ID, 적재 순서 | `docs/overview/structure.md` |
| 특정 필드의 형식·허용값, `accounts`/`host`, 검증 규칙, 인계본 대응 | `docs/spec/import-csv-spec.md` |
| 스크립트 실행, 옵션, 건수, 검증 실패, 보안 | `docs/guides/build-import-csv.md` |

## 문서 목록

```yaml
- path: docs/overview/structure.md
  title: 업체·담당자·프로젝트·서비스 데이터 구조
  category: overview
  summary: 업체는 wr_company_t, 담당자·프로젝트·서비스는 wr_module_t 게시판에 속한 wr_content_t 콘텐츠로 저장되는 구조와 고정 module_idx, company_idx·parent_idx 관계, 적재 순서.
  keywords: [구조, 관계, ERD, wr_company_t, wr_content_t, wr_module_t, module_idx, company_idx, parent_idx, 담당자, 프로젝트, 서비스, 적재 순서, receiver_idx, ref_idx]

- path: docs/spec/import-csv-spec.md
  title: 이관 CSV 필드 명세
  category: spec
  summary: 적재용 CSV 4개의 헤더·필드 형식·필수 여부·허용값, content_raw.accounts JSON 규칙(host는 FTP 전용), 인계본 → CSV 대응, 적재 전 검증 체크리스트 11항목. 필드 규칙의 기준 문서.
  keywords: [CSV, 필드 명세, wr_company_t, wr_content_t, company_idx, parent_idx, module_idx, status, type, date_end, url, content_raw, accounts, host, FTP, DB_iwinv, is_hidden, UUID v7, 검증 체크리스트, 인계본]

- path: docs/guides/build-import-csv.md
  title: 적재용 CSV 생성 가이드
  category: guide
  summary: scripts/build_import_csv.py로 ubot 인계본을 적재용 CSV 4개로 변환하는 방법 — 실행 명령, 옵션, 대상 기준과 현재 건수, 자동 검증과 실패 시 동작, 실데이터 보안 주의사항.
  keywords: [build_import_csv.py, 스크립트, 실행 방법, 인계본, ubot, data/import, --include-history, 현행 서비스, 검증 실패, 건수, 보안, gitignore, 평문 비밀번호]
```

## 문서 외 자료

```yaml
- path: scripts/build_import_csv.py
  summary: 인계본 → 적재용 CSV 변환과 명세 9장 자동 검증
- path: examples/
  summary: 명세를 통과하는 가짜 값 예시 CSV 4개 (company, contact_module, project_module, service_module)
```
