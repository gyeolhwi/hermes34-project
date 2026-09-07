# 우리기획 공용 API `wr_content_t` 적재 규격

## 구성 순서

모든 데이터는 `wr_content_t`에 저장하고, **고객 → 프로젝트 → 사이트** 순서로 연결합니다.

```text
고객 모듈 행
  idx = customer.idx

프로젝트 모듈 행
  ref_idx = customer.idx
  idx = project.idx

사이트 모듈 행
  parent_idx = project.idx
```

고객·프로젝트·사이트는 별도 테이블이 아니라 `module_idx`가 다른 `wr_content_t` 행입니다.

## 모듈별 핵심 필드

| 모듈 | 연결 필드 | 일반 필드 | `content_raw` 역할 |
|---|---|---|---|
| 고객 | — | `title` 고객명 | 고객 원본·연락처 `contact[]` |
| 프로젝트 | `ref_idx = customer.idx` | `title`, `tags`, `content` | 서비스ID·카테고리·운영상태·개설일 |
| 사이트 | `parent_idx = project.idx` | `url`, `tags`, `content`, `receiver_idx` | 원본 서비스 시트 A~W 전체 |

## 필드 사용 기준

| 필드 | 사용 목적 |
|---|---|
| `module_idx` | 고객/프로젝트/사이트 모듈 구분 |
| `idx` | 생성된 행 식별자·다음 모듈 연결값 |
| `ref_idx` | 프로젝트가 고객을 가리킴 |
| `parent_idx` | 사이트가 프로젝트를 가리킴 |
| `title` | 고객명 또는 서비스명 |
| `url` | 사이트 도메인주소·호스팅주소 |
| `tags` | 검색용 분류: `category_*`, `domain_*`, `hosting_*`, `frame_*` |
| `content` | 사람이 읽는 검수메모·비고 |
| `content_raw` | JSON 문자열. 원본값 전체와 다중값·접속정보 구조화 |
| `receiver_idx` | 작업자 member `idx` |

## 사이트 `content_raw` 최종 형태

사이트 행은 원본 서비스 시트 값 전체를 아래 구조로 보존합니다.

```json
{
  "source": {
    "service_id": "A열 서비스ID",
    "operation_status": "B열 운영상태",
    "service_name": "C열 서비스명",
    "category": "D열 카테고리",
    "service_kind": "E열 서비스구분",
    "domain_url": "F열 도메인주소",
    "hosting_url": "G열 호스팅주소",
    "customer_contact": "O열 고객연락처",
    "customer_email": "P열 고객이메일",
    "domain_registrar": "Q열 도메인등록업체",
    "hosting_provider": "R열 호스팅사",
    "framework": "S열 프레임워크",
    "inspection_memo": "T열 검수메모",
    "note": "U열 비고",
    "operator": "V열 작업자",
    "opened_at": "W열 개설일"
  },
  "access": {
    "hosting": {"id": "H열", "password": "I열"},
    "admin": {"id": "J열", "password": "K열"},
    "database": {"url": "L열", "id": "M열", "password": "N열"}
  }
}
```

세 모듈의 실제 ERD와 행 예시는 [3모듈 ERD와 필드 구조](wr-content-erd.md)를 참조합니다.
