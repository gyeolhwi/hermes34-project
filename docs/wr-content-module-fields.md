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
| `status` | `1=운영`, `-1=비운영` |
| `date_start`, `date_end` | 시작일·종료일; 종료일 없으면 `2999-12-31` |
| `type`, `url`, `tags` | 프로젝트 분류·주소·검색 태그; 현재 예시에서는 비어 있을 수 있음 |
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
| `status` | `1=운영`, `-1=비운영` |
| `date_start`, `date_end` | 서비스 시작일·종료일 |
| `type` | `1=운영`, `2=개발`, `3=샘플` |
| `url` | `도메인주소,호스팅주소` 형식 |
| `tags` | 호스팅·프레임워크·카테고리 검색 태그 |
| `receiver_idx` | 현재 비어 있음; 외부 담당자는 담당자 모듈에서 관리 |
| `is_hidden` | 서비스 민감 데이터 보호를 위해 `1` |
| `content_raw` | 접속·DB·관리자 계정 등 검색 불필요한 민감 JSON |
| `content` | 서비스 메모 |

## 관계

```text
company.idx ── company_idx ── 담당자
            ├─ company_idx ── 프로젝트
            └─ company_idx ── 서비스

project.idx ── parent_idx ── 서비스
```
