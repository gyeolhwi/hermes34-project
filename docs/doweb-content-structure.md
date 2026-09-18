# 업체 기반 `wr_content_t` 적재 규격

## 모듈과 콘텐츠

`wr_module_t`에서 담당자·프로젝트·서비스 게시판을 만들고, 각 게시판의 콘텐츠를 `wr_content_t`에 적재합니다. 업체는 콘텐츠 모듈이 아니라 `wr_company_t`에 생성합니다.

```text
업체 생성 → 담당자/프로젝트/서비스 콘텐츠 적재
프로젝트 생성 → 서비스.parent_idx에 프로젝트.idx 설정
```

모든 담당자·프로젝트·서비스 콘텐츠는 `company_idx`로 업체에 귀속됩니다. 서비스의 `parent_idx`는 프로젝트 귀속만 표현합니다.

## 데이터 보관

- 일반 필드: 제목, 상태, 기간, 구분, URL, 태그, 관계값
- `content_raw`: 검색 불필요하거나 보호가 필요한 JSON 값
- 서비스 접속정보: `content_raw.accounts[]`
- 서비스 `is_hidden`: `1`
- 외부 담당자: 담당자 모듈의 `name`, `contact`, `email`; `receiver_idx`와 구분
