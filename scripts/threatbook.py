#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""threatbook.py — 微步在线威胁情报核验（可选增强，独立模块）

有 THREATBOOK_API_KEY 才调用；无 key / 无 requests / 网络失败 → 返回 {} 静默跳过。
被 link_check.py import。
"""

import os
import subprocess

THREATBOOK_BASE = "https://api.threatbook.cn/v3"
THREATBOOK_KEY_ENV = "THREATBOOK_API_KEY"

try:
    import requests  # noqa: F401
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def get_key() -> str:
    """从环境变量或 credman 读微步 API key。无 key 返回空串（跳过情报核验）。"""
    key = os.environ.get(THREATBOOK_KEY_ENV, "")
    if key:
        return key
    try:
        credman = os.environ.get("CREDMAN_BIN", "credman")   # 凭据工具：换环境用环境变量指路径
        r = subprocess.run([credman, "get", "THREATBOOK_API_KEY"],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:
        pass
    return ""


def domain_report(domain: str, key: str) -> dict:
    """微步域名分析：威胁情报、恶意标签、judgments。失败返回 {}。"""
    if not HAS_REQUESTS or not key:
        return {}
    try:
        import requests as _req
        r = _req.get(f"{THREATBOOK_BASE}/domain/query",
                     params={"apikey": key, "resource": domain, "lang": "zh"},
                     timeout=10)
        data = r.json()
        verdict = data.get("data", {})
        if not verdict:
            return {}
        return {
            "source": "threatbook",
            "malicious": verdict.get("is_malicious", 0),
            "confidence": verdict.get("confidence_level", ""),
            "judgments": verdict.get("judgments", []),
            "threat_types": verdict.get("threat_types", []),
            "tags": verdict.get("tags", [])[:8],
            "categories": verdict.get("categories", [])[:5],
            "whois_registrar": (verdict.get("cur_whois") or {}).get("registrar", ""),
        }
    except Exception:
        return {}


def url_report(url: str, key: str) -> dict:
    """微步 URL 信誉报告：扫描引擎判定 + 检测结果。失败返回 {}。"""
    if not HAS_REQUESTS or not key:
        return {}
    try:
        import requests as _req
        r = _req.get(f"{THREATBOOK_BASE}/url/report",
                     params={"apikey": key, "url": url},
                     timeout=10)
        data = r.json()
        verdict = data.get("data", {})
        if not verdict:
            return {}
        return {
            "source": "threatbook",
            "detection": verdict.get("detection", ""),
            "engines_total": verdict.get("total_engines", 0),
            "engines_hit": verdict.get("detected_engines", 0),
            "threat_type": verdict.get("threat_type", ""),
            "categories": verdict.get("categories", [])[:8],
        }
    except Exception:
        return {}
