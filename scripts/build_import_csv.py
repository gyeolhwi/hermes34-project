#!/usr/bin/env python3
"""ubot 정제 인계본을 우리기획 적재용 CSV 4개로 투영한다.

규격: docs/wr-import-field-spec.md
입력: ubot 인계 패키지의 data/ 폴더 (company, contact, project, service,
      service_url, credential CSV)
출력: company.csv, contact_module.csv, project_module.csv, service_module.csv

출력에는 실제 연락처와 평문 계정이 들어간다. 저장소에 커밋하지 않는다.
"""

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

MODULE_CONTACT = "01a05700-8c1d-7cd4-8b2d-fac77f865a9f"
MODULE_PROJECT = "01a05701-ed99-7cfa-841e-ec6f6c9922a0"
MODULE_SERVICE = "01a05702-067e-729b-85ab-deb5b0836082"

COMPANY_FIELDS = [
    "idx", "company_name", "company_number", "company_phone", "company_email",
    "company_manager_name", "company_manager_phone", "company_manager_email",
    "company_address", "company_address_2", "company_extras", "tags", "admin_idx",
]
CONTACT_FIELDS = ["idx", "module_idx", "company_idx", "name", "content", "contact", "email"]
PROJECT_FIELDS = [
    "idx", "module_idx", "ref_idx", "company_idx", "title", "status", "date_start",
    "date_end", "type", "url", "tags", "receiver_idx", "is_hidden", "content_raw", "content",
]
SERVICE_FIELDS = [
    "idx", "module_idx", "parent_idx", "company_idx", "title", "status", "date_start",
    "date_end", "type", "url", "tags", "receiver_idx", "is_hidden", "content_raw", "content",
]

