#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""parse_bookmarks.py — 解析 Netscape 书签 HTML → 干净的 URL 清单

用法:
  python3 parse_bookmarks.py <bookmarks.html>
  python3 parse_bookmarks.py <bookmarks.html> --json   # JSON 输出
  python3 parse_bookmarks.py <bookmarks.html> --urls   # 只输出 URL（去重）

输出: 按文件夹分组：文件夹名 → [(title, url, add_date)]
"""

import argparse
import json
import re
import sys
from urllib.parse import urlparse


def parse_bookmarks(path: str):
    """解析 Netscape 书签文件，返回 (folder_tree, flat_urls)。"""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()

    # 去掉 base64 图标（占体积大头）
    html = re.sub(r'ICON="data:image/[^"]*"', "", html)

    # 栈式解析：DT H3=文件夹开始，/DL=文件夹结束，A=书签
    folders = []  # 当前文件夹栈
    tree = {}     # folder_path -> [(title, url, date)]
    flat = []     # 所有 URL（去重用）

    # 用行级扫描
    lines = html.splitlines()
    folder_stack = []
    current_path = None

    for line in lines:
        line = line.strip()
        # 文件夹开始 <DT><H3 ...>名称</H3>
        m = re.search(r"<DT><H3[^>]*>(.*?)</H3>", line, re.IGNORECASE)
        if m:
            name = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            folder_stack.append(name)
            current_path = "/".join(folder_stack)
            tree.setdefault(current_path, [])
            continue
        # 书签 <DT><A HREF="..." ...>标题</A>
        m = re.search(r'<DT><A HREF="([^"]+)"[^>]*>(.*?)</A>', line, re.IGNORECASE)
        if m:
            url = m.group(1).strip()
            title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            if not url or url.startswith("data:"):
                continue
            d = re.search(r'ADD_DATE="(\d+)"', line)
            date = d.group(1) if d else ""
            if current_path:
                tree.setdefault(current_path, []).append((title, url, date))
            flat.append((title, url, date, current_path or ""))
        # 文件夹结束 </DL>
        if re.search(r"</DL>", line, re.IGNORECASE):
            if folder_stack:
                folder_stack.pop()
            current_path = "/".join(folder_stack) if folder_stack else None

    return tree, flat


def main():
    parser = argparse.ArgumentParser(description="解析书签 HTML")
    parser.add_argument("path", help="书签文件路径")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--urls", action="store_true", help="只输出去重 URL")
    args = parser.parse_args()

    tree, flat = parse_bookmarks(args.path)

    if args.urls:
        seen = set()
        for _, url, _, _ in flat:
            host = urlparse(url).netloc
            if host not in seen:
                seen.add(host)
                print(url)
        return

    if args.json:
        out = {k: v for k, v in tree.items() if v}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return

    # 人类可读
    total = len(flat)
    print(f"共 {total} 条书签，{len([k for k in tree if tree[k]])} 个文件夹\n")
    for folder, items in tree.items():
        if not items:
            continue
        print(f"## {folder} ({len(items)})")
        for title, url, date in items[:8]:  # 每文件夹最多显示 8 条
            print(f"  - {title}")
            print(f"    {url}")
        if len(items) > 8:
            print(f"    ... 共 {len(items)} 条")
        print()


if __name__ == "__main__":
    main()
