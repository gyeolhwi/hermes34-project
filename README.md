# Hermes34 → 우리기획 공용 API 적재 구조

## 핵심

Hermes34는 물리적으로 **`wr_content_t` 한 테이블**을 사용합니다. 고객·프로젝트·서비스는 같은 행을 `module_idx`로 구분한 논리 모듈입니다. 원본 서비스 시트의 한 행은 세 모듈 행으로 나누어 적재하며, 공용 필드에 저장한 값은 `content_raw`에 다시 넣지 않습니다.

## 문서

1. [3모듈 ERD와 필드 구조](docs/wr-content-erd.md)
2. [서비스 시트 → 3모듈 매핑](docs/service-sheet-api-field-mapping.md)
3. [원본 시트·3모듈 정합성 점검](docs/data-integrity-check.md)
4. [공용 API 적재 규격](docs/doweb-content-structure.md)

## 공통 원칙

- 고객 → 프로젝트와 프로젝트 → 서비스 연결은 자식 행의 `parent_idx`를 사용합니다.
- 프로젝트에는 운영상태와 기간을 `status`, `date_start`, `date_end`로 저장합니다. 종료일 원본이 없으면 `date_end=2999-12-31`을 사용합니다.
- 서비스에는 `구분 (개발/운영)`을 `type`으로 저장하고, 도메인주소와 호스팅주소를 `url`에 쉼표로 구분해 저장합니다.
- `content_raw`는 공용/관계 필드에 없는 원본 식별값, 다중값, 접속정보만 JSON 문자열로 저장합니다.
- `tags`는 검색용 짧은 분류만, `content`는 사람이 읽는 검수메모·비고만 저장합니다.
