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

이 결과는 원본 시트 구조와 서비스ID 기준 점검입니다. 고객명 매핑, API 코드값, member 연결 여부는 적재 전 별도로 대조합니다.

## 열별 보존·중복 방지 점검

| 범위 | 원본 열 | 최종 위치 | 검수 조건 |
|---|---|---|---|
| 식별 | A | 프로젝트 `content_raw.source.service_id` | 서비스ID가 원본과 동일 |
| 공용 필드 | B~E, W | 프로젝트 `status`, `title`, `tags`, `type`, `date_start` | 같은 의미의 JSON 키 없음 |
| 주소 | F | 사이트 `url` | 같은 의미의 JSON 키 없음 |
| 호스팅·접속 | G~N | 사이트 `content_raw.source.hosting_url`, `access` | 유효 JSON, 구조별 값 보존 |
| 고객 연락처 | O~P | 사이트 원문, 고객 확정 후 고객 `contact[]` | 고객명 매핑 전에도 값 보존 |
| 검색 분류 | Q~S | 사이트 `tags` | 같은 의미의 JSON 키 없음 |
| 메모·작업자 | T~V | `content`, `receiver_idx` | member 대조가 된 경우만 연결 |

원본에 종료일은 없으므로 `date_end`는 비워 둡니다. 종료일 원본이 추가되면 기간 검색을 위해 `date_end`에 적재합니다.

## 3모듈 관계 점검

```text
고객 모듈 행 (wr_content_t)
  idx = customer.idx
       ↓
프로젝트 모듈 행 (wr_content_t)
  parent_idx = customer.idx
  idx = project.idx
       ↓
사이트 모듈 행 (wr_content_t)
  parent_idx = project.idx
```

| 관계 | 검수 조건 |
|---|---|
| 고객 → 프로젝트 | 프로젝트 `parent_idx`가 동일 고객 모듈 행의 `idx`인지 |
| 프로젝트 → 사이트 | 사이트 `parent_idx`가 동일 프로젝트 모듈 행의 `idx`인지 |
| 작업자 → 사이트 | 작업자 이름이 member와 대조된 경우만 `receiver_idx`를 넣는지 |
| 원본 추적 | 프로젝트 `content_raw.source.service_id`가 원본 A열과 같은지 |
| 공용 필드 | `status`, `type`, `date_start`, `date_end`가 API 필드에 있는지 |
| JSON | 각 모듈의 `content_raw`가 직렬화 가능한 유효 JSON이며 공용 필드와 중복되지 않는지 |

## 적재 전 확인해야 할 값

| 항목 | 이유 | 처리 |
|---|---|---|
| 고객명 → 고객 `title` | 원본에 고객명 전용 열 없음 | 고객명 매핑 기준 확정 후 생성 |
| 운영상태 → `status` | 공용 API 상태 코드표 대조 필요 | 코드 대조 후 프로젝트 필드에 저장 |
| 서비스구분 → `type` | 공용 API type 코드표 대조 필요 | 코드 대조 후 프로젝트 필드에 저장 |
| 작업자 → `receiver_idx` | member의 실제 `idx` 대조 필요 | 대조 성공 시 사이트 필드에 저장 |

상세 모듈 구조는 [3모듈 ERD와 필드 구조](wr-content-erd.md), 열 단위 매핑은 [서비스 시트 → 3모듈 매핑](service-sheet-api-field-mapping.md)을 참조합니다.
