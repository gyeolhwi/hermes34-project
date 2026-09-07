# 허비스 서비스 시트 → `wr_contents_t` 저장 구조

## 기준과 전제

- 원본: 사용자가 제공한 `우리기획_허비스_메인_통합본.xlsx` / `서비스_메인` / A:W
- 저장 대상: 우리기획 공용 API가 저장하는 **`wr_contents_t`** 컨텐츠 행
- 고객·프로젝트·사이트별 신규 테이블을 만들지 않습니다.
- 공용 API를 통해 저장합니다. 여기서 말하는 행은 API 저장 결과인 `wr_contents_t` 행입니다.
- 실제 비밀번호·토큰·개인키는 원본에 있더라도 `wr_contents_t`에 저장하지 않습니다.

## 전체 구조

```text
원본 서비스 시트 1행 (서비스ID 기준)
  ├─ 고객 컨텐츠 행        : 고객명·고객 묶음 기준이 확정된 경우에만 생성
  ├─ 프로젝트 컨텐츠 행    : 서비스명·카테고리·원본 상태
  └─ 사이트 컨텐츠 행      : 도메인·호스팅·프레임워크·검수정보
```

모든 행은 같은 `wr_contents_t`에 저장하고 `module_idx`로 역할을 구분합니다.

| 컨텐츠 역할 | 저장 행 | 관계 |
|---|---|---|
| 고객 | 고객 정보 모듈의 행 | 고객이 확정된 경우에만 생성 |
| 프로젝트 | 프로젝트 정보 모듈의 행 | `ref_idx = customer.idx` |
| 사이트 | 사이트 정보 모듈의 행 | `parent_idx = project.idx` |

`idx`, `ref_idx`, `parent_idx`는 DB FK가 아니라 컨텐츠 행 `idx` 문자열을 참조하는 공용 API 관계 필드입니다.

## 1. 고객 컨텐츠 행

### 생성 조건

원본에는 `고객연락처`, `고객이메일`은 있지만 **고객명 전용 열이 없습니다.** `카테고리`는 `교회`, `기업` 같은 유형이므로 고객명으로 쓰지 않습니다.

따라서 고객 컨텐츠는 아래 중 하나가 확정된 경우에만 만듭니다.

1. 별도 고객 마스터에서 고객명·고객키를 제공하는 경우
2. 서비스ID별 고객명 매핑표를 제공하는 경우
3. 검수된 규칙으로 서비스명을 고객명으로 써도 되는 대상임이 확인된 경우

확정 전에는 고객 행을 억지로 생성하지 않고, 프로젝트·사이트 행에 원본 서비스ID를 남겨 후속 연결합니다.

### 저장 필드

| `wr_contents_t` 필드 | 값 | 원본 열 | 규칙 |
|---|---|---|---|
| `module_idx` | 고객 정보 모듈 ID | 고정 | 고객 역할 |
| `title` | 확정된 고객명 | 없음 | 카테고리 사용 금지 |
| `content_raw` | 연락처 JSON 문자열 | O, P | 아래 형식 |
| `content` | 고객 공통 메모 | 필요 시 | 일반 메모만 |

```json
{
  "contact": [
    {
      "type": "phone",
      "name": "담당자명",
      "contact": "+821000000000"
    },
    {
      "type": "email",
      "name": "담당자명",
      "contact": "manager@example.com"
    }
  ]
}
```

- O/P의 원문은 담당자별로 파싱·검수한 뒤 배열 객체로 만듭니다.
- JSON은 직렬화된 문자열로 `content_raw`에 저장합니다.
- 연락처 원문 전체를 메모로 중복 저장하지 않습니다.

## 2. 프로젝트 컨텐츠 행

원본의 **서비스ID 1개당 프로젝트 컨텐츠 1행**을 기본안으로 합니다. 중복·통합 서비스는 서비스ID를 기준으로 검수해 합칩니다.

| `wr_contents_t` 필드 | 값 | 원본 열 | 규칙 |
|---|---|---|---|
| `module_idx` | 프로젝트 정보 모듈 ID | 고정 | 프로젝트 역할 |
| `title` | 서비스명 | C | 표시명 |
| `ref_idx` | 고객 컨텐츠 `idx` | 고객 확정 후 | 미확정이면 임의값 금지 |
| `tags` | 카테고리 태그 | D | 공백 구분 문자열 |
| `status` | API 상태 코드 | B | 코드표 확인 전에는 원본값만 `content_raw`에 보존 |
| `content` | 프로젝트 수준 비고 | U 중 프로젝트 공통분 | 일반 텍스트 |
| `content_raw` | 원본 추적 JSON | A, B, W | 아래 형식 |

```json
{
  "source_service_id": "SVC-000",
  "source_operation_status": "운영",
  "opened_at": "YYYY-MM-DD"
}
```

### 프로젝트 `tags`

```text
category_church
```

- 태그는 JSON이 아니라 공백 구분 문자열입니다.
- D `카테고리`는 고객명이 아니라 **프로젝트 검색 분류**입니다.
- 값은 `category_church`, `category_company`처럼 표준화합니다.

