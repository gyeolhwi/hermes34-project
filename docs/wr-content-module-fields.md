# 업체·담당자·프로젝트·서비스 필드표

## 역할 구분

| 저장소 | 역할 |
|---|---|
| `wr_company_t` | 업체 기본정보 |
| `wr_content_t` 담당자 모듈 | 업체에 속한 고객/서브 담당자 정보 |
| `wr_content_t` 프로젝트 모듈 | 업체에 속한 프로젝트 정보 |
| `wr_content_t` 서비스 모듈 | 업체에 속하고 프로젝트에 귀속되는 서비스 정보 |

`wr_module_t`의 담당자·프로젝트·서비스 게시판은 콘텐츠 행이 아닙니다. `wr_content_t.module_idx`에는 게시판의 실제 `idx`를 저장합니다.

## 업체 (`wr_company_t`)

| 필드 | 용도 |
|---|---|
| `idx` | 업체 고유 ID; 콘텐츠 `company_idx`의 참조값 |
| `company_name` | 업체명 |
| `company_number`, `company_phone`, `company_email` | 업체 기본 연락처 |
| `company_manager_*` | 업체 대표 담당자 정보 |
| `company_address`, `company_address_2` | 업체 주소 |
| `company_extras` | 업체 추가정보 |
| `tags` | 업체 검색 태그 |
| `admin_idx` | 관리 member ID |

## 담당자 콘텐츠 (`module_idx=`01a05700-8c1d-7cd4-8b2d-fac77f865a9f)

제공된 담당자 CSV 기준 필드입니다. 담당자는 업체의 고객/서브 담당자 역할입니다.

| 필드 | 용도 |
|---|---|
| `idx` | 담당자 콘텐츠 ID |
| `module_idx` | 담당자 모듈 ID |
| `company_idx` | 소속 업체 ID |
| `name` | 담당자명 |
| `content` | 담당자 메모 |
| `contact` | 연락처 |
| `email` | 이메일 |

## 프로젝트 콘텐츠 (`module_idx=`01a05701-ed99-7cfa-841e-ec6f6c9922a0)

| 필드 | 용도 |
|---|---|
| `idx` | 프로젝트 콘텐츠 ID |
| `module_idx` | 프로젝트 모듈 ID |
| `ref_idx` | 현재 제공 데이터에서는 비어 있는 보조 참조값 |
| `company_idx` | 소속 업체 ID |
| `title` | 프로젝트명 |
| `status` | `1=운영`, `-1=비운영`, `0=값 없음/unknown` |
| `date_start`, `date_end` | 시작일·종료일; 종료일 없으면 `2999-12-31` |
| `type`, `url`, `tags` | 프로젝트 분류·주소·검색 태그; 값이 없으면 `type=0` |
| `receiver_idx` | 내부 member 연결값; 외부 담당자 연결 기준으로 쓰지 않음 |
| `is_hidden` | 보호 처리 설정값 |
| `content_raw` | 검색 불필요한 원본 JSON |
| `content` | 사람이 읽는 메모 |

## 서비스 콘텐츠 (`module_idx=`01a05702-067e-729b-85ab-deb5b0836082)

| 필드 | 용도 |
|---|---|
| `idx` | 서비스 콘텐츠 ID |
| `module_idx` | 서비스 모듈 ID |
| `parent_idx` | 귀속 프로젝트 콘텐츠 `idx` |
| `company_idx` | 소속 업체 ID; 프로젝트 귀속과 별개 |
| `title` | 서비스명 |
| `status` | `1=운영`, `-1=비운영`, `0=값 없음/unknown` |
| `date_start`, `date_end` | 서비스 시작일·종료일 |
| `type` | `1=운영`, `2=개발`, `3=샘플`, `0=값 없음/unknown` |
| `url` | `도메인주소,호스팅주소` 형식 |
| `tags` | 호스팅·프레임워크·카테고리 검색 태그 |
| `receiver_idx` | 현재 비어 있음; 외부 담당자는 담당자 모듈에서 관리 |
| `is_hidden` | 서비스 민감 데이터 보호를 위해 `1` |
| `content_raw` | **`accounts`만** 저장하는 민감 JSON. 계정마다 `type`, 필요 시 `url`, `id`, `pw`만 둔다. URL 목록·접속점검·상태·기간 등 다른 서비스 정보는 넣지 않는다. |
| `content` | 서비스 메모 |

## 관계

