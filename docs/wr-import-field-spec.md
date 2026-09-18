# 우리기획 업체·콘텐츠 CSV 적재 명세

> 기준: `wr_company_t` 1개와 `wr_content_t`의 담당자·프로젝트·서비스 모듈 3개.
>
> 이 문서는 **현재 확정된 CSV 적재 계약**이다. 물리 DB DDL(예: VARCHAR 길이, NOT NULL, 실제 FK)은 제공되지 않았으므로, 확인되지 않은 DB 컬럼 길이나 SQL 제약은 단정하지 않는다.

## 1. 공통 규칙

| 항목 | 규칙 |
|---|---|
| 파일 인코딩 | UTF-8 with BOM (`utf-8-sig`) |
| 구분자 | CSV 쉼표(`,`), RFC 4180 방식의 큰따옴표 이스케이프 |
| 신규 `idx` | RFC 9562 UUID v7, 소문자 36자 문자열. 형식: `xxxxxxxx-xxxx-7xxx-[89ab]xxx-xxxxxxxxxxxx` |
| 날짜 | 실제 날짜가 있을 때만 `YYYY-MM-DD`; 날짜가 없으면 빈 값. 임의의 미래 종료일을 넣지 않음 |
| 상태/유형 | 원본이 빈 값 또는 `unknown`이면 `0`; 그 외 원본 코드 유지 |
| 빈 값 | 미확인·미제공 데이터는 빈 CSV 값. 추정·보완·복사 금지 |
| 민감정보 | 계정값은 서비스의 `content_raw.accounts`에만 저장하고 해당 서비스의 `is_hidden=1` |

## 2. 관계 및 고정 모듈 값

```text
wr_company_t.idx
  ├─ 담당자 wr_content_t.company_idx
  ├─ 프로젝트 wr_content_t.company_idx
  └─ 서비스 wr_content_t.company_idx

프로젝트 wr_content_t.idx
  └─ 서비스 wr_content_t.parent_idx
```

| 콘텐츠 | `module_idx` | 관계 |
|---|---|---|
| 담당자 | `01a05700-8c1d-7cd4-8b2d-fac77f865a9f` | `company_idx` 필수 |
| 프로젝트 | `01a05701-ed99-7cfa-841e-ec6f6c9922a0` | `company_idx` 필수 |
| 서비스 | `01a05702-067e-729b-85ab-deb5b0836082` | `company_idx`, `parent_idx` 필수 |

- `company_idx`는 반드시 `company.csv.idx`에 존재해야 한다.
- 서비스 `parent_idx`는 반드시 `project_module.csv.idx`에 존재해야 한다.
- `ref_idx`는 프로젝트의 보조 참조 필드이며, 현재 이관 데이터에서는 **빈 값**이다. 고객/업체 관계에 사용하지 않는다.
- `receiver_idx`는 내부 member 연결용이며, 현재 이관 데이터에서는 **빈 값**이다. 외부 담당자 연결에 사용하지 않는다.

## 3. `company.csv` → `wr_company_t`

현재 최소 이관에서 값이 들어가는 열은 `idx`, `company_name`뿐이다. 나머지 열은 대상 DB 템플릿의 열 순서를 유지하기 위해 빈 값으로 출력한다.

| 필드 | 형식 | 필수 | 제한/허용값 | 현재 이관 |
|---|---|---:|---|---|
| `idx` | UUID v7 | 예 | 중복 불가, 회사 참조의 기준값 | 입력 |
| `company_name` | UTF-8 텍스트 | 예 | 공백만 허용하지 않음 | 입력 |
| `company_number` | 텍스트 | 아니오 | 원본 제공값만 | 빈 값 |
| `company_phone` | 텍스트 | 아니오 | 원본 제공값만 | 빈 값 |
| `company_email` | 이메일 텍스트 | 아니오 | 원본 제공값만 | 빈 값 |
| `company_manager_name` | UTF-8 텍스트 | 아니오 | 원본 제공값만 | 빈 값 |
| `company_manager_phone` | 텍스트 | 아니오 | 원본 제공값만 | 빈 값 |
| `company_manager_email` | 이메일 텍스트 | 아니오 | 원본 제공값만 | 빈 값 |
| `company_address` | UTF-8 텍스트 | 아니오 | 원본 제공값만 | 빈 값 |
| `company_address_2` | UTF-8 텍스트 | 아니오 | 원본 제공값만 | 빈 값 |
| `company_extras` | JSON 또는 텍스트 | 아니오 | 임의 JSON 금지 | 빈 값 |
| `tags` | 공백 구분 텍스트 | 아니오 | 임의 태그 생성 금지 | 빈 값 |
| `admin_idx` | 내부 member ID | 아니오 | 실제 member ID만 | 빈 값 |

