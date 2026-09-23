## 작업 리포트 — ubot 인계본 적재용 CSV 생성 스크립트

스크립트·문서만 바뀌어서 화면 캡처는 생략하고, 실행 결과로 증거를 대신합니다. 실데이터는 포함하지 않았습니다.

### 결정 사항
- PR #8 선병합 후 main 기준으로 작업
- 서비스는 현행(`is_current=1`)만 적재. 이력까지 넣으려면 `--include-history` 사용(285건)

### 변경
- `scripts/build_import_csv.py`: 인계본 `data/`에서 `docs/wr-import-field-spec.md` 규격대로 4개 CSV 투영 + 9장 체크리스트 자동 검증
- `.gitignore`: 출력 폴더 `data/` 제외
- `README.md`: 실행 방법·대상 기준·적재 순서

### 원천 선택 근거
ubot 최상위 wr CSV는 구 규격(`date_end=2999-12-31`, `status` 빈 값, 임의 `tags`·`content`, 병합 전 `company_idx`)이라, ubot README가 기준으로 명시한 `인계/data/`에서 직접 투영했습니다.

### 전후
| | 이전 | 이후 |
|---|---|---|
| 적재용 CSV | 없음(원천 그대로면 업체 451, 이관 제외·중복 포함) | 스크립트 1회 실행으로 생성 |
| 업체 | - | 212 |
| 담당자 | - | 117 |
| 프로젝트 | - | 234 |
| 서비스 | - | 234 (계정 보유 223) |

### 검증 (실행 로그)
```
company.csv           212행
contact_module.csv    117행
project_module.csv    234행
service_module.csv    234행
계정 보유 서비스      223건
검증 통과 → data/import
```
- 끊긴 `company_idx`·`parent_idx` 0건, 서비스↔상위 프로젝트 업체 불일치 0건
- `module_idx` 고정 ID 일치, 전 `idx` UUID v7, 서비스 전부 `is_hidden=1`
- `content_raw` 최상위 키 `accounts`만, 계정 키 `type/id/pw/url`만. 종류 FTP 209 · admin 190 · DB_iwinv 117 · DB 64
- `status`/`type` 미정값은 `0`: 서비스 status 0=73, type 0=8
- `git status`에 `data/` 미노출 확인

### 남은 점
- `url`이 빈 서비스 3건(인계본에 주소 없음)
- `docs/wr-content-module-fields.md` 예시 안내표에는 아직 `date_end=2999-12-31` 문구가 남아 있어 최신 명세(빈 값)와 다름 — 스크립트는 명세를 따름