# 서비스 url 은 실제 서비스 도메인만, 호스팅 주소는 FTP 계정의 host 로 보낸다.
# repo·admin_tool·external 은 어느 쪽에도 넣지 않는다.
SERVICE_URL_ROLES = ["service"]
HOST_ROLES = ["hosting", "server_ip"]
ACCOUNT_TYPES = {"FTP", "DB_iwinv", "DB", "admin"}
ACCOUNT_KEYS = {"type", "host", "id", "pw", "url"}
UUID_V7 = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def read(src, name):
    with open(src / name, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(out, name, fields, rows):
    with open(out / name, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def code(value):
    """status·type 원본이 비었거나 unknown 이면 0."""
    value = (value or "").strip()
    return "0" if value in ("", "unknown") else value


def ordered_urls(urls, roles):
    """roles 순서 → 대표 주소 → seq 순으로 정렬하고 중복을 뺀다."""
    picked = sorted(
        (u for u in urls if u["url_role"] in roles),
        key=lambda u: (roles.index(u["url_role"]), u["is_primary"] != "1", int(u["seq"] or 0)),
    )
    seen = []
    for u in picked:
        if u["url"] not in seen:
            seen.append(u["url"])
    return seen


def account(cred, host):
    kind = cred["account_type"]
    url = cred["extra_url"].strip()
    if kind == "DB" and "iwinv" in url.lower():
        kind = "DB_iwinv"
    acc = {"type": kind}
    if kind != "FTP":
        host = ""
    for key, value in (("host", host), ("url", url), ("id", cred["account_id"]), ("pw", cred["password"])):
        if value:
            acc[key] = value
    return acc


def build(src, include_history):
    companies = read(src, "company.csv")
    live = {c["idx"]: c for c in companies if c["migrate"] == "1" and not c["merged_into"]}

    services = [
        s for s in read(src, "service.csv")
        if s["migrate"] == "1"
        and (include_history or s["is_current"] == "1")
        and s["company_idx"] in live
    ]
    project_ids = {s["project_idx"] for s in services}
    projects = [p for p in read(src, "project.csv") if p["idx"] in project_ids]
    contacts = [c for c in read(src, "contact.csv") if c["company_idx"] in live]

    urls = defaultdict(list)
    for u in read(src, "service_url.csv"):
        urls[u["service_idx"]].append(u)
    creds = defaultdict(list)
    for cred in read(src, "credential.csv"):
        creds[cred["service_idx"]].append(cred)

    company_rows = [{"idx": c["idx"], "company_name": c["company_name"]} for c in live.values()]
    contact_rows = [
        {
            "idx": c["idx"],
            "module_idx": MODULE_CONTACT,
            "company_idx": c["company_idx"],
            "name": c["name"],
            "contact": ", ".join(v for v in (c["phone"], c["phone_2"]) if v),
            "email": c["email"],
        }
        for c in contacts
    ]
    project_rows = [
        {
            "idx": p["idx"],
            "module_idx": MODULE_PROJECT,
            "company_idx": p["company_idx"],
            "title": p["title"],
            "status": code(p["status"]),
            "date_start": p["date_start"],
            "date_end": p["date_end"],
            "type": "0",
        }
        for p in projects
    ]
    service_rows = []
    for s in services:
        hosts = ordered_urls(urls[s["idx"]], HOST_ROLES)
        host = hosts[0] if hosts else ""
        accs = [account(cred, host) for cred in creds[s["idx"]]]
        service_rows.append({
            "idx": s["idx"],
            "module_idx": MODULE_SERVICE,
            "parent_idx": s["project_idx"],
            "company_idx": s["company_idx"],
            "title": s["title"],
            "status": code(s["status"]),
            "date_start": s["date_start"],
            "date_end": s["date_end"],
            "type": code(s["service_type"]),
            "url": ",".join(ordered_urls(urls[s["idx"]], SERVICE_URL_ROLES)),
            "is_hidden": "1",
            "content_raw": json.dumps({"accounts": accs}, ensure_ascii=False) if accs else "",
        })
    return company_rows, contact_rows, project_rows, service_rows


def validate(company_rows, contact_rows, project_rows, service_rows):
    """docs/wr-import-field-spec.md 9장 체크리스트. 실패 메시지 목록을 돌려준다."""
    errors = []
    company_ids = {r["idx"] for r in company_rows}
    project_ids = {r["idx"] for r in project_rows}

    tables = {
        "company": company_rows, "contact_module": contact_rows,
        "project_module": project_rows, "service_module": service_rows,
    }
    for name, rows in tables.items():
        ids = [r["idx"] for r in rows]
        if len(ids) != len(set(ids)):
            errors.append(f"{name}: idx 중복")
        bad = sum(not UUID_V7.match(i) for i in ids)
        if bad:
            errors.append(f"{name}: UUID v7 아닌 idx {bad}건")

    if any(not r["company_name"].strip() for r in company_rows):
        errors.append("company: 빈 company_name")
    if any(not r["name"].strip() for r in contact_rows):
        errors.append("contact_module: 빈 name")

    for name, rows, module in (
        ("contact_module", contact_rows, MODULE_CONTACT),
        ("project_module", project_rows, MODULE_PROJECT),
        ("service_module", service_rows, MODULE_SERVICE),
    ):
        if any(r["module_idx"] != module for r in rows):
            errors.append(f"{name}: module_idx 불일치")
        missing = sum(r["company_idx"] not in company_ids for r in rows)
        if missing:
            errors.append(f"{name}: 없는 company_idx {missing}건")

    missing = sum(r["parent_idx"] not in project_ids for r in service_rows)
    if missing:
        errors.append(f"service_module: 없는 parent_idx {missing}건")
    project_company = {r["idx"]: r["company_idx"] for r in project_rows}
    mismatch = sum(
        r["parent_idx"] in project_company and project_company[r["parent_idx"]] != r["company_idx"]
        for r in service_rows
    )
    if mismatch:
        errors.append(f"service_module: 상위 프로젝트와 업체 불일치 {mismatch}건")

    for name, rows in (("project_module", project_rows), ("service_module", service_rows)):
        for r in rows:
            if r["status"] in ("", "unknown") or r["type"] in ("", "unknown"):
                errors.append(f"{name}: status/type 미정 {r['idx']}")
            for d in (r["date_start"], r["date_end"]):
                if d and not DATE.match(d):
                    errors.append(f"{name}: 날짜 형식 {r['idx']}")

    for r in service_rows:
        if r["is_hidden"] != "1":
            errors.append(f"service_module: is_hidden!=1 {r['idx']}")
        if not r["content_raw"]:
            continue
        try:
            raw = json.loads(r["content_raw"])
        except json.JSONDecodeError:
            errors.append(f"service_module: content_raw JSON 오류 {r['idx']}")
            continue
        if set(raw) != {"accounts"} or not raw["accounts"]:
            errors.append(f"service_module: content_raw 최상위 키 {r['idx']}")
            continue
        for acc in raw["accounts"]:
            if set(acc) - ACCOUNT_KEYS or acc.get("type") not in ACCOUNT_TYPES:
                errors.append(f"service_module: 계정 키/종류 {r['idx']}")
        if any("host" in acc and acc["type"] != "FTP" for acc in raw["accounts"]):
            errors.append(f"service_module: FTP 외 계정에 host {r['idx']}")
        hosts = {acc.get("host") for acc in raw["accounts"] if acc["type"] == "FTP"}
        if len(hosts) > 1:
            errors.append(f"service_module: FTP 계정마다 host 다름 {r['idx']}")
        if hosts & set(r["url"].split(",")):
            errors.append(f"service_module: 호스팅 주소가 url 에 남음 {r['idx']}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--src", required=True, type=Path, help="ubot 인계 패키지의 data/ 폴더")
    parser.add_argument("--out", default=Path("data/import"), type=Path, help="출력 폴더 (기본 data/import)")
    parser.add_argument("--include-history", action="store_true", help="과거 배포 이력 서비스까지 포함")
    args = parser.parse_args()

    tables = build(args.src, args.include_history)
    errors = validate(*tables)
    if errors:
        for e in errors[:50]:
            print(f"✗ {e}", file=sys.stderr)
        print(f"검증 실패 {len(errors)}건 — CSV를 쓰지 않았습니다.", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    names = ("company.csv", "contact_module.csv", "project_module.csv", "service_module.csv")
    fields = (COMPANY_FIELDS, CONTACT_FIELDS, PROJECT_FIELDS, SERVICE_FIELDS)
    for name, field_list, rows in zip(names, fields, tables):
        write(args.out, name, field_list, rows)
        print(f"{name:<20} {len(rows):>4}행")
    with_accounts = sum(bool(r["content_raw"]) for r in tables[3])
    print(f"계정 보유 서비스     {with_accounts:>4}건")
    print(f"검증 통과 → {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
