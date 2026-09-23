---
id: overview-structure
title: 업체·담당자·프로젝트·서비스 데이터 구조
category: overview
summary: 우리기획 DB에서 업체는 wr_company_t, 담당자·프로젝트·서비스는 wr_module_t 게시판에 속한 wr_content_t 콘텐츠로 저장되는 구조와 고정 module_idx, company_idx·parent_idx 관계, 적재 순서를 설명한다.
keywords: [구조, 관계, ERD, wr_company_t, wr_content_t, wr_module_t, module_idx, company_idx, parent_idx, 담당자, 프로젝트, 서비스, 적재 순서, receiver_idx, ref_idx]
related_files: [docs/spec/import-csv-spec.md, scripts/build_import_csv.py]
last_updated: 2026-09-23
---

# 업체·담당자·프로젝트·서비스 데이터 구조

## 저장 위치

| 대상 | 저장 테이블 | 구분 방법 |
|---|---|---|
| 업체(고객사) | `wr_company_t` | 테이블 자체 |
| 담당자 | `wr_content_t` | `module_idx` = 담당자 게시판 |
| 프로젝트 | `wr_content_t` | `module_idx` = 프로젝트 게시판 |
| 서비스 | `wr_content_t` | `module_idx` = 서비스 게시판 |

업체는 콘텐츠 모듈이 **아니다.** "고객"은 `wr_company_t`의 업체를 말한다.
`wr_module_t`의 담당자·프로젝트·서비스 행은 콘텐츠가 아니라 **게시판 정의**이며, 콘텐츠의 `module_idx`는 그 게시판의 `idx`를 가리킨다.

## 고정 모듈 ID

| 모듈 | `wr_module_t.idx` |
|---|---|
| 담당자 | `01a05700-8c1d-7cd4-8b2d-fac77f865a9f` |
| 프로젝트 | `01a05701-ed99-7cfa-841e-ec6f6c9922a0` |
| 서비스 | `01a05702-067e-729b-85ab-deb5b0836082` |

## 관계

```text
wr_company_t (업체)
 ├─ 담당자 콘텐츠   company_idx → 업체.idx
 ├─ 프로젝트 콘텐츠 company_idx → 업체.idx
 └─ 서비스 콘텐츠   company_idx → 업체.idx
                    parent_idx  → 프로젝트.idx
```

- 모든 콘텐츠는 `company_idx`로 업체에 속한다.
- 서비스의 `parent_idx`는 프로젝트 귀속만 뜻한다. 서비스와 상위 프로젝트의 `company_idx`는 같아야 한다.
- 프로젝트 `ref_idx`는 현재 비어 있으며 관계에 쓰지 않는다.
- `receiver_idx`는 내부 member 연결값이다. 외부 고객 담당자는 담당자 콘텐츠로 관리한다.

## 데이터 보관 원칙

- 검색·관계·상태·기간에 필요한 값은 일반 필드에 둔다.
- `content_raw`는 서비스 계정 정보(`accounts`) 전용이다. 호스팅 주소는 FTP 계정의 `host`에 둔다.
- 계정을 가진 서비스는 모두 `is_hidden=1`이다.

필드별 규칙은 [이관 CSV 필드 명세](../spec/import-csv-spec.md)를 따른다.

## 적재 순서

```text
1. company.csv          → wr_company_t
2. contact_module.csv   → wr_content_t (담당자)
   project_module.csv   → wr_content_t (프로젝트)
3. service_module.csv   → wr_content_t (서비스, parent_idx 가 가리키는 프로젝트가 먼저 있어야 함)
```