```text
company.idx ── company_idx ── 담당자
            ├─ company_idx ── 프로젝트
            └─ company_idx ── 서비스

project.idx ── parent_idx ── 서비스
```

## 서비스 관리대장 정제본 활용 범위

`ubot_db` 인계본의 `company`, `site`, `service`, `service_url`, `contact`, `credential`, `access_check`, `project`은 서비스 메인 통합본을 정제·검증하기 위한 **중간 모델**이다. 이는 우리기획 운영 DB에 새 테이블로 추가하는 대상이 아니다.

실제 우리기획 적재 대상은 계속 아래 네 CSV이며, `wr_company_t`와 세 종류의 `wr_content_t` 콘텐츠만 사용한다.

| 정제본 데이터 | 우리기획 적재 위치 | 입력 원칙 |
|---|---|---|
| `company` | `company.csv` → `wr_company_t` | 대표 업체, `merged_into`·`migrate` 판단을 반영한다. |
| `contact` | `contact_module.csv` → 담당자 `wr_content_t` | `company_idx`를 유지하고 고객/서브 담당자로 적재한다. |
| `project` | `project_module.csv` → 프로젝트 `wr_content_t` | 업체 귀속 프로젝트로 적재한다. |
| `service` + `site` | `service_module.csv` → 서비스 `wr_content_t` | 서비스 기본값·기간·상태는 일반 필드에 적재한다. |
| `service_url` | 서비스 `url` | 실제 서비스·호스팅 주소만 일반 서비스 필드로 보존한다. |
| `credential` | 서비스 `content_raw.accounts[]` | 민감정보이므로 `is_hidden=1`; 각 계정에는 `type`, 필요 시 `url`, `id`, `pw`만 둔다. GitHub·일반 문서에는 실제 값을 기록하지 않는다. |
| `access_check` | 정제 인계본에 유지 | 우리기획 현재 콘텐츠 필드에는 투영하지 않는다. |

### 적재 전 적용 규칙

- `migrate=0` 또는 업체가 `merged_into`를 가진 항목은 자동 적재하지 않고 검토 대상으로 남긴다.
- 봇 실행 후보는 서비스 상태만으로 고르지 않는다. `migrate=1`, 병합되지 않은 업체, `live_status=live/redirect`, 접속 사전점검을 함께 확인한다.
- `site`는 도메인/배포 이력을 정리하기 위한 중간 식별자다. 우리기획 구조에는 별도 사이트 테이블이 없으므로 서비스 콘텐츠의 `url`로만 투영한다.
- 모든 신규 `idx`는 UUID v7으로 생성한다. 기존 담당자·프로젝트·서비스의 `module_idx`는 아래 고정 모듈 ID를 그대로 쓴다.

### 현재 이관 CSV의 최소 입력 원칙

인계본에서 검증된 값과 사용자 지정 코드만 적재한다. 태그·업체 보조정보·메모·정제 이력·접속점검은 별도 인계본에 남기며, 우리기획 CSV에는 임의로 조합하거나 복사하지 않는다.

| CSV | 값이 들어가는 필드 |
|---|---|
| `company.csv` | `idx`, `company_name` |
| `contact_module.csv` | `idx`, `module_idx`, `company_idx`, `name`, `contact`, `email` |
| `project_module.csv` | `idx`, `module_idx`, `company_idx`, `title`, `status`, `date_start`, `date_end`, `type` |
| `service_module.csv` | `idx`, `module_idx`, `parent_idx`, `company_idx`, `title`, `status`, `date_start`, `date_end`, `type`, `url`, `is_hidden`, `content_raw.accounts` |

비어 있는 대상 필드는 빈 값으로 둔다. `status`·`type` 원본 값이 비어 있거나 `unknown`인 경우에만 사용자 지정 코드 `0`을 쓴다.

## CSV 예시별 입력값 안내

아래의 `*-001` 값은 **예시용 식별자**입니다. 실제 적재 시에는 생성 API 또는 DB에서 반환한 실제 `idx`를 사용합니다. 모듈 ID만 현재 생성된 `wr_module_t.idx`를 고정으로 사용합니다.

### 1. 업체 CSV (`company_example.csv`)

