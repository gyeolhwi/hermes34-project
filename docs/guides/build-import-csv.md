---
id: guide-build-import-csv
title: 적재용 CSV 생성 가이드
category: guide
summary: scripts/build_import_csv.py로 ubot 정제 인계본(인계/data)을 적재용 CSV 4개로 변환하는 방법 — 실행 명령, 옵션(--out, --include-history), 대상 선택 기준과 현재 건수, 자동 검증과 실패 시 동작, 실데이터 보안 주의사항.
keywords: [build_import_csv.py, 스크립트, 실행 방법, 인계본, ubot, data/import, --include-history, 현행 서비스, 검증 실패, 건수, 보안, gitignore, 평문 비밀번호]
related_files: [scripts/build_import_csv.py, .gitignore, docs/spec/import-csv-spec.md]
last_updated: 2026-09-23
---

# 적재용 CSV 생성 가이드

## 실행

```bash
python3 scripts/build_import_csv.py --src "<ubot>/ubot db 구조화/인계/data"
```

Python 3 표준 라이브러리만 쓴다. 입력은 ubot 인계 패키지의 `data/` 폴더(`company`, `contact`, `project`, `service`, `service_url`, `credential` CSV)다.

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--src` | 없음(필수) | 인계본 `data/` 폴더 |
| `--out` | `data/import` | 출력 폴더 |
| `--include-history` | 꺼짐 | 과거 배포 이력(`is_current=0`) 서비스까지 포함 |

## 출력

| 파일 | 적재 대상 | 2026-09-23 기준 행 수 |
|---|---|---|
| `company.csv` | `wr_company_t` | 212 |
| `contact_module.csv` | 담당자 콘텐츠 | 117 |
| `project_module.csv` | 프로젝트 콘텐츠 | 234 |
| `service_module.csv` | 서비스 콘텐츠 | 234 (계정 보유 223) |

대상 선택 기준과 필드 변환 규칙은 [이관 CSV 필드 명세](../spec/import-csv-spec.md)의 1장·10장에 있다. 적재 순서는 [데이터 구조](../overview/structure.md)를 따른다.

## 검증

스크립트는 CSV를 쓰기 전에 명세 9장 체크리스트를 자동으로 검사한다.

- 통과: 파일을 쓰고 파일별 행 수를 출력한다.
- 실패: 파일을 **쓰지 않고** 실패 항목을 출력한 뒤 종료 코드 `1`을 돌려준다.

## 보안

- 출력에는 실제 연락처와 **평문 비밀번호**가 들어 있다.
- `data/`는 `.gitignore`로 제외되어 있다. 이 저장소는 공개 저장소이므로 출력 파일을 커밋하거나 공유하지 않는다.
- 문서·예시에는 실제 값을 복사하지 않는다. 예시는 `examples/`의 가짜 값만 쓴다.
