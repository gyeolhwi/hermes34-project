# Hermes34 고객시트 → DoWeb `wr_contents_t` 적재 규격

## 핵심

실제 서비스 시트의 열별 적재 여부와 API 필드 매핑은 [서비스 시트 → 공용 API 필드 매핑](service-sheet-api-field-mapping.md)을 먼저 봅니다.

Hermes34 고객시트를 우리기획 공용 API로 이관할 때 **별도의 `customers`, `projects`, `sites`, `customer_contacts` 같은 정규화 테이블을 만들거나 서로 FK로 엮지 않습니다.**

공용 API가 받는 컨텐츠 한 건이 DoWeb의 공용 컨텐츠 테이블 **`wr_contents_t`의 한 행**으로 저장됩니다. 고객·프로젝트·사이트는 물리 테이블이 아니라 `module_idx`로 구분하는 논리적인 컨텐츠 종류입니다.

```text
고객시트 행/정보
  → 공용 API의 contents 생성·수정 요청
    → wr_contents_t 행 1건 저장
```

> 운영 데이터 입력은 공용 API를 사용합니다. API를 우회해 DB에 직접 INSERT하는 것은 API의 검증·권한·후처리 규칙을 건너뛸 수 있으므로 이 문서는 API 요청 payload 기준으로 설명합니다.

## 공용 컨텐츠 종류

| 논리 종류 | `module_idx` | `wr_contents_t`에 저장되는 한 행의 의미 |
|---|---|---|
| 고객 정보 | `01a05700-8c1d-7cd4-8b2d-fac77f865a9f` | 고객사/기관 1건 |
| 프로젝트 정보 | `01a05701-ed99-7cfa-841e-ec6f6c9922a0` | 고객의 서비스/유지보수 프로젝트 1건 |
| 사이트 정보 | `01a05702-067e-729b-85ab-deb5b0836082` | 프로젝트에 속한 운영 대상 사이트 1건 |

- `module_idx`는 컨텐츠 종류를 구분하는 값입니다.
- API가 생성 후 반환하는 `idx`가 해당 `wr_contents_t` 행의 식별자입니다.
- 아래 관계도 DB FK가 아니라, 같은 `wr_contents_t` 행끼리 `idx` 문자열을 참조하는 운영 규칙입니다.

## 연결 방식

```text
[고객 행]      idx = customer.idx
   └─ [프로젝트 행]  ref_idx = customer.idx
        └─ [사이트 행] parent_idx = project.idx
```

| 연결 목적 | 저장 필드 | 넣는 값 |
|---|---|---|
| 프로젝트 → 고객 | 프로젝트 `ref_idx` | 고객 컨텐츠의 `idx` |
| 사이트 → 프로젝트 | 사이트 `parent_idx` | 프로젝트 컨텐츠의 `idx` |
| 사이트 → 담당자 | 사이트 `receiver_idx` | member의 `idx` |

`CATEGORY_CONTENT`나 별도 카테고리 테이블은 만들지 않습니다.

## 1. 고객 행

고객시트의 고객 1건을 고객 모듈의 컨텐츠 1건으로 저장합니다.

| API 필드 | 저장 내용 |
|---|---|
| `module_idx` | 고객 정보 모듈 ID |
| `title` | 고객사/기관명 |
| `content_raw` | 연락처 JSON을 직렬화한 문자열 |
| `content` | 고객 공통 메모 |
| `status` | 고객 상태를 실제로 사용할 때만 지정 |

### 고객 `content_raw`

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

- 연락처가 여러 개면 `contact` 배열에 객체를 추가합니다.
- `content_raw`는 **문자열 필드에 JSON을 직렬화하여** 넣습니다.
- 이 JSON 자체가 `wr_contents_t.content_raw`의 값입니다. 연락처를 별도 `customer_contacts` 테이블로 나누지 않습니다.

## 2. 프로젝트 행