## 4. `contact_module.csv` → 담당자 `wr_content_t`

| 필드 | 형식 | 필수 | 제한/허용값 | 현재 이관 |
|---|---|---:|---|---|
| `idx` | UUID v7 | 예 | 중복 불가 | 입력 |
| `module_idx` | UUID | 예 | 담당자 모듈 ID 고정값만 | 입력 |
| `company_idx` | UUID v7 | 예 | `company.csv.idx` 참조 | 입력 |
| `name` | UTF-8 텍스트 | 예 | 원본 담당자명, 공백만 불가 | 입력 |
| `content` | UTF-8 텍스트 | 아니오 | 임의 메모 금지 | 빈 값 |
| `contact` | 전화번호 텍스트 | 아니오 | 원본 표기 보존 | 입력 가능 |
| `email` | 이메일 텍스트 | 아니오 | 원본 표기 보존 | 입력 가능 |

## 5. `project_module.csv` → 프로젝트 `wr_content_t`

| 필드 | 형식 | 필수 | 제한/허용값 | 현재 이관 |
|---|---|---:|---|---|
| `idx` | UUID v7 | 예 | 중복 불가 | 입력 |
| `module_idx` | UUID | 예 | 프로젝트 모듈 ID 고정값만 | 입력 |
| `ref_idx` | UUID 또는 빈 값 | 아니오 | 현재 업체 관계에 사용 금지 | 빈 값 |
| `company_idx` | UUID v7 | 예 | `company.csv.idx` 참조 | 입력 |
| `title` | UTF-8 텍스트 | 예 | 원본 프로젝트명, 공백만 불가 | 입력 |
| `status` | 정수 코드 | 예 | `1` 운영, `-1` 비운영/종료, `0` 빈 값/unknown | 입력 |
| `date_start` | `YYYY-MM-DD` 또는 빈 값 | 아니오 | 실제 시작일만 | 입력 가능 |
| `date_end` | `YYYY-MM-DD` 또는 빈 값 | 아니오 | 실제 종료일만 | 입력 가능 |
| `type` | 정수 코드 | 예 | 현재 이관에서는 `0`만 사용 | `0` |
| `url` | URL/호스트 텍스트 | 아니오 | 현재 프로젝트 데이터에는 미사용 | 빈 값 |
| `tags` | 공백 구분 텍스트 | 아니오 | 임의 태그 생성 금지 | 빈 값 |
| `receiver_idx` | 내부 member ID 또는 빈 값 | 아니오 | 외부 담당자 ID 사용 금지 | 빈 값 |
| `is_hidden` | `1`, `0` 또는 빈 값 | 아니오 | 현재 프로젝트에는 미사용 | 빈 값 |
| `content_raw` | JSON 또는 빈 값 | 아니오 | 현재 프로젝트에는 미사용 | 빈 값 |
| `content` | UTF-8 텍스트 | 아니오 | 임의 메모 금지 | 빈 값 |

## 6. `service_module.csv` → 서비스 `wr_content_t`

