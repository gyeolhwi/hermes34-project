# 제공 서비스 시트 → 우리기획 공용 API 필드 매핑

## 참조한 원본 시트

이 문서는 사용자가 제공한 아래 엑셀 파일만 기준으로 작성했습니다.

```text
우리기획_허비스_메인_통합본.xlsx
시트: 서비스_메인
범위: A1:W508
```

> 이전에 참조한 `service-inventory.xlsx`는 사용자가 제공한 원본이 아니므로 이 문서의 기준에서 제외합니다.

이 파일은 **고객 마스터 시트가 아니라 서비스/사이트 단위 시트**입니다. `카테고리`는 고객명으로 사용하면 안 되는 고객 유형/분류 값입니다. 고객 행을 자동으로 만들 고객명·고객 묶음 규칙은 이 파일의 헤더만으로 확정할 수 없습니다.

## 원본 시트 필드 목록

| 열 | 원본 필드 | 공용 API 적재 위치 | 처리 기준 |
|---|---|---|---|
| A | 서비스ID | `content_raw.source_service_id` | 원본 행 식별자로 보존 |
| B | 운영상태 | `status` | API 상태 코드표 확정 뒤 변환 |
| C | 서비스명 | 프로젝트 `title` | 그대로 사용. 고객명과 혼동 금지 |
| D | 카테고리 | 프로젝트 `tags` | `category_*` 검색 태그 |
| E | 서비스구분 | 사이트 `type` | 실제/테스트/관리자 변환표 확정 필요 |
| F | 도메인주소 | 사이트 `url` | 공개 도메인/URL |
| G | 호스팅주소 | 사이트 `url` | 호스팅·서버 URL. F와 쉼표로 결합 |
| H | 접속아이디 | 사이트 `content_raw.access.hosting.id` | 원본값 보존 |
| I | 접속비밀번호 | 사이트 `content_raw.access.hosting.password` | 원본값 보존 |
| J | 관리자아이디 | 사이트 `content_raw.access.admin.id` | 원본값 보존 |
| K | 관리자비밀번호 | 사이트 `content_raw.access.admin.password` | 원본값 보존 |
| L | DB접속경로 | 사이트 `content_raw.access.database.url` | 원본값 보존 |
| M | DB아이디 | 사이트 `content_raw.access.database.id` | 원본값 보존 |
| N | DB비밀번호 | 사이트 `content_raw.access.database.password` | 원본값 보존 |
| O | 고객연락처 | 고객 `content_raw.contact[]` + 사이트 `content_raw.source.customer_contact` | 고객 미확정 상태에서도 원문 보존 |
| P | 고객이메일 | 고객 `content_raw.contact[]` + 사이트 `content_raw.source.customer_email` | 고객 미확정 상태에서도 원문 보존 |
| Q | 도메인등록업체 | 사이트 `tags` | `domain_*` |
| R | 호스팅사 | 사이트 `tags` | `hosting_*` |
| S | 프레임워크 | 사이트 `tags` | `frame_*` |
| T | 검수메모 | 사이트 `content` | 라벨을 유지한 일반 메모 |
| U | 비고 | 사이트 `content` | 라벨을 유지한 일반 메모 |
| V | 작업자 | 사이트 `receiver_idx` + `content_raw.source.operator` | member 대조 전에도 원문 보존 |
| W | 개설일 | 사이트 `content_raw.opened_at` | ISO 날짜로 정규화 |

## 한 서비스 행을 API에 넣는 구조

공용 API는 각 요청을 `wr_contents_t`의 컨텐츠 행으로 저장합니다. 현재 원본 한 행은 주로 **프로젝트 + 사이트** 정보입니다.

```text
서비스 시트 1행
  ├─ 프로젝트 컨텐츠 1건
  │   ├─ title     ← 서비스명(C)
  │   ├─ ref_idx   ← 확정된 고객 컨텐츠 idx
  │   └─ tags      ← 카테고리(D)
  └─ 사이트 컨텐츠 1건
      ├─ parent_idx  ← 프로젝트 컨텐츠 idx
      ├─ type        ← 서비스구분(E) 변환값
      ├─ url         ← 도메인주소(F), 호스팅주소(G)
      ├─ tags        ← 도메인등록업체(Q), 호스팅사(R), 프레임워크(S)
      ├─ content     ← 검수메모(T), 비고(U)
      └─ content_raw ← 서비스ID(A), 개설일(W)
```