## 3. 사이트 컨텐츠 행

원본 서비스ID 하나에 공개 도메인/호스팅 주소가 함께 있으므로, 기본안은 **서비스ID 1개당 사이트 컨텐츠 1행**입니다. 서로 독립 운영되는 도메인이 한 서비스ID에 여러 개라고 확인되면 사이트 행을 나누고 같은 프로젝트 `idx`를 `parent_idx`에 넣습니다.

| `wr_contents_t` 필드 | 값 | 원본 열 | 규칙 |
|---|---|---|---|
| `module_idx` | 사이트 정보 모듈 ID | 고정 | 사이트 역할 |
| `parent_idx` | 프로젝트 컨텐츠 `idx` | 프로젝트 생성 결과 | 필수 관계 |
| `type` | API 사이트 유형 코드 | E | 코드표 확인 전 임의 문자열 저장 금지 |
| `url` | 도메인·호스팅 주소 | F, G | 빈값 제외, 쉼표로 연결 |
| `tags` | 도메인·호스팅·프레임워크 태그 | Q, R, S | 공백 구분 문자열 |
| `receiver_idx` | 작업자 member `idx` | V | 이름이 정확히 일치할 때만 |
| `content` | 검수메모 + 비고 | T, U | 라벨을 유지해 합침 |
| `content_raw` | 원본 추적 JSON | A, B, E, W | 아래 형식 |

```json
{
  "source_service_id": "SVC-000",
  "source_operation_status": "운영",
  "source_service_kind": "실제",
  "opened_at": "YYYY-MM-DD"
}
```

### 사이트 `url`

```text
https://public.example.com,https://host.example.net
```

- F 도메인주소가 있으면 먼저 넣습니다.
- G 호스팅주소가 있으면 뒤에 넣습니다.
- 비어 있는 값, 비밀 URL, 관리자 비밀번호가 포함된 URL은 제외합니다.

### 사이트 `tags`

```text
domain_gabia hosting_iwinv frame_xe
```

| 원본 열 | 태그 접두어 | 예 |
|---|---|---|
| Q 도메인등록업체 | `domain_` | `domain_gabia` |
| R 호스팅사 | `hosting_` | `hosting_iwinv` |
| S 프레임워크 | `frame_` | `frame_xe` |

태그는 검색용 정보만 넣습니다. `tags`에 원문 메모, 연락처, 비밀값을 넣지 않습니다.

## 원본 열별 최종 처리표

| 원본 열 | `wr_contents_t` 처리 |
|---|---|
| A 서비스ID | 프로젝트·사이트 `content_raw.source_service_id` |
| B 운영상태 | 원본값은 `content_raw.source_operation_status`; `status`는 API 코드표 확정 후 |
| C 서비스명 | 프로젝트 `title` |
| D 카테고리 | 프로젝트 `tags`의 `category_*` |
| E 서비스구분 | 원본값은 사이트 `content_raw.source_service_kind`; `type`은 API 코드표 확정 후 |
| F 도메인주소 | 사이트 `url` |
| G 호스팅주소 | 사이트 `url` |
| H~N 접속·DB 정보 | 제한 저장소로 분리; `wr_contents_t`에는 실제 값 미저장 |
| O 고객연락처 | 고객 `content_raw.contact[]` (고객 확정 후) |
| P 고객이메일 | 고객 `content_raw.contact[]` (고객 확정 후) |
| Q 도메인등록업체 | 사이트 `tags`의 `domain_*` |
| R 호스팅사 | 사이트 `tags`의 `hosting_*` |
| S 프레임워크 | 사이트 `tags`의 `frame_*` |
| T 검수메모 | 사이트 `content` |
| U 비고 | 사이트 `content` 또는 프로젝트 공통 메모 |
| V 작업자 | member 대조 후 사이트 `receiver_idx` |
| W 개설일 | 프로젝트·사이트 `content_raw.opened_at` |

## 예시: 엑셀 한 행이 `wr_contents_t`에 저장되는 모습

아래는 **설명용 가상 값**입니다. 실제 고객 연락처·접속정보·비밀번호는 포함하지 않습니다.

### 1) 원본 엑셀의 한 행

| 원본 열 | 예시값 |
|---|---|
| A 서비스ID | `SVC-201` |
| B 운영상태 | `운영` |
| C 서비스명 | `샘플교회 홈페이지` |
| D 카테고리 | `교회` |
| E 서비스구분 | `실제` |
| F 도메인주소 | `samplechurch.example.kr` |
| G 호스팅주소 | `samplechurch.iwinv.net` |
| O 고객연락처 | `김담당: 010-0000-0000` |
| P 고객이메일 | `manager@samplechurch.example.kr` |
| Q 도메인등록업체 | `가비아` |
| R 호스팅사 | `iwinv` |
| S 프레임워크 | `XE` |
| T 검수메모 | `메인 페이지 점검 완료` |
| U 비고 | `관리자 URL은 별도 확인 필요` |
| V 작업자 | `홍작업자` |
| W 개설일 | `2024-05-20` |

