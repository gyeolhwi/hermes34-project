#!/usr/bin/env python3
"""project_module.csv 의 프로젝트를 우리기획 API(POST /contents)로 적재한다.

요청 형식: project_post_sample.md 의 curl 예시
입력: build_import_csv.py 가 만든 project_module.csv
기본은 dry-run(보낼 JSON만 출력)이고, --send 를 줘야 실제로 보낸다.

API 키는 공개 저장소에 두지 않는다. WOORI_API_KEY 환경변수나 --key 로 넘긴다.
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

DEFAULT_BASE_URL = "https://woori-dev.doweb.kr:3000"
KST_OFFSET = timedelta(hours=9)


def to_utc(date):
    """YYYY-MM-DD 를 KST 자정으로 보고 UTC 로 바꾼다. 2022-12-20 → 2022-12-19T15:00:00"""
    return (datetime.strptime(date, "%Y-%m-%d") - KST_OFFSET).strftime("%Y-%m-%dT%H:%M:%S")


def payload(row):
    body = {
        "idx": row["idx"],
        "module_idx": row["module_idx"],
        "company_idx": row["company_idx"],
        "title": row["title"],
        "status": int(row["status"]),
    }
    if row.get("date_start"):
        body["date_start"] = to_utc(row["date_start"])
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


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--csv", type=Path, default=Path("data/import/project_module.csv"))
    parser.add_argument("--base-url", default=os.environ.get("WOORI_API_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--key", default=os.environ.get("WOORI_API_KEY", ""))
    parser.add_argument("--send", action="store_true", help="실제로 전송한다 (없으면 dry-run)")
    parser.add_argument("--only", action="append", default=[], metavar="IDX",
                        help="이 idx 행만 처리한다 (여러 번 지정 가능)")
    parser.add_argument("--limit", type=int, help="앞에서부터 N행만 처리한다")
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()

    if args.send and not args.key:
        sys.exit("API 키가 없다. WOORI_API_KEY 환경변수나 --key 로 넘긴다.")

    with open(args.csv, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if args.only:
        rows = [r for r in rows if r["idx"] in args.only]
    if args.limit is not None:
        rows = rows[:args.limit]

    if not args.send:
        for row in rows:
            print(json.dumps(payload(row), ensure_ascii=False))
        print(f"dry-run: {len(rows)}건. 전송하려면 --send", file=sys.stderr)
        return

    failed = []
    for i, row in enumerate(rows, 1):
        status, text = post(args.base_url, args.key, payload(row), args.timeout)
        ok = status is not None and 200 <= status < 300
        print(f"[{i}/{len(rows)}] {'OK ' if ok else 'ERR'} {status or '-'} {row['idx']} {row['title']}")
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
