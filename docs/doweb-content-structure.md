# 우리기획 공용 API `wr_content_t` 적재 규격

## 구성 순서

```text
고객: idx = customer.idx
프로젝트: parent_idx = customer.idx, idx = project.idx
서비스: parent_idx = project.idx
```

## 모듈별 핵심 필드

| 모듈 | 연결/일반 필드 | `content_raw` |
|---|---|---|
| 고객 | `title`, `content` | 고객명 근거·연락처 |
| 프로젝트 | `parent_idx`, `title`, `status`, `date_start`, `date_end`, `tags`, `content` | 서비스ID |
| 서비스 | `parent_idx`, `type`, `url`, `tags`, `content`, `receiver_idx`, `is_hidden=1` | 고객 연락처·접속정보 |

## 필드 사용 기준

- 프로젝트 `status`는 `1=운영`, `-1=비운영`을 사용합니다.
- 프로젝트 `date_start`에는 개설일을, `date_end`에는 종료일 원본 또는 `2999-12-31`을 저장합니다.
- 서비스 `type`에는 `1=운영`, `2=개발`, `3=샘플`을 저장합니다.
- 서비스 `url`에는 `도메인주소, 호스팅주소`를 쉼표로 구분해 저장합니다.
- 공용·관계·검색 필드에 저장한 값은 `content_raw`에 넣지 않습니다. 검색이 불필요하거나 암호화 보관이 필요한 값만 넣습니다.
- 서비스 행은 `is_hidden=1`로 설정해 이 배포 환경의 DB 암호화 처리를 적용합니다.

## 서비스 `content_raw` 형태

```json
{
  "source": {"customer_contact":"O열 고객연락처", "customer_email":"P열 고객이메일"},
  "access": {
    "hosting":{"id":"H열","password":"I열"},
    "admin":{"id":"J열","password":"K열"},
    "database":{"url":"L열","id":"M열","password":"N열"}
  }
}
```

도메인주소, 호스팅주소, 구분 (개발/운영), 운영상태, 날짜, 제목, 카테고리, 태그, 메모, 작업자 연결값은 이 JSON에 넣지 않습니다.
