# 서비스 시트 → 우리기획 공용 API 필드 매핑

## 참조한 원본 시트

이 문서는 아래 파일만 기준으로 작성했습니다.

```text
/home/hermes/Work/secure-intake/service-sheets/service-inventory.xlsx
시트: 서비스_메인
범위: A1:AD1000
```

이 시트는 **고객 마스터 시트가 아니라 서비스/사이트 단위 시트**입니다. 헤더상 고객명 전용 열이 없으며, `카테고리`는 고객명으로 사용하면 안 되는 고객 유형/분류 값입니다. 따라서 고객 행을 자동으로 만들기 위한 고객명·고객 묶음 규칙은 이 파일만으로 확정할 수 없습니다.

## 원본 시트 필드 목록

| 열 | 원본 필드 | 성격 | API 적재 판단 |
|---|---|---|---|
| A | 서비스ID | 원본 식별자 | `content_raw.source_service_id`로 보존 |
| B | 운영상태 | 운영 상태 | `status` 매핑표 확정 후 사용 |
| C | 서비스명 | 서비스 표시명 | 프로젝트 `title` 후보 |
| D | 카테고리 | 고객 유형/분류 | 프로젝트 `tags`: `category_*` |
| E | 서비스구분 | 실제/테스트/관리자 등 | 사이트 `type` 매핑 필요 |
| F | 도메인주소 | 공개 도메인 | 사이트 `url` |
| G | 호스팅주소 | 서버/호스팅 주소 | 사이트 `url` |
| H | 접속아이디 | 비밀 접근 정보 | 제한 저장소로 이동, API 일반 필드에는 미적재 |
| I | 접속비밀번호 | 비밀값 | 제한 저장소로 이동, 절대 API/Git에 미적재 |
| J | 관리자아이디 | 비밀 접근 정보 | 제한 저장소로 이동, API 일반 필드에는 미적재 |
| K | 관리자비밀번호 | 비밀값 | 제한 저장소로 이동, 절대 API/Git에 미적재 |
| L | DB접속경로 | 접속 정보 | 제한 저장소 또는 검수 메모; 공개 API 기본 적재 제외 |
| M | DB아이디 | 비밀 접근 정보 | 제한 저장소로 이동 |
| N | DB비밀번호 | 비밀값 | 제한 저장소로 이동, 절대 API/Git에 미적재 |
| O | 고객연락처 | 고객 연락처 원문 | 고객 `content_raw.contact[]`로 정제 후 저장 |
| P | 고객이메일 | 고객 이메일 원문 | 고객 `content_raw.contact[]`로 정제 후 저장 |
| Q | 도메인등록업체 | 검색 분류 | 사이트 `tags`: `domain_*` |
| R | 호스팅사 | 검색 분류 | 사이트 `tags`: `hosting_*` |
| S | 프레임워크 | 검색 분류 | 사이트 `tags`: `frame_*` |
| T | 검수메모 | 검수 기록 | 사이트 `content` |
| U | 비고 | 운영 메모 | 사이트 `content` |
| V | 작업자 | 담당자 이름 | member 조회 후 사이트 `receiver_idx` |
| W | 개설일 | 원본 이력 | 사이트 `content_raw.opened_at` |
| X | 접속분류 | 접속 운영 분류 | 사이트 `tags`: `connection_*` 또는 `content_raw` |
| Y | VPN 필요 | 접속 정책 | 사이트 `content_raw.vpn_required` |
| Z | VPN 프로필 | 제한 접속 정보 | 제한 저장소 참조 또는 `content_raw.vpn_profile_ref` |
| AA | SSH 호스트키 상태 | 접속 검증 상태 | 사이트 `content_raw.ssh_host_key_status` |
| AB | 접속 사전점검 | 접속 검증 상태 | 사이트 `content_raw.connection_precheck` |
| AC | 검증일 | 접속 검증 이력 | 사이트 `content_raw.verified_at` |
| AD | 검증메모 | 접속 검증 이력 | 사이트 `content_raw.verification_note` |

## 한 서비스 행을 API에 넣는 구조

현재 원본 한 행은 주로 **프로젝트 + 사이트**를 만들 수 있는 정보입니다. 고객 행은 고객 식별 규칙이 확정된 뒤에만 생성합니다.

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
      ├─ tags        ← Q/R/S/X의 검색용 값
      ├─ content     ← 검수메모(T), 비고(U)
      └─ content_raw ← 서비스ID·검증 이력 등 비검색 구조화 정보
