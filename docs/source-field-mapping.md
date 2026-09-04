# 정규화 구조 ↔ DoWeb 운영 모듈 매핑

## 역할과 관계

| 구분 | 정규화 DB | DoWeb 운영 모듈 |
|---|---|---|
| 식별자 | 내부 `BIGINT IDENTITY` | 컨텐츠 `idx` UUID |
| 고객-프로젝트 | `projects.customer_id` | `projects.ref_idx = customer.idx` |
| 프로젝트-사이트 | `sites.project_id` | `sites.parent_idx = project.idx` |
| 사이트 담당자 | `sites.primary_receiver_id` | `sites.receiver_idx = member.idx` |
| 고객 연락처 | `customer_contacts` 행 | 고객 `content_raw.contact[]` JSON |
| 프로젝트 분류 | `projects.tags` | 프로젝트 `tags`의 `category_*` |
| 사이트 환경 | `sites.site_type` | 사이트 `type`: `production`/`development`/`staging`/`other` |
| 사이트 기술·호스팅 | `sites.tags` | 사이트 `tags`: `hosting_*`, `domain_*`, `frame_*`, `server_*` |
| URL | `site_endpoints` 행 | 사이트 `url` 쉼표 구분 문자열 |
| 접속계정 | `site_access_accounts` + `secret_ref` | 사이트 `content_raw.accounts[]` + `secret_ref` |

`CATEGORY_CONTENT`, `categories`, 프로젝트 `parent_idx` 카테고리 관계는 사용하지 않습니다. 기존 문서의 예시용 구조였으며, 현재 정한 운영 규격에서 프로젝트 카테고리는 검색 가능한 `tags`입니다.

## 모듈 ID의 위치

| 업무 | 값 | API 요청 위치 |
|---|---|---|
| 고객 | `01a05700-8c1d-7cd4-8b2d-fac77f865a9f` | `module_idx` |
| 프로젝트 | `01a05701-ed99-7cfa-841e-ec6f6c9922a0` | `module_idx` |
| 사이트 | `01a05702-067e-729b-85ab-deb5b0836082` | `module_idx` |

이 값은 관계 키가 아닙니다. 관계에는 API가 반환한 컨텐츠 `idx`를 씁니다.

## `tags`와 `content_raw` 구분

| 정보 성격 | 저장 위치 | 예 |
|---|---|---|
| 검색·필터·조합 검색할 분류 | `tags` | `category_maintenance`, `hosting_iwinv`, `frame_xe` |
| 프로젝트 분류 | 프로젝트 `tags` | `category_maintenance` |
| 사이트 운영 환경 | 사이트 `type` | `production`, `development` |
| 연락처·계정 참조 등 구조화된 비검색 보조정보 | `content_raw` JSON | `contact[]`, `accounts[].secret_ref` |
| 실제 비밀번호·토큰·개인키 | 제한 저장소만 | DB/API/Git/Slack 저장 금지 |

`tags`는 JSON이 아닙니다. 공백으로 구분한 문자열이며 태그 하나는 공백 없는 `접두어_값` 형식입니다.

## 입력 전 검수

- 고객 `content_raw`가 유효 JSON인지
- 프로젝트 `ref_idx`가 실제 고객 컨텐츠인지
- 사이트 `parent_idx`가 실제 프로젝트 컨텐츠인지
- 태그가 중복·공백·비정의 접두어 없이 입력됐는지
- 사이트 `type`이 운영 환경 코드인지
- `content_raw.accounts[]`에 실제 비밀값이 없고 `secret_ref`만 있는지
