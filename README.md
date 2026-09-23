# Hermes34 → 우리기획 공용 API 적재 구조

## 핵심

업체는 `wr_company_t`에서 관리합니다. 담당자·프로젝트·서비스는 `wr_module_t`에서 생성한 게시판(모듈)이며, 각 데이터는 `wr_content_t`에 저장합니다.

```text
wr_company_t (업체)
 ├─ wr_content_t: 담당자 모듈
 ├─ wr_content_t: 프로젝트 모듈
 └─ wr_content_t: 서비스 모듈
       └─ parent_idx → 프로젝트 콘텐츠
```

각 콘텐츠의 `company_idx`는 소속 업체를 가리킵니다. 서비스의 `parent_idx`는 프로젝트 귀속 관계이며, 업체 귀속과 별개입니다.

## 모듈 ID

| 모듈 | `wr_module_t.idx` |
|---|---|
| 담당자 | `01a05700-8c1d-7cd4-8b2d-fac77f865a9f` |
| 프로젝트 | `01a05701-ed99-7cfa-841e-ec6f6c9922a0` |
| 서비스 | `01a05702-067e-729b-85ab-deb5b0836082` |

## 공통 원칙

- `module_idx`에는 모듈 이름이 아니라 위 `wr_module_t.idx`를 저장합니다.
- `company_idx`에는 소속 `wr_company_t.idx`를 저장합니다.
- 검색·관계·상태·기간에 필요한 값은 일반 필드에 저장합니다.
- `content_raw`에는 검색이 불필요하거나 보호가 필요한 원본값만 JSON으로 저장합니다. 서비스의 접속·DB 계정은 여기에 보관합니다.
- 서비스는 `is_hidden=1`로 설정하여 이 배포 환경의 민감 데이터 보호 처리를 적용합니다.
- 외부 고객 담당자는 담당자 모듈로 관리하며, `receiver_idx`는 담당자 관계의 기준이 아닙니다.

## 문서

1. [업체·모듈 필드표](docs/wr-content-module-fields.md)
2. [관계 및 적재 규격](docs/doweb-content-structure.md)
3. [정합성 점검](docs/data-integrity-check.md)
4. [업체 CSV 예시](examples/company_example.csv)
5. [담당자 CSV 예시](examples/contact_module_example.csv)
6. [프로젝트 CSV 예시](examples/project_module_example.csv)
7. [서비스 CSV 예시](examples/service_module_example.csv)
8. [이관 CSV 필드 명세](docs/wr-import-field-spec.md)

## 실데이터 적재용 CSV 만들기

ubot 정제 인계본(`인계/data/`)을 [이관 CSV 필드 명세](docs/wr-import-field-spec.md)에 맞춰 4개 CSV로 변환합니다.

```bash
python3 scripts/build_import_csv.py --src "<ubot>/ubot db 구조화/인계/data"
```

- 출력: `data/import/` (`--out`으로 변경). `data/`는 `.gitignore`로 제외합니다. **실제 연락처와 평문 계정이 들어 있으므로 커밋하거나 공유하지 않습니다.**
- 대상: `migrate=1`이면서 병합되지 않은 업체, 그 업체의 담당자, 현행(`is_current=1`) 서비스와 그 상위 프로젝트입니다. 과거 배포 이력까지 넣으려면 `--include-history`를 붙입니다.
- 명세 9장의 적재 전 체크리스트를 자동으로 검증하며, 하나라도 실패하면 CSV를 쓰지 않고 종료 코드 1을 돌려줍니다.

적재 순서는 `company.csv`(`wr_company_t`) → `contact_module.csv`, `project_module.csv` → `service_module.csv`입니다. 서비스는 `parent_idx`가 가리키는 프로젝트가 먼저 있어야 합니다.
