# 제공 서비스 시트 → `wr_content_t` 3모듈 매핑

## 원본 기준

```text
우리기획_허비스_메인_통합본.xlsx
시트: 서비스_메인
범위: A1:W508
```

원본 서비스 시트의 한 행은 `wr_content_t`에서 고객·프로젝트·사이트 **3개 모듈 행**으로 정리합니다. 물리 테이블은 하나이며, 모듈은 `module_idx`로 구분합니다.

## 원본 열 매핑

| 열 | 원본 필드 | 프로젝트 모듈 | 사이트 모듈 `content_raw.source/access` |
|---|---|---|---|
| A | 서비스ID | `content_raw.source.service_id` | `source.service_id` |
| B | 운영상태 | `content_raw.source.operation_status` | `source.operation_status` |
| C | 서비스명 | `title`, `content_raw.source.service_name` | `source.service_name` |
| D | 카테고리 | `tags: category_*`, `content_raw.source.category` | `source.category` |
| E | 서비스구분 | — | `source.service_kind`; API `type` 코드 확정 뒤 사용 |
| F | 도메인주소 | — | `url`, `source.domain_url` |
| G | 호스팅주소 | — | `url`, `source.hosting_url` |
| H | 접속아이디 | — | `access.hosting.id` |
| I | 접속비밀번호 | — | `access.hosting.password` |
| J | 관리자아이디 | — | `access.admin.id` |
| K | 관리자비밀번호 | — | `access.admin.password` |
| L | DB접속경로 | — | `access.database.url` |
| M | DB아이디 | — | `access.database.id` |
| N | DB비밀번호 | — | `access.database.password` |
| O | 고객연락처 | — | `source.customer_contact`; 고객 확정 후 고객 `contact[]` |
| P | 고객이메일 | — | `source.customer_email`; 고객 확정 후 고객 `contact[]` |
| Q | 도메인등록업체 | — | `tags: domain_*`, `source.domain_registrar` |
| R | 호스팅사 | — | `tags: hosting_*`, `source.hosting_provider` |
| S | 프레임워크 | — | `tags: frame_*`, `source.framework` |
| T | 검수메모 | — | `content` + `source.inspection_memo` |
| U | 비고 | `content` 필요 시 | `content` + `source.note` |
| V | 작업자 | — | `receiver_idx` + `source.operator` |
| W | 개설일 | `content_raw.source.opened_at` | `source.opened_at` |

## 고객 모듈 입력

원본에 고객명 전용 열은 없습니다. 따라서 고객 모듈은 고객명 매핑표가 확정된 경우에 생성합니다.

| 고객 모듈 필드 | 값 |
|---|---|
| `title` | 확정된 고객명 |
| `content_raw.customer.service_ids` | 해당 고객의 서비스ID 목록 |
| `content_raw.contact[]` | O/P 원문을 담당자별로 정제한 연락처 배열 |

`카테고리`는 고객명이 아니라 프로젝트 검색 분류입니다.

## 관계값

```text
customer.idx → project.ref_idx
project.idx  → site.parent_idx
member.idx   → site.receiver_idx
```

정확한 JSON 형태와 ERD는 [3모듈 ERD와 필드 구조](wr-content-erd.md)를 기준으로 합니다.