고객의 서비스/유지보수 단위마다 프로젝트 모듈 컨텐츠 한 행을 만듭니다.

| API 필드 | 저장 내용 |
|---|---|
| `module_idx` | 프로젝트 정보 모듈 ID |
| `title` | 프로젝트명/서비스명 |
| `ref_idx` | 연결할 고객 행의 `idx` |
| `tags` | 프로젝트 카테고리·검색 분류 |
| `content` | 프로젝트 메모 |
| `status` | 프로젝트 상태를 실제로 사용할 때만 지정 |

### 프로젝트 `tags`

카테고리/고객유형처럼 검색할 분류는 `content_raw`가 아닌 프로젝트 `tags`에 저장합니다.

```text
category_maintenance category_cms
```

- `tags`는 JSON이 아닙니다.
- 공백으로 태그를 구분합니다.
- 한 태그는 공백 없는 `접두어_값` 형식으로 통일합니다.

## 3. 사이트 행

운영 대상 주소마다 사이트 모듈 컨텐츠 한 행을 만듭니다.

| API 필드 | 저장 내용 |
|---|---|
| `module_idx` | 사이트 정보 모듈 ID |
| `parent_idx` | 연결할 프로젝트 행의 `idx` |
| `type` | 공용 API 사이트 유형 코드. 원본 `서비스구분`은 코드표 확인 뒤 변환 |
| `url` | 공개 URL, 호스팅/서버 URL, 관리자 URL을 쉼표로 구분 |
| `tags` | 호스팅·도메인·프레임워크·서버 역할 등 검색용 정보 |
| `content_raw` | 검색하지 않는 구조화 보조정보와 접속·DB 정보의 `access` 객체 |
| `content` | 검수 메모·운영 비고 |
| `receiver_idx` | 담당 member의 `idx` |

### 사이트 `tags`

```text
hosting_iwinv domain_iwinv frame_xe server_web
```

| 접두어 | 의미 | 예 |
|---|---|---|
| `hosting_` | 호스팅/클라우드 사업자 | `hosting_iwinv` |
| `domain_` | 도메인 등록업체 | `domain_iwinv` |
| `frame_` | 프레임워크/CMS | `frame_xe` |
| `server_` | 서버 역할 | `server_web` |
| `service_` | 서비스 성격이 필요한 경우 | `service_shop` |

## `tags`와 `content_raw` 기준

| 정보 | 저장 위치 |
|---|---|
| 고객 담당자·연락처 | 고객 `content_raw.contact[]` |
| 프로젝트 카테고리 | 프로젝트 `tags` |
| 원본 서비스구분 | 사이트 `content_raw.source_service_kind`; `type`은 API 코드표 확인 후 |
| 호스팅·도메인·프레임워크·서버 역할 | 사이트 `tags` |
| 검색할 필요 없는 구조화 보조정보 | 해당 행의 `content_raw` |
| 접속아이디·비밀번호·DB 정보 | 사이트 `content_raw.access` |

## API 적재 순서

1. 고객 요청을 생성하고, 응답의 `customer.idx`를 확보합니다.
2. 프로젝트 요청을 생성합니다. `ref_idx = customer.idx`를 넣습니다.
3. 응답의 `project.idx`를 확보합니다.
4. 사이트 요청을 생성합니다. `parent_idx = project.idx`를 넣습니다.
5. 모든 요청은 공용 API로 수행하며, 각 결과가 `wr_contents_t`에 저장됐는지 API 응답과 목록 조회로 확인합니다.

## 금지 사항

1. 고객·프로젝트·사이트별로 새 물리 테이블을 만들지 않습니다.
2. `module_idx`를 `parent_idx`, `ref_idx`, `receiver_idx`에 넣지 않습니다.
3. 카테고리를 별도 컨텐츠·테이블·`content_raw`로 만들지 않습니다.
4. 접속·DB 정보는 사이트 `content_raw.access`에 구조화하고, `content`·`tags`에는 넣지 않습니다.
