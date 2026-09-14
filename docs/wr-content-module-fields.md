# `wr_content_t` 모듈별 필드표

고객·프로젝트·서비스는 별도 물리 테이블이 아니라 `module_idx`가 다른 같은 `wr_content_t` 행입니다. 아래 표의 **필수**는 구조화 예시를 위한 기준이며, 실제 API의 필수성·코드값은 적재 전에 대조합니다.

## 고객 모듈 (`CUSTOMER_MODULE`)

| 필드 | 필수 | 용도 | 예시 | 중복 금지 / 비고 |
|---|---|---|---|---|
| `idx` | 생성 후 | 고객 행 식별자 | `customer-001` | 생성 결과를 프로젝트 `parent_idx`에 사용 |
| `module_idx` | 예 | 고객 모듈 ID | `customer-module-id` | 모듈 설정값 사용 |
| `title` | 예 | 확정된 고객명 | `예시 고객사` | 고객명 매핑 기준 확정 후 입력 |
| `content_raw` | 조건부 | 고객명 매핑 근거, 담당자 연락처 배열 | `{"customer":{"name_source":"..."},"contact":[]}` | `title`·메모를 중복하지 않음 |
| `content` | 아니오 | 고객 메모 | `고객 메모 예시` | 사람이 읽는 메모만 저장 |

## 프로젝트 모듈 (`PROJECT_MODULE`)

| 필드 | 필수 | 용도 | 예시 | 중복 금지 / 비고 |
|---|---|---|---|---|
| `idx` | 생성 후 | 프로젝트 행 식별자 | `project-001` | 서비스 `parent_idx`에 사용 |
| `module_idx` | 예 | 프로젝트 모듈 ID | `project-module-id` | 모듈 설정값 사용 |
| `parent_idx` | 예 | 부모 고객 `idx` | `customer-001` | 고객→프로젝트 연결 |
| `title` | 예 | 서비스/프로젝트명 | `예시 서비스` | JSON에 중복하지 않음 |
| `status` | 예 | 운영상태 | `운영` | 원본 B열, JSON에 중복하지 않음 |
| `date_start` | 예 | 개설일/시작일 | `2024-05-20` | 원본 W열 |
| `date_end` | 예 | 종료일/검색 상한 | `2999-12-31` | 종료일 원본이 없을 때 기본값 |
| `tags` | 아니오 | 카테고리 검색 태그 | `category_example` | 원본 D열의 검색용 정규화 값 |
| `content_raw` | 조건부 | 공용 필드에 없는 서비스ID | `{"source":{"service_id":"SVC-001"}}` | 상태·이름·날짜·태그 중복 금지 |
| `content` | 아니오 | 프로젝트 메모 | `프로젝트 메모 예시` | 사람이 읽는 메모만 저장 |

## 서비스 모듈 (`SERVICE_MODULE`)

| 필드 | 필수 | 용도 | 예시 | 중복 금지 / 비고 |
|---|---|---|---|---|
| `idx` | 생성 후 | 서비스 행 식별자 | `service-001` | 행 식별자 |
| `module_idx` | 예 | 서비스 모듈 ID | `service-module-id` | 모듈 설정값 사용 |
| `parent_idx` | 예 | 부모 프로젝트 `idx` | `project-001` | 프로젝트→서비스 연결 |
| `type` | 예 | 구분 (개발/운영) | `운영` | 원본 E열, JSON에 중복하지 않음 |
| `url` | 예 | 도메인주소와 호스팅주소 | `https://service.example.test, https://host.example.test` | 반드시 쉼표로 구분, JSON에 중복하지 않음 |
| `tags` | 아니오 | 도메인·호스팅·프레임워크 태그 | `domain_example hosting_example frame_example` | 원본 Q~S의 검색용 정규화 값 |
| `receiver_idx` | 조건부 | 대조된 작업자 member `idx` | `member-001` | 원본 V열; 대조 성공 시만 입력 |
| `content_raw` | 조건부 | 고객 연락처·이메일 원문, 접속·DB 정보 | `{"source":{},"access":{}}` | `type`, `url`, 태그, 메모, 작업자값 중복 금지 |
| `content` | 아니오 | 검수메모·비고 | `서비스 메모 예시` | 사람이 읽는 메모만 저장 |

## 연결 및 JSON 검증

1. 고객 행을 만든 뒤 반환된 `idx`를 프로젝트 `parent_idx`에 넣습니다.
2. 프로젝트 행을 만든 뒤 반환된 `idx`를 서비스 `parent_idx`에 넣습니다.
3. `content_raw`는 JSON **문자열**로 전송하고 각 행에서 파싱 가능한지 확인합니다.
4. 공용 필드로 저장한 값은 같은 의미의 `content_raw` 키로 다시 저장하지 않습니다.

CSV 예시는 [examples/wr_content_module_example.csv](../examples/wr_content_module_example.csv)를 참조합니다.
