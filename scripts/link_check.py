#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""link_check.py — 链接危险识别（入口 + 编排）

用法:
  python3 link_check.py <url>              # 静态特征检测 + 跳转链展开
  python3 link_check.py <url> --no-follow  # 只做静态检测，不展开跳转

模块分工:
  link_rules.py   — 规则数据（TLD/品牌/白名单/关键词/阈值）——维护规则只改它
  link_checks.py  — 检查器函数（每个判定维度一个函数，可独立测试）
  threatbook.py   — 微步威胁情报核验（可选增强，无 key 静默跳过）
  link_check.py   — 编排 + CLI（本文件）

判定维度:
  1. URL 结构异常（@伪装 / IP直连 / 端口异常 / punycode）
  2. TLD 风险（免费/滥用高发后缀）
  3. 品牌仿冒（leetspeak 替换 + fuzzy 相似）
  4. 危险关键词（login/verify/payment 等在陌生域名）
  5. 短链识别（t.cn/dwz.cn/bit.ly 等 → 必须展开看真实目标）
  6. 跳转偏离（最终目标 ≠ 原始域名，单条即红）
  7. 随机短域名（注册域 ≤6 字符随机串直连落地）
  8. 非 HTTPS
  9. 微步威胁情报（可选）

输出: 风险评分 + 分级（🟢低 / 🟡中 / 🔴高）+ 逐条命中理由
"""

import argparse
import difflib
import ipaddress
import json
import re
import subprocess
import sys
from urllib.parse import urlparse, unquote

from link_rules import SCORE_HIGH, SCORE_MED
from link_checks import (
    host_in, check_scheme, check_at_sign, check_ip_direct, check_port,
    check_punycode, check_tld, check_brand, check_keywords, check_shortener,
    check_redirect, check_random_domain, check_threatbook_domain,
    check_threatbook_url,
)


# ───────────────── 工具函数 ─────────────────

def normalize(s: str) -> str:
    """去数字字母外字符，供相似度比较。"""
    return re.sub(r"[^a-z0-9]", "", s.lower())


# leetspeak 替换表：钓鱼仿冒常用数字替字母（ta0ba0→taobao, p4ypal→paypal）
LEET = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t", "8": "b"})


def deleet(s: str) -> str:
    return s.lower().translate(LEET)


def is_ip(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def brand_lookup(host: str):
    """域名 vs 品牌匹配。两级：
       1) leetspeak 替换后包含品牌词（ta0ba0→taobao 命中）
       2) 相似度 >= 0.75（fuzzy）
    返回 (品牌, 匹配方式, 是否白名单域名)。
    """
    from link_rules import BRANDS, BRAND_DOMAINS, BRAND_SUFFIX_WHITELIST
    host_clean = normalize(host)
    host_deleet = deleet(host)
    if not host_clean:
        return None

    # 一级：leetspeak 替换后包含品牌词（数字品牌 139 不受 deleet 变形影响——原串也查）
    for brand in BRANDS:
        if len(brand) >= 3 and (brand in host_deleet or brand in host_clean):
            # 生态域名豁免：品牌词出现在白名单后缀里 → 不算仿冒
            if any(host.endswith("." + s) or host == s for s in BRAND_SUFFIX_WHITELIST):
                return (brand, "contains", True)
            whitelist = BRAND_DOMAINS.get(brand, "")
            # 域边界匹配（防 abchina.com.evil.com 子串误判官方）：等于官方域或在其子域下
            is_white = bool(whitelist) and (host == whitelist or host.endswith("." + whitelist))
            return (brand, "contains", is_white)

    # 二级：fuzzy 相似度
    best = None
    best_ratio = 0.0
    for brand in BRANDS:
        ratio = difflib.SequenceMatcher(None, host_clean, brand).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best = brand
    if best_ratio >= 0.75 and best is not None:
        whitelist = BRAND_DOMAINS.get(best, "")
        is_white = bool(whitelist) and (host == whitelist or host.endswith("." + whitelist))
        return (best, "fuzzy", is_white)
    return None


def follow_redirects(url: str, timeout: int = 12) -> list:
    """展开跳转链，返回 [原始, 中间..., 最终]。失败返回空列表。"""
    try:
        r = subprocess.run(
            ["curl", "-sIL", "--max-time", str(timeout),
             "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
             "-o", "/dev/null", "-w", "%{url_effective} %{num_redirects} %{http_code}",
             url],
            capture_output=True, text=True, timeout=timeout + 5,
        )
        if r.returncode != 0:
            return []
        parts = r.stdout.strip().split()
        if not parts:
            return []
        final_url = parts[0]
        num = int(parts[1]) if len(parts) > 1 else 0
        if num == 0 or final_url == url:
            return [url]
        # 只有最终地址；跳转中间链用 -w %{redirect_url} 拿不到，重跑拿完整链
        r2 = subprocess.run(
            ["curl", "-sIL", "--max-time", str(timeout),
             "-A", "Mozilla/5.0", url],
            capture_output=True, text=True, timeout=timeout + 5,
        )
        chain = [url]
        for line in r2.stdout.splitlines():
            if line.lower().startswith("location:"):
                loc = line.split(":", 1)[1].strip()
                chain.append(loc)
        if chain[-1] != final_url:
            chain.append(final_url)
        return chain
    except Exception:
        return []


# ───────────────── 编排 ─────────────────

def analyze(url: str, follow: bool = True) -> dict:
    parsed = urlparse(url if "://" in url else "http://" + url)
    host = parsed.hostname or ""
    ctx = {
        "url": url,
        "scheme": parsed.scheme.lower(),
        "host": host,
        "host_lower": host.lower(),
        "port": parsed.port,
        "path": unquote(parsed.path),
        "tld": host.rsplit(".", 1)[-1].lower() if "." in host else "",
        "is_ip": is_ip(host),
        "brand": brand_lookup(host),
    }

    findings = []
    score = 0

    # 静态维度（顺序敏感：品牌/短链先跑，供后续豁免）
    for check in (check_scheme, check_at_sign, check_ip_direct, check_port,
                  check_punycode, check_tld, check_brand, check_keywords,
                  check_shortener):
        findings, score = check(ctx, findings, score)

    # 动态维度（跳转展开）
    findings, score = check_redirect(ctx, findings, score, follow=follow)
    findings, score = check_random_domain(ctx, findings, score)

    # 威胁情报（可选）
    findings, score = check_threatbook_domain(ctx, findings, score)
    findings, score = check_threatbook_url(ctx, findings, score, follow=follow)

    # 分级
    if score >= SCORE_HIGH:
        level = "🔴 高"
    elif score >= SCORE_MED:
        level = "🟡 中"
    else:
        level = "🟢 低"

    return {
        "url": url,
        "score": score,
        "level": level,
        "host": host,
        "tld": ctx["tld"],
        "findings": findings,
    }


def render(result: dict) -> str:
    lines = []
    lines.append(f"🔗 链接审核: {result['level']}（评分 {result['score']}）")
    lines.append(f"   目标: {result['url']}")
    lines.append(f"   域名: {result['host']}（TLD: .{result['tld']}）")
    lines.append("")
    lines.append("命中项:")
    if not result["findings"]:
        lines.append("   无异常特征")
    for level, tag, msg in result["findings"]:
        icon = {"high": "🔴", "warn": "🟡", "info": "ℹ️"}.get(level, "ℹ️")
        lines.append(f"   {icon} [{tag}] {msg}")
    lines.append("")
    lines.append("建议: " + {
        "🔴 高": "不要点击/不要输入任何信息。如已访问过，立即修改相关账号密码。",
        "🟡 中": "谨慎处理——先核实来源，短链务必看真实目标，陌生站点不输凭据。",
        "🟢 低": "未见明显风险特征，可正常访问。",
    }[result["level"]])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="链接危险识别")
    parser.add_argument("url", help="要审核的链接")
    parser.add_argument("--no-follow", action="store_true", help="只做静态检测，不展开跳转")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    result = analyze(args.url, follow=not args.no_follow)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render(result))
    sys.exit(0 if result["score"] < SCORE_MED else 1)


if __name__ == "__main__":
    main()
