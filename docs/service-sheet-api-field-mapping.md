# 제공 서비스 시트 → `wr_content_t` 3모듈 매핑

## 원본 기준

```text
우리기획_허비스_메인_통합본.xlsx
시트: 서비스_메인
범위: A1:W508
```

원본 서비스 시트의 한 행은 고객·프로젝트·사이트 3개 모듈 행으로 정리합니다. 물리 테이블은 하나이며 모듈은 `module_idx`로 구분합니다.

## 원본 열 매핑

| 열 | 원본 필드 | 최종 위치 | 중복 저장 금지 |
|---|---|---|---|
| A | 서비스ID | 프로젝트 `content_raw.source.service_id` | — |
| B | 운영상태 | 프로젝트 `status` | `content_raw` |
| C | 서비스명 | 프로젝트 `title` | `content_raw` |
| D | 카테고리 | 프로젝트 `tags: category_*` | `content_raw` |
| E | 서비스구분 | 프로젝트 `type` | `content_raw` |
| F | 도메인주소 | 사이트 `url` | `content_raw` |
| G | 호스팅주소 | 사이트 `content_raw.source.hosting_url` | — |
| H~I | 호스팅 접속정보 | 사이트 `content_raw.access.hosting` | — |
| J~K | 관리자 접속정보 | 사이트 `content_raw.access.admin` | — |
| L~N | DB 접속정보 | 사이트 `content_raw.access.database` | — |
| O | 고객연락처 | 사이트 `content_raw.source.customer_contact`; 고객 확정 후 고객 `content_raw.contact[]` | — |
| P | 고객이메일 | 사이트 `content_raw.source.customer_email`; 고객 확정 후 고객 `content_raw.contact[]` | — |
| Q | 도메인등록업체 | 사이트 `tags: domain_*` | `content_raw` |
| R | 호스팅사 | 사이트 `tags: hosting_*` | `content_raw` |
| S | 프레임워크 | 사이트 `tags: frame_*` | `content_raw` |
| T | 검수메모 | 사이트 `content` | `content_raw` |
| U | 비고 | 사이트 또는 프로젝트 `content` | `content_raw` |
| V | 작업자 | 사이트 `receiver_idx` (member 대조 후) | `content_raw` |
| W | 개설일 | 프로젝트 `date_start` | `content_raw` |

원본에 종료일 열은 없습니다. `date_end`는 종료일 원본이 제공될 때만 적재하며, 단일 개설일을 임의로 복제하지 않습니다.

## 고객 모듈 입력

원본에 고객명 전용 열은 없습니다. 고객 모듈은 고객명 매핑표가 확정된 경우에 생성합니다.

| 고객 모듈 필드 | 값 |
|---|---|
| `title` | 확정된 고객명 |
| `content_raw.customer.name_source` | 고객명 매핑 근거 |
| `content_raw.contact[]` | O/P 원문을 담당자별로 정제한 연락처 배열 |

카테고리는 고객명이 아니라 프로젝트 검색 분류입니다.

## 관계값

```text
customer.idx → project.parent_idx
project.idx  → site.parent_idx
member.idx   → site.receiver_idx
```

정확한 JSON 형태와 ERD는 [3모듈 ERD와 필드 구조](wr-content-erd.md)를 기준으로 합니다.
