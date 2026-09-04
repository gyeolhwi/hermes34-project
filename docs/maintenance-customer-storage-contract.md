# 유지보수 고객 저장 계약

## 적용 범위

Hermes34는 **정규화 DB**를 유지보수 고객의 조회·수정 기준으로 사용하고, 우리기획 DoWeb 고객 모듈에는 공용 API 호환용 `content_raw`를 저장합니다. 두 저장소의 ID 역할은 다릅니다.

- 내부 DB: `customers.id`와 `customer_contacts.id`를 사용합니다.
- DoWeb: 고객 컨텐츠 생성 뒤 반환된 `idx`를 `customers.source_content_idx`에 유일하게 보관합니다.
- DoWeb 고객 모듈 ID는 API 요청의 `module_idx`일 뿐 관계 키나 내부 PK가 아닙니다.

## 고객 연락처 API 계약

DoWeb API의 `content_raw`는 **문자열** 필드입니다. 아래 JSON을 한 번 직렬화하여 고객 컨텐츠의 `content_raw`에 저장합니다.

```json
{
  "contact": [
    {
      "type": "phone",
      "name": "이름",
      "contact": "+821000000000"
    },
    {
      "type": "email",
      "name": "운영 담당",
      "contact": "ops@example.com"
    }
  ]
}
```

각 배열 원소는 반드시 객체여야 합니다. 질문에 제시된 배열 내부의 `"type": ...`만 있는 형태는 JSON 객체 중괄호가 없어 유효하지 않습니다.

| API JSON 키 | DB 컬럼 | 규칙 |
|---|---|---|
| `contact[].type` | `customer_contacts.contact_type` | `phone`, `email`, `kakao`, `other`만 허용 |
| `contact[].name` | `customer_contacts.contact_name` | 없으면 JSON에서 키를 생략할 수 있음 |
| `contact[].contact` | `customer_contacts.contact_value` | 빈값 금지; 전화는 E.164 `+8210…` 형식 |
| 배열 순서 | `sort_order` | 작은 값이 먼저. 대표 연락처가 먼저 오도록 직렬화 |
| 대표 여부 | `is_primary` | API에는 별도 키를 추가하지 않음; 고객별 활성 대표 1건만 허용 |
| 사용 여부 | `is_active` | 비활성 행은 API `content_raw`에서 제외 |

`content_raw.contact[]`는 고객의 활성 연락처를 `is_primary DESC, sort_order ASC, id ASC` 순서로 직렬화한 호환 표현입니다. 검색·중복 방지·대표 연락처·비활성화는 모두 `customer_contacts` 테이블에서 처리합니다.

## 저장·갱신 절차

1. 고객명을 `customers.name`에 만들거나 갱신합니다. 기존 DoWeb 고객이면 반환된 `idx`를 `source_content_idx`에 연결합니다.
2. 수신한 연락처마다 `customer_contacts`에 한 행을 upsert합니다. `(customer_id, contact_type, contact_value)`는 중복 저장하지 않습니다.
3. 전화번호는 입력 시 E.164로 정규화합니다. 대표 연락처를 바꾸면 같은 고객의 기존 활성 대표을 해제한 뒤 새 행을 대표로 지정합니다.
4. 활성 연락처만 규정 JSON으로 직렬화해 DoWeb 고객 컨텐츠의 `content_raw`를 생성/수정합니다. API에는 고객 모듈 ID를 `module_idx`로, 고객 컨텐츠 ID를 수정 대상 `idx`로 사용합니다.
5. DoWeb API 성공 후 `source_content_idx`와 동기화 시각을 운영 로그에 남깁니다. 실패 시 DB의 연락처는 유지하고, API 재시도 대상만 별도로 처리합니다. 실패를 성공으로 표시하지 않습니다.

## 비밀정보 경계

연락처는 업무상 필요한 개인정보이므로 권한 있는 유지보수 운영자만 조회합니다. 비밀번호, 토큰, 개인키는 `content_raw`, `content`, DB 일반 컬럼, Git, Slack, Issue에 저장하지 않습니다. 사이트 접속계정은 `site_access_accounts.secret_ref`로 제한 저장소의 비밀값만 참조합니다.

## 테이블 구현

PostgreSQL용 실제 DDL은 [`sql/001_customer_maintenance_schema.sql`](../sql/001_customer_maintenance_schema.sql)에 있습니다. 이 스키마는 고객 → 프로젝트 → 사이트와 연락처·주소·접속계정의 다중값 관계 및 제약조건을 포함합니다.
