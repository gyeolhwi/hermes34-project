# 이상적 정규화 구조 ↔ DoWeb 기존 모듈 매핑

## 두 구조의 역할

| 구분 | 이상적 정규화 구조 | DoWeb 기존 모듈 구조 |
|---|---|---|
| 목적 | 장기 운영 DB / 엄격한 검색·관계·감사 | 이미 생성된 모듈을 이용한 즉시 운영 |
| 식별자 | 내부 `BIGINT IDENTITY` | DoWeb 컨텐츠 `idx` UUID |
| 고객-프로젝트 | `projects.customer_id` | 프로젝트 `ref_idx = customer.idx` |
| 프로젝트-카테고리 | `projects.category_id` | 프로젝트 `parent_idx = category.idx` |
| 프로젝트-사이트 | `sites.project_id` | 사이트 `parent_idx = project.idx` |
| 담당자 | `sites.primary_receiver_id` | 사이트 `receiver_idx = member.idx` |
| 연락처 | `customer_contacts` 행 | 고객 `content_raw.contact[]` JSON |
| URL | `site_endpoints` 행 | 사이트 `url` 쉼표 분리 문자열 |
| 도메인/호스팅사 | `providers` 관계 | 사이트 `tags`: `domain_*`, `hosting_*` |
| 접속계정 | `site_access_accounts` + `secret_ref` | 사이트 `content_raw.accounts[]` + `secret_ref` |

## 제공된 모듈 ID의 올바른 위치

| 업무 | 값 | DoWeb 요청에서의 위치 |
|---|---|---|
| 고객 | `01a05700-8c1d-7cd4-8b2d-fac77f865a9f` | `module_idx` |
| 프로젝트 | `01a05701-ed99-7cfa-841e-ec6f6c9922a0` | `module_idx` |
| 사이트 | `01a05702-067e-729b-85ab-deb5b0836082` | `module_idx` |

이 값은 행의 `idx`나 관계용 FK가 아닙니다. 고객·프로젝트·사이트를 생성한 뒤 서버가 반환하는 각 컨텐츠의 `idx`가 관계 키가 됩니다.

## 필드별 매핑

| 업무 | 사용자 요구 필드 | DoWeb 호환 저장 | 이상적 정규화 저장 |
|---|---|---|---|
| 고객 연락처 | `content_raw.contact[]` | `content_raw.contact[]` JSON | `customer_contacts` |
| 프로젝트 상태 | `status` | `status` | `projects.status` |
| 서비스명 | `title` | `title` | `projects.title` |
| 프로젝트 메모 | `content` | `content` | `projects.memo` |
| 프로젝트 카테고리 | `parent_idx` | `parent_idx = category.idx` | `projects.category_id` |
| 프로젝트 고객 | 신규 필요 | `ref_idx = customer.idx` | `projects.customer_id` |
| 사이트 구분 | `type` | `type` | `sites.type` |
| 주소 | `url` | 쉼표 구분 문자열 | `site_endpoints` |
| 계정 | `content_raw.accounts` | JSON + `secret_ref` | `site_access_accounts` + `secret_ref` |
| 도메인 업체 | `tags` | `domain_*` | `providers` |
| 호스팅사 | `tags` | `hosting_*` | `providers` |
| 검수 메모 | `content` | `content` | `sites.inspection_memo` |
| 작업자 | `receiver_idx` | `receiver_idx = member.idx` | `sites.primary_receiver_id` |

## 데이터 입력 전 검수

- 고객 `title` 중복 여부
- `content_raw`가 유효 JSON인지
- 프로젝트 `ref_idx`가 실제 고객 컨텐츠인지
- 프로젝트 `parent_idx`가 실제 카테고리 컨텐츠인지
- 사이트 `parent_idx`가 실제 프로젝트 컨텐츠인지
- 사이트 `receiver_idx`가 실제 member인지
- `url`의 쉼표 분리값이 유효 URL인지
- `tags`가 공백 구분이며 `domain_`/`hosting_` 접두어를 따르는지
- 계정 JSON에 실제 비밀번호·토큰·개인키가 없는지, `secret_ref`가 있는지

## 금지 사항

1. 제공된 `module_idx`를 `parent_idx`, `ref_idx`, `receiver_idx`에 넣지 않습니다.
2. 실제 비밀번호를 `content_raw`, `content`, `tags`, Git, Slack, Issue에 저장하지 않습니다.
3. 고객 관계를 `parent_idx`에 넣지 않습니다. 프로젝트의 `parent_idx`는 카테고리이므로 고객은 `ref_idx`를 사용합니다.
4. 사이트가 어느 프로젝트에도 연결되지 않은 상태로 생성되지 않게 합니다.