H~N의 접속·DB 정보는 이 예시와 API payload에서 의도적으로 제외합니다.

### 2) 고객 컨텐츠 행 — 고객명이 확정된 경우만

고객명 매핑으로 `샘플교회`가 확정됐다고 가정합니다. 고객 생성 API 응답의 `idx`는 이후 프로젝트 연결에 사용합니다.

```json
{
  "module_idx": "01a05700-8c1d-7cd4-8b2d-fac77f865a9f",
  "title": "샘플교회",
  "content_raw": "{\"contact\":[{\"type\":\"phone\",\"name\":\"김담당\",\"contact\":\"+821000000000\"},{\"type\":\"email\",\"name\":\"김담당\",\"contact\":\"manager@samplechurch.example.kr\"}]}",
  "content": ""
}
```

```text
API 생성 응답: customer.idx = "customer-uuid-001"
```

### 3) 프로젝트 컨텐츠 행

프로젝트는 서비스명(C)을 `title`로 쓰고, 고객이 확정됐으므로 `ref_idx`에 방금 받은 고객 `idx`를 넣습니다. B `운영`은 API 상태 코드가 아직 확정되지 않았으므로 `status`에 추측값을 넣지 않고 원본 그대로 `content_raw`에 보존합니다.

```json
{
  "module_idx": "01a05701-ed99-7cfa-841e-ec6f6c9922a0",
  "title": "샘플교회 홈페이지",
  "ref_idx": "customer-uuid-001",
  "tags": "category_church",
  "content": "",
  "content_raw": "{\"source_service_id\":\"SVC-201\",\"source_operation_status\":\"운영\",\"opened_at\":\"2024-05-20\"}"
}
```

```text
API 생성 응답: project.idx = "project-uuid-001"
```

### 4) 사이트 컨텐츠 행

사이트는 프로젝트 `idx`를 `parent_idx`로 연결합니다. E `실제`도 API `type` 코드가 확정되기 전까지는 `content_raw`에 원본값으로 남기고, `type`에는 임의 문자열을 넣지 않습니다.

```json
{
  "module_idx": "01a05702-067e-729b-85ab-deb5b0836082",
  "parent_idx": "project-uuid-001",
  "url": "https://samplechurch.example.kr,https://samplechurch.iwinv.net",
  "tags": "domain_gabia hosting_iwinv frame_xe",
  "receiver_idx": "member-uuid-001",
  "content": "[검수메모] 메인 페이지 점검 완료\n\n[비고] 관리자 URL은 별도 확인 필요",
  "content_raw": "{\"source_service_id\":\"SVC-201\",\"source_operation_status\":\"운영\",\"source_service_kind\":\"실제\",\"opened_at\":\"2024-05-20\"}"
}
```

`member-uuid-001`은 V 작업자 `홍작업자`가 실제 member 목록에서 확인된 경우에만 넣습니다. 확인되지 않으면 `receiver_idx`는 넣지 않습니다.

### 5) 최종적으로 보이는 `wr_contents_t` 행 관계

```text
[고객 모듈 행]
idx       = customer-uuid-001
title     = 샘플교회

[프로젝트 모듈 행]
idx       = project-uuid-001
ref_idx   = customer-uuid-001
title     = 샘플교회 홈페이지
tags      = category_church

[사이트 모듈 행]
parent_idx = project-uuid-001
url        = https://samplechurch.example.kr,https://samplechurch.iwinv.net
tags       = domain_gabia hosting_iwinv frame_xe
```

## 적재 순서와 검수 기준

1. 서비스ID 중복·서비스명·도메인 중복을 먼저 검수합니다.
2. 고객명 매핑이 확정된 대상만 고객 컨텐츠를 생성하고 `customer.idx`를 확보합니다.
3. 프로젝트 컨텐츠를 생성합니다. 고객이 확정된 대상만 `ref_idx = customer.idx`를 넣습니다.
4. 사이트 컨텐츠를 생성하고 `parent_idx = project.idx`를 넣습니다.
5. 작업자 이름을 member `idx`와 대조한 경우에만 `receiver_idx`를 넣습니다.
6. API 응답의 `idx`와 원본 `source_service_id`를 이관 결과표에 기록합니다.
7. API 목록 조회로 생성된 행의 `module_idx`, 관계값, `content_raw` JSON, 태그를 다시 대조합니다.

## 아직 확정이 필요한 API 값

| 항목 | 현재 방침 |
|---|---|
| `status` 값 | B 운영상태를 무작정 넣지 않음. 공용 API 상태 코드표 확인 후 변환 |
| 사이트 `type` 값 | E 서비스구분을 무작정 넣지 않음. 공용 API type 코드표 확인 후 변환 |
| 고객명/고객 묶음 | 별도 고객 마스터 또는 서비스ID별 매핑표가 있어야 자동 적재 |
| 작업자 `receiver_idx` | member 목록의 실제 `idx` 확인 후 입력 |

이 네 항목은 데이터 손실을 피하기 위해 원본값을 `content_raw`에 보존하고, API 코드·관계값은 확인 뒤 채웁니다.
