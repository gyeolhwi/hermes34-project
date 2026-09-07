# Hermes34 고객시트 → 우리기획(DoWeb) 공용 API 적재 규격

Hermes34 고객시트 데이터는 고객·프로젝트·사이트별 신규 테이블로 정규화하지 않습니다. 공용 API의 컨텐츠 생성·수정 요청으로 적재하며, 결과는 DoWeb 공용 컨텐츠 테이블 **`wr_content_t`**에 행 단위로 저장됩니다.

## 문서

1. [서비스 시트 → 공용 API 필드 매핑](docs/service-sheet-api-field-mapping.md)
   - 참조한 실제 엑셀 파일·시트·30개 원본 필드 목록
   - 원본 열 → 공용 API payload 필드별 매핑 및 적재 보류 항목
2. [DoWeb `wr_content_t` 적재 규격](docs/doweb-content-structure.md)
   - 고객·프로젝트·사이트 행의 `module_idx`, `idx`, `ref_idx`, `parent_idx` 사용 기준
   - `content_raw`, `tags`, `type`의 저장 위치와 형식

## 핵심 규칙

- 고객·프로젝트·사이트는 물리 테이블이 아니라 `module_idx`로 구분하는 컨텐츠 종류입니다.
- 고객 1건, 프로젝트 1건, 사이트 1건은 각각 `wr_content_t`의 컨텐츠 행 1건입니다.
- 프로젝트는 `ref_idx = customer.idx`, 사이트는 `parent_idx = project.idx`로 연결합니다.
- 프로젝트 분류는 프로젝트 `tags`, 사이트 환경은 사이트 `type`, 호스팅·프레임워크 등의 검색 정보는 사이트 `tags`에 저장합니다.
- 연락처처럼 검색하지 않는 구조화 정보는 `content_raw` JSON 문자열로 저장합니다.
- 실제 비밀번호·토큰·개인키는 `wr_content_t`, Git, Slack에 저장하지 않고 제한 저장소로 관리합니다.
