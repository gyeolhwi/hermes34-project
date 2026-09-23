# 제공 서비스 시트 → 업체·프로젝트·서비스 매핑

| 대상 | 소속·관계 | 핵심 필드 |
|---|---|---|
| 업체 | `wr_company_t.idx` | `company_name`, 업체 연락처·주소·대표 담당자 |
| 담당자 | `company_idx=업체.idx` | `name`, `contact`, `email`, `content` |
| 프로젝트 | `company_idx=업체.idx` | `title`, `status`, `date_start`, `date_end`, `ref_idx` |
| 서비스 | `company_idx=업체.idx`, `parent_idx=프로젝트.idx` | `title`, `status`, `type`, `url`, `tags`, `is_hidden=1` |

서비스 URL은 `도메인주소,호스팅주소`로 저장하고, 서비스 접속·DB 정보는 `content_raw.accounts[]`에 보관합니다. 실제 비밀번호나 고객 연락처를 문서 예시로 복사하지 않습니다.