| 필드 | 형식 | 필수 | 제한/허용값 | 현재 이관 |
|---|---|---:|---|---|
| `idx` | UUID v7 | 예 | 중복 불가 | 입력 |
| `module_idx` | UUID | 예 | 서비스 모듈 ID 고정값만 | 입력 |
| `parent_idx` | UUID v7 | 예 | `project_module.csv.idx` 참조 | 입력 |
| `company_idx` | UUID v7 | 예 | `company.csv.idx` 참조 | 입력 |
| `title` | UTF-8 텍스트 | 예 | 원본 서비스명, 공백만 불가 | 입력 |
| `status` | 정수 코드 | 예 | `1` 운영, `-1` 비운영/종료, `0` 빈 값/unknown | 입력 |
| `date_start` | `YYYY-MM-DD` 또는 빈 값 | 아니오 | 실제 시작일만 | 입력 가능 |
| `date_end` | `YYYY-MM-DD` 또는 빈 값 | 아니오 | 실제 종료일만 | 입력 가능 |
| `type` | 정수 코드 | 예 | `1` 실제 운영, `2` 테스트/개발, `3` 샘플, `0` 빈 값/unknown | 입력 |
| `url` | 쉼표 구분 URL/호스트 텍스트 | 아니오 | 원본의 서비스·호스팅 주소만, 공백·추정 URL 금지 | 입력 가능 |
| `tags` | 공백 구분 텍스트 | 아니오 | 임의 태그 생성 금지 | 빈 값 |
| `receiver_idx` | 내부 member ID 또는 빈 값 | 아니오 | 외부 담당자 ID 사용 금지 | 빈 값 |
| `is_hidden` | 정수 코드 | 예 | 계정이 있는 서비스는 `1`; 현 이관 서비스는 모두 `1` | `1` |
| `content_raw` | JSON 또는 빈 값 | 계정이 있을 때 예 | 아래 `accounts` 규격만 허용 | 입력 가능 |
| `content` | UTF-8 텍스트 | 아니오 | 임의 메모 금지 | 빈 값 |

## 7. 서비스 `content_raw` JSON 명세

`content_raw`에 허용되는 최상위 키는 **`accounts` 하나뿐**이다. 계정이 없으면 빈 값으로 둔다. `{}`, `urls`, `access_check`, `status`, `type`, `risk_flags` 등은 넣지 않는다.

```json
{
  "accounts": [
    {
      "type": "FTP",
      "id": "<원본_접속아이디>",
      "pw": "<원본_접속비밀번호>"
    },
    {
      "type": "DB_iwinv",
      "url": "<원본_phpMyAdmin_URL>",
      "id": "<원본_DB_아이디>",
      "pw": "<원본_DB_비밀번호>"
    },
    {
      "type": "admin",
      "id": "<원본_관리자아이디>",
      "pw": "<원본_관리자비밀번호>"
    }
  ]
}
```

### `accounts[]` 필드

| JSON 경로 | 형식 | 필수 | 허용값/제한 |
|---|---|---:|---|
| `accounts` | JSON 배열 | 예 | 계정 객체 1개 이상. 계정이 없으면 `content_raw` 자체를 빈 값으로 둠 |
| `accounts[].type` | 문자열 | 예 | `FTP`, `DB_iwinv`, `DB`, `admin` 중 하나 |
| `accounts[].id` | 문자열 | 아니오 | 원본 계정 ID만. 값이 없으면 키 자체를 생략 |
| `accounts[].pw` | 문자열 | 아니오 | 원본 비밀번호만. 값이 없으면 키 자체를 생략 |
| `accounts[].url` | URL 문자열 | 아니오 | DB 관리도구 등 원본 URL만. 값이 없으면 키 자체를 생략 |

계정 객체에는 위 네 키 외의 키를 넣지 않는다. `DB_iwinv`는 iwinv 호스팅의 DB 계정이고, iwinv 외 DB 계정은 `DB`를 사용한다.

## 8. 적재 전 검증

1. 네 CSV의 모든 `idx`가 UUID v7인지 확인한다.
2. 담당자·프로젝트·서비스의 `company_idx`가 업체 CSV에 존재하는지 확인한다.
3. 서비스의 `parent_idx`가 프로젝트 CSV에 존재하는지 확인한다.
4. 프로젝트/서비스 `status`, `type`에 빈 값 또는 `unknown`이 없는지 확인한다.
5. 서비스 `content_raw`가 유효한 JSON인지, 최상위 키가 `accounts`만인지 확인한다.
6. 계정 객체가 `type`, `id`, `pw`, `url` 외 키를 가지지 않는지 확인한다.
7. `service_module.csv`는 민감정보 파일이므로 공개 Git 저장소·일반 메신저 전달 대상에서 제외한다.
