#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""batch_check.py — 批量链接风险扫描

用法:
  python3 batch_check.py <urls.txt>              # 扫描文件里的 URL（每行一个）
  python3 batch_check.py <urls.txt> --no-follow  # 只静态检测（不碰目标站）
  cat urls.txt | python3 batch_check.py -        # 从 stdin 读
  python3 batch_check.py <urls.txt> --json       # JSON 汇总输出

输出: 高/中/低分组 + 每个 URL 的评分与命中项
"""

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from link_check import analyze

MAX_WORKERS = 8


def load_urls(path: str) -> list:
    if path == "-":
        return [l.strip() for l in sys.stdin if l.strip()]
    with open(path, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


def scan_one(url: str, follow: bool) -> dict:
    try:
        return analyze(url, follow=follow)
    except Exception as e:
        return {"url": url, "score": 999, "level": "❌ 异常", "host": "?", "tld": "?",
                "findings": [("high", "error", f"扫描异常: {e}")]}


def main():
    parser = argparse.ArgumentParser(description="批量链接风险扫描")
    parser.add_argument("path", help="URL 列表文件（每行一个，- 表示 stdin）")
    parser.add_argument("--no-follow", action="store_true", help="只静态检测，不展开跳转")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--workers", type=int, default=MAX_WORKERS, help="并发数（默认 8）")
    args = parser.parse_args()

    urls = load_urls(args.path)
    follow = not args.no_follow
    print(f"扫描 {len(urls)} 个 URL（并发 {args.workers}，follow={follow}）...", file=sys.stderr)

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(scan_one, u, follow): u for u in urls}
        for fut in as_completed(futures):
            results.append(fut.result())

    # 排序：高 → 中 → 低（按评分降序）
    order = {"🔴 高": 0, "🟡 中": 1, "🟢 低": 2, "❌ 异常": 3}
    results.sort(key=lambda r: (order.get(r["level"], 3), -r["score"]))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
        return

    high = [r for r in results if r["level"] == "🔴 高"]
    mid = [r for r in results if r["level"] == "🟡 中"]
    low = [r for r in results if r["level"] == "🟢 低"]
    err = [r for r in results if r["level"] == "❌ 异常"]
    print(f"\n🔴 高 {len(high)} | 🟡 中 {len(mid)} | 🟢 低 {len(low)} | ❌ {len(err)}")

    for label, bucket in (("=== 🔴 高风险 ===", high), ("=== 🟡 中风险 ===", mid)):
        if not bucket:
            continue
        print(f"\n{label}")
        for r in bucket:
            print(f"  [{r['score']}] {r['url']}")
            for lvl, tag, msg in r["findings"]:
                if lvl != "info":
                    print(f"      {msg[:100]}")
    if err:
        print("\n=== ❌ 异常 ===")
        for r in err:
            print(f"  {r['url']}: {r['findings'][0][2] if r['findings'] else '?'}")


if __name__ == "__main__":
    main()
