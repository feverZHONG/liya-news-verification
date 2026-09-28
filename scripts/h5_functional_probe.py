#!/usr/bin/env python3
"""H5/交互页「还能用吗」功能实测（linkcheck 之后的第二层）。

用法：
    python3 scripts/h5_functional_probe.py <url> [--click '#sel1,#sel2'] [--wait 6] [--ua mobile|desktop]

干什么：无头浏览器真跑一遍，抓 ① 全部网络请求（含媒体文件与状态码）② 控制台报错
        ③ 页面上 <video>/<audio> 的 currentSrc/paused/readyState/duration。
判读：
    - 资源 200 + media 请求出现 + video.paused=false & readyState>=3 → 「真能用」
    - 只有 HTML/CSS 200、媒体请求始终不出现 → 多半是空壳/接口已废（按钮还在 ≠ 有效）
    - 只有 4xx 的 js（如 share.js 404）→ 该模块已丢，主流程可能仍活，要看媒体有没有播起来

⚠️ 本机坑：playwright 包与已装浏览器**版本号常常对不上**（例：包要 chromium_headless_shell-1228，
   实际只装了 -1243）→ launch 直接报 "Executable doesn't exist"。
   解法：列出 /opt/hermes/.playwright/ 里真实的 chromium_headless_shell-* 目录，把
   .../chrome-headless-shell-linux64/chrome-headless-shell 作为 executable_path 传进去（脚本已自动探测）。
"""
import argparse
import glob
import json
import os
import sys


def find_headless_shell():
    cands = sorted(glob.glob("/opt/hermes/.playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell"))
    for c in reversed(cands):
        if os.access(c, os.X_OK):
            return c
    return None


MOBILE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
             "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--click", default="", help="逗号分隔的 CSS 选择器，依次点击（如 '#weiBoBtn,#btn'）")
    ap.add_argument("--wait", type=float, default=6.0, help="最后再等多久（秒）看媒体是否起播")
    ap.add_argument("--ua", default="mobile", choices=["mobile", "desktop"])
    ap.add_argument("--timeout", type=int, default=45)
    a = ap.parse_args()

    from playwright.sync_api import sync_playwright

    exe = find_headless_shell()
    reqs, errs = [], []
    with sync_playwright() as p:
        kw = {"headless": True, "args": ["--no-sandbox", "--disable-blink-features=AutomationControlled"]}
        if exe:
            kw["executable_path"] = exe
        b = p.chromium.launch(**kw)
        ctx = b.new_context(
            viewport={"width": 390, "height": 844} if a.ua == "mobile" else {"width": 1440, "height": 900},
            is_mobile=(a.ua == "mobile"),
            user_agent=MOBILE_UA if a.ua == "mobile" else None,
        )
        pg = ctx.new_page()
        pg.on("request", lambda r: reqs.append(("REQ", r.url, r.resource_type)))
        pg.on("response", lambda r: reqs.append(("RES", r.url, str(r.status))))
        pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:200]))
        pg.on("console", lambda m: errs.append("console.error: " + m.text[:160]) if m.type == "error" else None)
        try:
            pg.goto(a.url, wait_until="load", timeout=a.timeout * 1000)
        except Exception as e:
            print("goto err:", str(e)[:200])
        pg.wait_for_timeout(2500)
        for sel in [s.strip() for s in a.click.split(",") if s.strip()]:
            try:
                el = pg.query_selector(sel)
                if el:
                    el.click(timeout=3000)
                    pg.wait_for_timeout(2000)
                    print("clicked:", sel)
                else:
                    print("no such element:", sel)
            except Exception as e:
                print("click", sel, "err:", str(e)[:120])
        pg.wait_for_timeout(int(a.wait * 1000))
        media = pg.eval_on_selector_all(
            "video,audio",
            "els => els.map(e => ({tag: e.tagName, src: e.currentSrc || e.src, paused: e.paused, rs: e.readyState, dur: e.duration}))",
        )
        print("TITLE:", pg.title())
        print("MEDIA:", json.dumps(media, ensure_ascii=False))
        print("ERRORS:", json.dumps(errs[:8], ensure_ascii=False))
        print("NET(bad + media):")
        seen = set()
        for kind, u, extra in reqs:
            bad = kind == "RES" and extra and extra[0] in "45"
            is_media = any(k in u for k in (".mp4", ".m3u8", ".mp3", ".m4a"))
            if (bad or is_media) and (u, kind) not in seen:
                seen.add((u, kind))
                print("  ", kind, extra, u[:160])
        print("REQ total:", sum(1 for k, _, _ in reqs if k == "REQ"))
        b.close()


if __name__ == "__main__":
    sys.exit(main())
