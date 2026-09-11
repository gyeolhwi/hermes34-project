# 제공 서비스 시트 → `wr_content_t` 3모듈 매핑

## 원본 기준

```text
우리기획_허비스_메인_통합본.xlsx
시트: 서비스_메인
범위: A1:W508
```

원본 서비스 시트 한 행은 고객·프로젝트·사이트 3개 모듈 행으로 정리합니다.

## 원본 열 매핑

| 열 | 원본 필드 | 최종 위치 | 중복 저장 금지 |
|---|---|---|---|
| A | 서비스ID | 프로젝트 `content_raw.source.service_id` | — |
| B | 운영상태 | 프로젝트 `status` | `content_raw` |
| C | 서비스명 | 프로젝트 `title` | `content_raw` |
| D | 카테고리 | 프로젝트 `tags: category_*` | `content_raw` |
| E | 구분 (개발/운영) | 사이트 `type` | `content_raw` |
| F~G | 도메인주소, 호스팅주소 | 사이트 `url`: `도메인주소, 호스팅주소` | `content_raw` |
| H~I | 호스팅 접속정보 | 사이트 `content_raw.access.hosting` | — |
| J~K | 관리자 접속정보 | 사이트 `content_raw.access.admin` | — |
| L~N | DB 접속정보 | 사이트 `content_raw.access.database` | — |
| O~P | 고객연락처, 고객이메일 | 사이트 원문; 고객 확정 후 고객 `content_raw.contact[]` | — |
| Q~S | 도메인등록업체, 호스팅사, 프레임워크 | 사이트 `tags` | `content_raw` |
| T~U | 검수메모, 비고 | 사이트 또는 프로젝트 `content` | `content_raw` |
| V | 작업자 | 사이트 `receiver_idx` (member 대조 후) | `content_raw` |
| W | 개설일 | 프로젝트 `date_start` | `content_raw` |

원본에 종료일 열은 없습니다. 기간 검색을 위해 프로젝트 `date_end`에는 기본값 `2999-12-31`을 적재합니다. 종료일 원본이 생기면 그 값을 우선합니다.

## 관계값

```text
customer.idx → project.parent_idx
project.idx  → site.parent_idx
member.idx   → site.receiver_idx
```

고객명 전용 열은 없으므로 고객 모듈은 고객명 매핑표가 확정된 경우에 생성합니다. 고객 `content_raw`에는 고객명 매핑 근거와 연락처 배열만 보존합니다.
