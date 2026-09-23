## 작업 리포트 — accounts.host를 FTP 계정에만 기록

스크립트·문서만 바뀌어서 실행 결과로 증거를 남깁니다. 실데이터는 포함하지 않았습니다.

### 전후 (실데이터, `host`가 있는 계정 수)
| 계정 종류 | 이전 | 이후 |
|---|---|---|
| FTP | 134 | 134 |
| DB · DB_iwinv | 121 | 0 |
| admin | 125 | 0 |

- 행 수 212/117/234/234 유지, 스크립트 검증 통과
- 검증 11번 강화: FTP 외 계정에 `host`가 있으면 실패, 한 서비스의 FTP `host`는 모두 같아야 함
- FTP 계정이 없는 서비스 3건은 호스팅 주소가 CSV에서 빠짐(인계본에는 남아 있음)

### 변경 파일
- `scripts/build_import_csv.py` — `account()`에서 FTP만 `host`, 검증 수정
- `docs/wr-import-field-spec.md`, `docs/wr-content-module-fields.md`, `docs/service-sheet-api-field-mapping.md` — FTP 전용 규칙으로 정정
- `examples/service_module_example.csv` — DB·admin 예시에서 `host` 제거
