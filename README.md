# Hermes34 고객·프로젝트·사이트 데이터 모델

이미 생성된 DoWeb 컨텐츠 모듈을 즉시 운영하는 구조와, 장기적으로 정규화 DB로 전환하는 구조를 **분리**해 검수하는 문서입니다.

## 문서

1. [이상적인 정규화 구조 — ERD·DBML](docs/erd-1st-review.md)
   - 신규 운영 DB 또는 향후 이관 기준
   - 내부 식별자는 `BIGINT IDENTITY`
2. [우리기획(DoWeb) 규격 구조 — 기존 모듈 운영](docs/doweb-content-structure.md)
   - 제공된 `module_idx` 3개를 그대로 사용
   - `contents` API의 `title`, `content`, `content_raw`, `url`, `tags`, `parent_idx`, `ref_idx`, `receiver_idx`로 저장
3. [필드 매핑 및 이관 규칙](docs/source-field-mapping.md)
   - 두 구조 간 대응표와 데이터 품질 검수 기준
4. [참조용 DBML](docs/customer-project-site.dbml)

## 원칙

- **지금**: DoWeb 규격을 따르되, 관계·JSON·태그 규칙을 고정해 데이터가 더 흐트러지지 않게 합니다.
- **향후**: 주소·연락처·계정·공급자처럼 다중값인 필드는 정규화 DB로 분리합니다.
- 비밀번호·토큰·개인키는 Git·문서·Slack·일반 `content_raw`에 기록하지 않습니다. DoWeb `content_raw`에 `pw` 키가 필요한 기존 호환 요구가 있더라도, 실제 값은 제한 저장소의 `secret_ref`로 대체합니다.