```

## API payload 필드별 매핑

### 고객 컨텐츠

고객명 전용 열이 없는 상태이므로 아래 두 필드는 **고객 묶음 규칙 확정 전에는 만들지 않습니다.**

| API 필드 | 원본 열 | 처리 |
|---|---|---|
| `module_idx` | 고정 | 고객 모듈 ID |
| `title` | 없음 | 고객명/고객 묶음 규칙 필요 |
| `content_raw.contact[]` | O 고객연락처, P 고객이메일 | 담당자별 이름·연락처를 파싱·검수 후 JSON화 |

### 프로젝트 컨텐츠

| API 필드 | 원본 열 | 예시/처리 |
|---|---|---|
| `module_idx` | 고정 | 프로젝트 모듈 ID |
| `title` | C 서비스명 | 그대로 사용, 중복은 원본 서비스ID로 구분 |
| `ref_idx` | 고객 생성 결과 | 고객 컨텐츠 `idx`; 자동 결정 금지 |
| `tags` | D 카테고리 | `category_church`, `category_company`처럼 정규화 |
| `status` | B 운영상태 | 상태 코드표 확정 후 변환 |
| `content` | 필요 시 U 비고 | 프로젝트 수준 메모만 이동 |
| `content_raw` | A 서비스ID | `{"source_service_id":"SVC-..."}` |

### 사이트 컨텐츠

| API 필드 | 원본 열 | 예시/처리 |
|---|---|---|
| `module_idx` | 고정 | 사이트 모듈 ID |
| `parent_idx` | 프로젝트 생성 결과 | 프로젝트 컨텐츠 `idx` |
| `type` | E 서비스구분 | `실제`/`테스트`/`관리자`의 변환표 확정 필요 |
| `url` | F 도메인주소, G 호스팅주소 | 비어 있지 않은 값만 쉼표로 결합 |
| `tags` | Q/R/S/X | `domain_* hosting_* frame_* connection_*` |
| `receiver_idx` | V 작업자 | 이름으로 member를 정확히 조회한 `idx` |
| `content` | T 검수메모, U 비고 | 라벨을 유지해 합침 |
| `content_raw` | A/W/Y/Z/AA/AB/AC/AD | 아래 JSON 예시 |

```json
{
  "source_service_id": "SVC-000",
  "opened_at": "YYYY-MM-DD",
  "vpn_required": false,
  "vpn_profile_ref": "restricted://vpn/profile-id",
  "ssh_host_key_status": "...",
  "connection_precheck": "...",
  "verified_at": "YYYY-MM-DD",
  "verification_note": "..."
}
```

## 적재 제외·별도 처리 필드

H~N은 접근 아이디·비밀번호·DB 접속정보이며 일반 공용 API 데이터로 그대로 옮기면 안 됩니다.

1. 실제 비밀번호·토큰·개인키는 `content_raw`, `content`, `tags`에 넣지 않습니다.
2. 필요한 접근 정보는 제한 저장소에 이전합니다.
3. API에는 제한 저장소를 가리키는 참조값(`secret_ref` 또는 별도 `*_ref`)만 넣습니다.
4. O/P 연락처도 개인정보이므로 원본 형식을 기계적으로 복사하지 않고 담당자·전화·이메일 단위로 검수합니다.

## 적재 전 확정이 필요한 항목

| 결정 항목 | 현재 시트만으로 확정 불가한 이유 |
|---|---|
| 고객명과 고객 묶음 규칙 | 고객명 열이 없음. `카테고리`는 유형일 뿐 고객명이 아님 |
| `실제`/`테스트`/`관리자` → 사이트 `type` 변환 | 현재 API 운영 환경 코드와 1:1 대응이 정해지지 않음 |
| `운영`/`종료` → `status` 코드 | 공용 API의 상태 코드표 확인 필요 |
| 작업자 이름 → `receiver_idx` | member 목록의 실제 `idx` 대조 필요 |
| 원본 중복 서비스 행 처리 | 동일 도메인·서비스명·접속정보가 반복될 수 있어 서비스ID 기준 검수 필요 |
