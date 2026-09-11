# Hermes34 → 우리기획 공용 API 적재 구조

## 핵심

Hermes34는 물리적으로 **`wr_content_t` 한 테이블**을 사용합니다. 고객·프로젝트·사이트는 별도 물리 테이블이 아니라 같은 행을 `module_idx`로 구분한 논리 모듈입니다.

```text
wr_content_t
 ├─ 고객 모듈 행
 ├─ 프로젝트 모듈 행
 └─ 사이트 모듈 행
```

원본 서비스 시트의 한 행은 세 모듈 행으로 나누어 적재합니다. 공용 필드에 저장한 값은 `content_raw`에 다시 넣지 않습니다.

## 문서

1. [3모듈 ERD와 필드 구조](docs/wr-content-erd.md)
2. [서비스 시트 → 3모듈 매핑](docs/service-sheet-api-field-mapping.md)
3. [원본 시트·3모듈 정합성 점검](docs/data-integrity-check.md)
4. [공용 API 적재 규격](docs/doweb-content-structure.md)

## 공통 원칙

- 고객·프로젝트·사이트는 모두 `wr_content_t` 행이며 `module_idx`로 구분합니다.
- 고객 → 프로젝트와 프로젝트 → 사이트 연결은 모두 자식 행의 `parent_idx`를 사용합니다.
- 운영상태·서비스구분·기간은 기존 `status`, `type`, `date_start`, `date_end` 필드에 저장합니다.
- `content_raw`는 공용/관계 필드에 없는 원본 식별값, 미구조화 보존값, 다중값, 접속정보만 JSON 문자열로 저장합니다.
- `tags`는 검색용 짧은 분류만, `content`는 사람이 읽는 검수메모·비고만 저장합니다.
