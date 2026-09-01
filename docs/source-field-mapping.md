# 기존 데이터베이스 필드 매핑 및 이관 규칙

## 제공된 데이터베이스 식별자

| 업무 영역 | 원본 데이터베이스 ID |
|---|---|
| 고객 정보 | `01a05700-8c1d-7cd4-8b2d-fac77f865a9f` |
| 프로젝트 정보 | `01a05701-ed99-7cfa-841e-ec6f6c9922a0` |
| 사이트 정보 | `01a05702-067e-729b-85ab-deb5b0836082` |

> ID는 원본 데이터베이스 참조용입니다. API 토큰·접속 비밀값은 이 저장소에 저장하지 않습니다.

## 고객 정보 매핑

| 원본 필드 | 정규화 대상 | 변환 규칙 |
|---|---|---|
| 고객명/제목 필드 | `customers.name` | 공백 정리, 필수 확인 |
| `content_raw.contact[]` | `customer_contacts` | 연락처 1개당 행 1개 생성 |

- 전화번호는 가능하면 E.164(`+82…`)로 정규화합니다.
- 동일 고객·동일 type·동일 value는 중복 후보로 보고합니다.
- 대표 연락처 기준이 없으면 자동 지정하지 않고 검수 목록으로 남깁니다.

## 프로젝트 정보 매핑

| 원본 필드 | 정규화 대상 | 변환 규칙 |
|---|---|---|
| `status` | `projects.status` | 상태 코드 표준화 필요 |
| `title` | `projects.title` | 서비스명 |
| `content` | `projects.memo` | 일반 메모만 보관 |
| `parent_idx` | `projects.category_id` | 숫자 참조를 `categories.id` 관계로 치환 |
| 고객 relation | `projects.customer_id` | 고객 연결이 없으면 검수 대상 |

## 사이트 정보 매핑

| 원본 필드 | 정규화 대상 | 변환 규칙 |
|---|---|---|
| `type` | `sites.type` | 표준 분류 값으로 대조 |
| `url` | `site_endpoints.url` | 쉼표 분리 후 주소별 1행 |
| `tags`의 `domain_*` | `providers` + endpoint 관계 | 도메인 등록업체 파싱 |
| `tags`의 `hosting_*` | `providers` + endpoint 관계 | 호스팅사 파싱 |
| `content` | `sites.inspection_memo` | 검수 메모·비고 |
| `receiver_idx` | `sites.primary_receiver_id` | 선행 `members` 등록 필수 |
| `content_raw.accounts[]` | `site_access_accounts` | 비밀값은 `secret_ref`로 교체 |

## 주소 역할 판별 규칙

| URL 형태/의미 | `endpoint_role` |
|---|---|
| 고객에게 공개되는 도메인 | `public_domain` |
| 서버/호스팅 접속 주소 | `hosting_endpoint` |
| CMS 관리자 주소 | `admin_url` |
| 개발·테스트 주소 | `staging` |
| 역할 미판별 | `unknown` + 검수 대상 |

하나의 원본 `url`에 여러 값이 들어 있으면 쉼표 기준으로 먼저 분리하고, URL의 역할은 자동 추측이 아닌 검수 규칙 또는 명시된 데이터로 확정합니다.

## 접속 계정 이관 보안 규칙

1. 원본 `pw`는 로그·Git·Issue·Slack·일반 DB에 기록하지 않습니다.
2. `id`도 운영상 불필요한 조회 화면에는 마스킹하며, 접근권한이 있는 서비스 계층에서만 사용합니다.
3. 대상 계정마다 Secret Vault 또는 제한 레코드의 `secret_ref`를 발급/연결합니다.
4. 이관 성공은 `secret_ref` 존재 여부와 읽기 전용 접속 검증 결과로만 기록합니다.
5. 원본 필드에 비밀값이 이미 있다면, 이전 완료 후 원본 보관/파기 정책을 별도 승인합니다.

## 이관 검수 산출물

- 고객/프로젝트/사이트별 원본 수와 이관 수 비교표
- 누락된 고객 관계, 작업자 관계, category 관계 목록
- 쉼표 URL 분리 결과 및 중복/비정상 URL 목록
- tag 파싱 불가 항목 목록
- `secret_ref` 미연결 계정 목록(비밀값 제외)
- 임의 표본의 읽기 전용 접속 검증 결과
