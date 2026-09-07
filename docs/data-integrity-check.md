# 허비스 서비스 시트 → `wr_content_t` 정합성 점검

## 점검 대상

```text
우리기획_허비스_메인_통합본.xlsx
시트: 서비스_메인
범위: A1:W508
```

## 원본 시트 구조 점검 결과

| 항목 | 결과 |
|---|---:|
| 원본 헤더 수 | 23개 |
| 비어 있지 않은 데이터 행 | 507개 |
| 서비스ID(A) 빈 행 | 0개 |
| 서비스명(C) 빈 행 | 0개 |
| 중복 서비스ID 그룹 | 0개 |
| 중복 서비스ID 행 | 0개 |

이 결과는 **원본 시트 구조와 서비스ID 기준** 점검입니다. 고객명 매핑, API 상태코드, member 연결 여부는 API 적재 전 별도로 대조합니다.

## 23개 원본 열 보존 점검

| 범위 | 원본 열 | `wr_content_t` 최종 위치 | 결과 |
|---|---|---|---|
| 기본 | A~E | 프로젝트/사이트 `content_raw.source` | 보존 |
| 주소 | F~G | 사이트 `url` + `content_raw.source` | 보존 |
| 접속·DB | H~N | 사이트 `content_raw.access` | 보존 |
| 고객 연락처 | O~P | 사이트 `content_raw.source`, 고객 확정 후 고객 `content_raw.contact[]` | 보존 |
| 검색 분류 | Q~S | 사이트 `tags` + `content_raw.source` | 보존 |
| 메모·작업자·개설일 | T~W | 사이트 `content`, `receiver_idx`, `content_raw.source` | 보존 |

따라서 원본 A~W의 23개 열은 모두 사이트 모듈 `content_raw.source` 또는 `content_raw.access`에 원문 보존됩니다. 검색·관계에 필요한 값은 별도 API 필드에도 중복 배치합니다.

## 3모듈 관계 점검

```text
고객 모듈 행 (wr_content_t)
  idx = customer.idx
       ↓
프로젝트 모듈 행 (wr_content_t)
  ref_idx = customer.idx
  idx = project.idx
       ↓
사이트 모듈 행 (wr_content_t)
  parent_idx = project.idx
```

| 관계 | 검수 조건 |
|---|---|
| 고객 → 프로젝트 | 프로젝트 `ref_idx`가 동일 고객 모듈 행의 `idx`인지 |
| 프로젝트 → 사이트 | 사이트 `parent_idx`가 동일 프로젝트 모듈 행의 `idx`인지 |
| 작업자 → 사이트 | 작업자 이름이 member와 대조된 경우만 `receiver_idx`를 넣는지 |
| 원본 추적 | 프로젝트·사이트 `content_raw.source.service_id`가 원본 A열과 같은지 |
| JSON | 세 모듈의 `content_raw`가 직렬화 가능한 유효 JSON인지 |

## 적재 전 확인해야 할 값

| 항목 | 이유 | 원본값 보존 위치 |
|---|---|---|
| 고객명 → 고객 `title` | 원본에 고객명 전용 열 없음 | 사이트 `source.customer_contact`, `source.customer_email` |
| 운영상태 → `status` | 공용 API 상태 코드표 대조 필요 | `source.operation_status` |
| 서비스구분 → `type` | 공용 API type 코드표 대조 필요 | `source.service_kind` |
| 작업자 → `receiver_idx` | member의 실제 `idx` 대조 필요 | `source.operator` |

이 항목들은 연결/코드값이 확정되기 전에도 원본 데이터 자체는 사이트 `content_raw`에 저장되므로 누락되지 않습니다.

상세 모듈 구조는 [3모듈 ERD와 필드 구조](wr-content-erd.md), 열 단위 매핑은 [서비스 시트 → 3모듈 매핑](service-sheet-api-field-mapping.md)을 참조합니다.
