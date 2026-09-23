# Hermes34 → 우리기획 데이터 적재

ubot 정제 인계본(서비스 관리대장 정리본)을 우리기획 DB의 `wr_company_t`와 `wr_content_t`에 넣을 CSV로 만드는 저장소입니다.

## 한눈에 보기

```text
wr_company_t (업체 = 고객사)
 ├─ wr_content_t 담당자   company_idx → 업체
 ├─ wr_content_t 프로젝트 company_idx → 업체
 └─ wr_content_t 서비스   company_idx → 업체, parent_idx → 프로젝트
```

| 모듈 | `module_idx` |
|---|---|
| 담당자 | `01a05700-8c1d-7cd4-8b2d-fac77f865a9f` |
| 프로젝트 | `01a05701-ed99-7cfa-841e-ec6f6c9922a0` |
| 서비스 | `01a05702-067e-729b-85ab-deb5b0836082` |

- 서비스 `url`에는 실제 서비스 도메인만 넣습니다.
- 서비스 계정은 `content_raw.accounts[]`에 넣고, 호스팅 주소는 **FTP 계정의 `host`** 에만 넣습니다.
- 계정을 가진 서비스는 `is_hidden=1`입니다.

## 빠른 시작

```bash
python3 scripts/build_import_csv.py --src "<ubot>/ubot db 구조화/인계/data"
```

`data/import/`에 CSV 4개가 생깁니다. 적재 순서는 `company.csv` → `contact_module.csv`·`project_module.csv` → `service_module.csv`입니다.

> ⚠ 출력에는 실제 연락처와 평문 비밀번호가 들어 있습니다. `data/`는 git에서 제외되어 있으며, 공개 저장소이므로 절대 커밋하지 않습니다.

## 문서

모든 문서 목록과 요약은 [INDEX.md](INDEX.md)에 있습니다.

| 알고 싶은 것 | 문서 |
|---|---|
| 테이블·모듈 관계, 적재 순서 | [데이터 구조](docs/overview/structure.md) |
| 필드별 규칙, `accounts`·`host`, 검증 체크리스트 | [이관 CSV 필드 명세](docs/spec/import-csv-spec.md) (기준 문서) |
| 스크립트 실행·옵션·보안 | [적재용 CSV 생성 가이드](docs/guides/build-import-csv.md) |

## 폴더 구조

```text
.
├── README.md                 이 파일
├── INDEX.md                  문서 색인 (path·title·summary·keywords)
├── docs/
│   ├── overview/structure.md       데이터 구조
│   ├── spec/import-csv-spec.md     CSV 필드 명세
│   └── guides/build-import-csv.md  스크립트 가이드
├── examples/                 가짜 값 예시 CSV 4개
├── scripts/build_import_csv.py
└── data/                     (git 제외) 생성된 실데이터 CSV
```
