#!/usr/bin/env python3
"""적재용 CSV 의 콘텐츠를 우리기획 API(POST /contents)로 적재한다.

모듈: project(프로젝트), contact(담당자), service(서비스)
요청 형식: docs/guides/post-contents.md
입력: build_import_csv.py 가 만든 <module>_module.csv
기본은 dry-run(보낼 JSON만 출력)이고, --send 를 줘야 실제로 보낸다.

API 주소와 키는 공개 저장소에 두지 않는다. WOORI_API_BASE_URL·WOORI_API_KEY 환경변수나
--base-url·--key 로 넘긴다.
"""

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

KST_OFFSET = timedelta(hours=9)
MODULES = ["project", "contact", "service"]


def to_utc(date):
    """YYYY-MM-DD 를 KST 자정으로 보고 UTC 로 바꾼다. 2022-12-20 → 2022-12-19T15:00:00"""
    return (datetime.strptime(date, "%Y-%m-%d") - KST_OFFSET).strftime("%Y-%m-%dT%H:%M:%S")


def put_if(body, key, value):
    """빈 값은 키 자체를 넣지 않는다."""
    if value not in ("", None):
        body[key] = value


def payload(module, row, args):
    body = {"idx": row["idx"], "module_idx": row["module_idx"]}
    if module == "service":
        body["parent_idx"] = row["parent_idx"]
    body["company_idx"] = row["company_idx"]

    if module == "contact":
        body[args.name_field] = row["name"]
        put_if(body, "contact", row["contact"])
        put_if(body, "email", row["email"])
        return body

    body["title"] = row["title"]
    body["status"] = int(row["status"])
    if module == "service":
        body["type"] = int(row["type"])
    if row["date_start"]:
        body["date_start"] = to_utc(row["date_start"])
    if row["date_end"]:
        body["date_end"] = to_utc(row["date_end"])
    if module == "service":
        put_if(body, "url", row["url"])
        if row["is_hidden"]:
            body["is_hidden"] = int(row["is_hidden"])
        if row["content_raw"]:
            raw = json.loads(row["content_raw"])
            body["content_raw"] = json.dumps(raw, ensure_ascii=False) if args.content_raw_as_string else raw
    return body


def post(base_url, key, body, timeout):
    req = urllib.request.Request(
        base_url.rstrip("/") + "/contents",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "accept": "application/json",
            "x-key": key,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return res.status, res.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError) as e:
        return None, str(getattr(e, "reason", e))


def label(module, row):
    return row["name"] if module == "contact" else row["title"]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("module", choices=MODULES)
    parser.add_argument("--csv", type=Path, help="기본값: data/import/<module>_module.csv")
    parser.add_argument("--base-url", default=os.environ.get("WOORI_API_BASE_URL", ""))
    parser.add_argument("--key", default=os.environ.get("WOORI_API_KEY", ""))
    parser.add_argument("--send", action="store_true", help="실제로 전송한다 (없으면 dry-run)")
    parser.add_argument("--only", action="append", default=[], metavar="IDX",
                        help="이 idx 행만 처리한다 (여러 번 지정 가능)")
    parser.add_argument("--skip", action="append", default=[], metavar="IDX",
                        help="이 idx 행은 건너뛴다 (여러 번 지정 가능)")
    parser.add_argument("--limit", type=int, help="앞에서부터 N행만 처리한다")
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--name-field", default="name", choices=["name", "title"],
                        help="담당자 이름을 보낼 키 (contact 전용)")
    parser.add_argument("--content-raw-as-string", action="store_true",
                        help="content_raw 를 JSON 객체 대신 문자열로 보낸다 (service 전용)")
    args = parser.parse_args()

    if args.send and not args.base_url:
        sys.exit("API 주소가 없다. WOORI_API_BASE_URL 환경변수나 --base-url 로 넘긴다.")
    if args.send and not args.key:
        sys.exit("API 키가 없다. WOORI_API_KEY 환경변수나 --key 로 넘긴다.")

    csv_path = args.csv or Path(f"data/import/{args.module}_module.csv")
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if args.only:
        rows = [r for r in rows if r["idx"] in args.only]
    if args.skip:
        rows = [r for r in rows if r["idx"] not in args.skip]
    if args.limit is not None:
        rows = rows[:args.limit]

    if not args.send:
        for row in rows:
            print(json.dumps(payload(args.module, row, args), ensure_ascii=False))
        print(f"dry-run: {args.module} {len(rows)}건. 전송하려면 --send", file=sys.stderr)
        return

    failed = []
    for i, row in enumerate(rows, 1):
        status, text = post(args.base_url, args.key, payload(args.module, row, args), args.timeout)
        ok = status is not None and 200 <= status < 300
        print(f"[{i}/{len(rows)}] {'OK ' if ok else 'ERR'} {status or '-'} {row['idx']} {label(args.module, row)}")
        if not ok:
            print(f"    {text[:300]}")
            failed.append(row["idx"])

    print(f"\n전송 {len(rows)}건 / 성공 {len(rows) - len(failed)} / 실패 {len(failed)}")
    if failed:
        print("실패 idx (재시도: --only <idx>):")
        for idx in failed:
            print(f"  {idx}")
        sys.exit(1)


if __name__ == "__main__":
    main()
