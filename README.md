# Hermes34 → 우리기획 공용 API 적재 구조

## 핵심

Hermes34는 물리적으로는 **`wr_content_t` 한 테이블**만 사용합니다.

고객·프로젝트·사이트는 별도 물리 테이블이 아니라, 같은 `wr_content_t` 행을 `module_idx`로 구분하는 **3개 모듈**입니다.

```text
wr_content_t
 ├─ 고객 모듈 행
 ├─ 프로젝트 모듈 행
 └─ 사이트 모듈 행
```

원본 서비스 시트의 데이터는 세 모듈 행에 나누어 적재하되, 원본값 전체는 각 행의 `content_raw` JSON에 최대한 보존합니다.

## 문서

1. [3모듈 ERD와 필드 구조](docs/wr-content-erd.md)
2. [서비스 시트 → 3모듈 매핑](docs/service-sheet-api-field-mapping.md)
3. [공용 API 적재 규격](docs/doweb-content-structure.md)

## 공통 원칙

- 고객·프로젝트·사이트는 모두 `wr_content_t`의 행입니다.
- 고객 → 프로젝트는 `project.ref_idx = customer.idx`로 연결합니다.
- 프로젝트 → 사이트는 `site.parent_idx = project.idx`로 연결합니다.
- `content_raw`는 JSON 문자열로 저장하며, 원본 시트 데이터와 다중값·접속정보를 구조화해 담습니다.
- `tags`는 검색용 짧은 분류만 저장합니다.
- `content`는 사람이 읽는 검수메모·비고만 저장합니다.