| 필드 | 예시 입력값 | 실제 입력 기준 |
|---|---|---|
| `idx` | `company-001` | 업체 생성 후 반환된 `wr_company_t.idx` |
| `company_name` | `예시 업체` | 실제 업체명 |
| `company_number` | 빈 값 | 사업자번호가 있으면 입력 |
| `company_phone`, `company_email` | 빈 값 | 업체 대표 연락처가 있으면 입력 |
| `company_manager_*` | 빈 값 | 업체 대표 담당자 정보가 있으면 입력 |
| `company_address*` | 빈 값 | 업체 주소가 있으면 입력 |
| `tags` | 빈 값 | 업체 검색 태그가 필요할 때 입력 |
| `admin_idx` | 빈 값 | 내부 관리 member를 지정할 때만 입력 |

### 2. 담당자 CSV (`contact_module_example.csv`)

| 필드 | 예시 입력값 | 실제 입력 기준 |
|---|---|---|
| `idx` | `contact-content-001` | 담당자 콘텐츠 생성 후 반환된 `idx` |
| `module_idx` | `01a05700-8c1d-7cd4-8b2d-fac77f865a9f` | 담당자 모듈의 고정 ID |
| `company_idx` | `company-001` | 소속 업체의 실제 `wr_company_t.idx` |
| `name` | `예시 담당자` | 고객/서브 담당자명 |
| `content` | `담당자 메모` | 역할·비고 등 메모; 없으면 빈 값 |
| `contact` | `+821000000000` | 전화번호 등 연락처; 없으면 빈 값 |
| `email` | `contact@example.test` | 이메일; 없으면 빈 값 |

### 3. 프로젝트 CSV (`project_module_example.csv`)

| 필드 | 예시 입력값 | 실제 입력 기준 |
|---|---|---|
| `idx` | `project-content-001` | 프로젝트 콘텐츠 생성 후 반환된 `idx` |
| `module_idx` | `01a05701-ed99-7cfa-841e-ec6f6c9922a0` | 프로젝트 모듈의 고정 ID |
| `ref_idx` | 빈 값 | 현재 구조에서는 비움; 별도 참조 규칙이 확정될 때만 입력 |
| `company_idx` | `company-001` | 소속 업체의 실제 `idx` |
| `title` | `예시 프로젝트` | 프로젝트명 |
| `status` | `1` | `1=운영`, `-1=비운영` |
| `date_start` | `2024-05-20` | 실제 시작일/개설일 (`YYYY-MM-DD`) |
| `date_end` | `2999-12-31` | 실제 종료일; 없으면 기본값 `2999-12-31` |
| `type`, `url`, `tags` | 빈 값 | 프로젝트에서 사용할 값이 있을 때만 입력 |
| `receiver_idx`, `is_hidden` | 빈 값 | 내부 member/보호 설정이 필요한 경우만 입력 |
| `content_raw` | `{"source":{"service_id":"SVC-001"}}` | 검색하지 않을 원본 식별값만 JSON으로 입력 |
| `content` | `프로젝트 메모` | 사람이 읽는 비고 |

### 4. 서비스 CSV (`service_module_example.csv`)

| 필드 | 예시 입력값 | 실제 입력 기준 |
|---|---|---|
| `idx` | `service-content-001` | 서비스 콘텐츠 생성 후 반환된 `idx` |
| `module_idx` | `01a05702-067e-729b-85ab-deb5b0836082` | 서비스 모듈의 고정 ID |
| `parent_idx` | `project-content-001` | 귀속 프로젝트의 실제 콘텐츠 `idx` |
| `company_idx` | `company-001` | 소속 업체의 실제 `idx`; 부모 프로젝트와 같은 업체인지 대조 |
| `title` | `예시 서비스` | 서비스/사이트 표시명 |
| `status` | `1` | `1=운영`, `-1=비운영` |
| `date_start`, `date_end` | `2024-05-20`, `2999-12-31` | 실제 서비스 기간 (`YYYY-MM-DD`) |
| `type` | `1` | `1=운영`, `2=개발`, `3=샘플` |
| `url` | `https://service.example.test,https://host.example.test` | 도메인주소와 호스팅주소를 쉼표로 구분 |
| `tags` | `hosting_example frame_example cat_example` | 검색용 호스팅·프레임워크·카테고리 태그 |
| `receiver_idx` | 빈 값 | 내부 member 지정 시만 입력; 외부 고객 담당자는 담당자 모듈 사용 |
| `is_hidden` | `1` | 민감 접속정보를 보관하는 서비스는 반드시 `1` |
| `content_raw` | `{"accounts":[...]}` | 접속·DB·관리자 계정 등 검색 불필요한 민감 JSON; 실제 비밀번호는 외부 문서에 복사하지 않음 |
| `content` | `서비스 메모` | 검수 내용·비고 |
