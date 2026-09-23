## 작업 리포트 — 호스팅 주소를 accounts.host로 분리

스크립트·문서만 바뀌어서 화면 캡처 대신 실행 결과로 증거를 남깁니다. 실데이터는 포함하지 않았습니다.

### 결정
- `host`는 FTP·DB·admin **모든 계정**에 넣음(사용자 확인)
- 호스팅 주소 = `service_url.url_role=hosting`, 없으면 `server_ip`. 서비스당 최대 1개
- DB 계정의 `url`(phpMyAdmin 등)은 유지

### 전후 (인계본 실데이터, 현행 서비스 234건)
| | 이전 | 이후 |
|---|---|---|
| 서비스 `url`에 호스팅 주소 포함 | 146건(`도메인,호스팅` 형태) | 0건 |
| `url`에 쉼표가 있는 서비스 | 146 | 9(서비스 도메인이 2개인 원본) |
| 계정에 `host` 있는 서비스 | 0 | 137 |
| 한 서비스 안에서 `host`가 다른 계정 | - | 0 |
| 행 수 | 212/117/234/234 | 212/117/234/234 (변화 없음) |

- 계정은 있는데 호스팅 주소가 없는 서비스는 `host` 키 생략
- 스크립트 검증에 11번 항목 추가: 한 서비스의 계정 `host`가 모두 같고, 그 값이 서비스 `url`에 없을 것 → 통과
- 참고: `bslchurch.doweb.kr`은 이 서비스에서는 실제 도메인이고, 다른 서비스에서 호스팅 주소로 쓰임(원본 역할 기준 정상)

### 변경 파일
- `scripts/build_import_csv.py` — url은 `service` 역할만, 계정에 `host`, 허용 키에 `host` 추가, 검증 추가
- `docs/wr-import-field-spec.md` — 서비스 `url` 정의, `accounts[].host` 필드·예시, 체크리스트 10·11번
- `docs/wr-content-module-fields.md`, `docs/service-sheet-api-field-mapping.md` — `도메인주소,호스팅주소` 문구 정정
- `examples/service_module_example.csv` — `url`은 도메인만, 계정에 `host` 추가
