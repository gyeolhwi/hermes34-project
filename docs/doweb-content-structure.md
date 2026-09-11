# 우리기획 공용 API `wr_content_t` 적재 규격

## 구성 순서

모든 데이터는 `wr_content_t`에 저장하고 고객 → 프로젝트 → 사이트 순서로 연결합니다.

```text
고객 모듈 행
  idx = customer.idx

프로젝트 모듈 행
  parent_idx = customer.idx
  idx = project.idx

사이트 모듈 행
  parent_idx = project.idx
```

고객·프로젝트·사이트는 별도 테이블이 아니라 `module_idx`가 다른 `wr_content_t` 행입니다.

## 모듈별 핵심 필드

| 모듈 | 연결 필드 | 일반 필드 | `content_raw` 역할 |
|---|---|---|---|
| 고객 | — | `title`, `content` | 고객명 근거·연락처 `contact[]` |
| 프로젝트 | `parent_idx = customer.idx` | `title`, `status`, `type`, `date_start`, `date_end`, `tags`, `content` | 서비스ID 등 공용 필드에 없는 원본 식별값 |
| 사이트 | `parent_idx = project.idx` | `url`, `tags`, `content`, `receiver_idx` | 호스팅주소, 고객 연락처, 접속정보 |

## 필드 사용 기준

| 필드 | 사용 목적 |
|---|---|
| `module_idx` | 고객/프로젝트/사이트 모듈 구분 |
| `idx` | 생성된 행 식별자·다음 모듈 연결값 |
| `parent_idx` | 고객→프로젝트 또는 프로젝트→사이트 부모 행 연결 |
| `title` | 고객명 또는 서비스명 |
| `status` | 운영상태 |
| `type` | 서비스구분 |
| `date_start` | 개설일 또는 시작일 |
| `date_end` | 종료일; 원본 종료일이 있을 때만 사용 |
| `url` | 사이트 대표 도메인주소 |
| `tags` | 검색용 분류: `category_*`, `domain_*`, `hosting_*`, `frame_*` |
| `content` | 사람이 읽는 검수메모·비고 |
| `content_raw` | JSON 문자열. 공용·관계 필드에 없는 원본값, 다중값, 접속정보 |
| `receiver_idx` | 작업자 member `idx` |

## 사이트 `content_raw` 형태

사이트 행은 공용 필드로 이동하지 않은 원본값과 접속정보만 보존합니다.

```json
{
  "source": {
    "hosting_url": "G열 호스팅주소",
    "customer_contact": "O열 고객연락처",
    "customer_email": "P열 고객이메일"
  },
  "access": {
    "hosting": {"id": "H열", "password": "I열"},
    "admin": {"id": "J열", "password": "K열"},
    "database": {"url": "L열", "id": "M열", "password": "N열"}
  }
}
```

`status`, `type`, 날짜, 제목, 카테고리, 대표 도메인, 태그, 메모, 작업자 연결값은 이 JSON에 넣지 않습니다. 세 모듈의 실제 ERD와 행 예시는 [3모듈 ERD와 필드 구조](wr-content-erd.md)를 참조합니다.