## API payload 필드 매칭

### 고객 컨텐츠 — 생성 보류

고객 연락처는 O/P열에 있지만 고객명 전용 열이 없습니다. 따라서 고객 묶음 규칙을 정하기 전에는 고객 컨텐츠를 자동 생성하지 않습니다.

| API 필드 | 원본 열 | 처리 |
|---|---|---|
| `module_idx` | 고정 | 고객 정보 모듈 ID |
| `title` | 없음 | 고객명/고객 묶음 기준 필요 |
| `content_raw.contact[]` | O 고객연락처, P 고객이메일 | 검수 후 JSON화 |

```json
{
  "contact": [
    {
      "type": "phone",
      "name": "담당자명",
      "contact": "+821000000000"
    }
  ]
}
```

### 프로젝트 컨텐츠

| API 필드 | 원본 열 | 처리 |
|---|---|---|
| `module_idx` | 고정 | 프로젝트 정보 모듈 ID |
| `title` | C 서비스명 | 프로젝트/서비스 표시명 |
| `ref_idx` | 고객 생성 결과 | 고객 컨텐츠 `idx`; 자동 결정 금지 |
| `tags` | D 카테고리 | `category_church`, `category_company` 등으로 정규화 |
| `status` | B 운영상태 | 코드표 확정 후 변환 |
| `content_raw` | A 서비스ID | `{"source_service_id":"SVC-..."}` |

### 사이트 컨텐츠

| API 필드 | 원본 열 | 처리 |
|---|---|---|
| `module_idx` | 고정 | 사이트 정보 모듈 ID |
| `parent_idx` | 프로젝트 생성 결과 | 프로젝트 컨텐츠 `idx` |
| `type` | E 서비스구분 | 변환표 확정 필요 |
| `url` | F 도메인주소, G 호스팅주소 | 비어 있지 않은 값만 쉼표로 결합 |
| `tags` | Q/R/S | `domain_* hosting_* frame_*` |
| `receiver_idx` | V 작업자 | member 조회 결과의 `idx` |
| `content` | T 검수메모, U 비고 | 라벨을 유지해 합침 |
| `content_raw` | A 서비스ID, W 개설일 | 비검색 구조화 정보 |

```json
{
  "source_service_id": "SVC-000",
  "opened_at": "YYYY-MM-DD"
}
```

## H~N 접속·DB 정보 저장 방식

H~N 열도 누락하지 않고 사이트 행의 `content_raw.access` 객체에 저장합니다. `content_raw`는 공용 API에서 문자열로 받으므로 아래 JSON 전체를 직렬화해 저장합니다.

```json
{
  "access": {
    "hosting": {
      "id": "원본 H열 접속아이디",
      "password": "원본 I열 접속비밀번호"
    },
    "admin": {
      "id": "원본 J열 관리자아이디",
      "password": "원본 K열 관리자비밀번호"
    },
    "database": {
      "url": "원본 L열 DB접속경로",
      "id": "원본 M열 DB아이디",
      "password": "원본 N열 DB비밀번호"
    }
  }
}
```

접속정보는 검색 태그나 일반 메모가 아니므로 `tags`·`content`가 아닌 `content_raw`에만 넣습니다. 실제 이관 전에는 공용 API의 `content_raw` 접근권한·암호화 방식이 별도로 확인돼야 합니다.

## 원본값 전체 보존 원칙

원본 23개 열이 변환 과정에서 사라지지 않도록, 사이트 `content_raw.source`에 원문값을 함께 보존합니다. `title`, `url`, `tags`, `content`, `receiver_idx`는 빠른 조회를 위한 API 필드이고, `source`는 이관 근거입니다.

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

## 적재 전 확정할 항목

| 결정 항목 | 이유 |
|---|---|
| 고객명과 고객 묶음 규칙 | 고객명 전용 열이 없고, `카테고리`는 고객 유형임 |
| `실제`/`테스트`/`관리자` → 사이트 `type` | API 운영 환경 코드와 1:1 대응 미확정 |
| `운영`/`종료` → `status` | 공용 API 상태 코드표 확인 필요 |
| 작업자 이름 → `receiver_idx` | member의 실제 `idx` 대조 필요 |
| 중복 서비스 행 처리 | 서비스ID·도메인·서비스명 기준의 중복 검수 필요 |
