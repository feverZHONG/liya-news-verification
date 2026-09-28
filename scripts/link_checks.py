#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""link_checks.py — 链接判定检查器（每个维度一个独立函数）

设计：每个检查器输入 (ctx, findings, score)，返回 (findings, score) 增量。
ctx 是 analyze 预解析的上下文 dict（url/scheme/host/path/tld 等）。
被 link_check.py import，可独立测试。

约定：findings 元素 = (level, tag, message)，level ∈ {high, warn, info}
"""

from urllib.parse import urlparse

from link_rules import (
    HIGH_RISK_TLDS, BRANDS, BRAND_DOMAINS, BRAND_SUFFIX_WHITELIST,
    SHORTENER_DOMAINS, TRUSTED_SHORTENER_MAP, TRUSTED_REDIRECT_HOSTS,
    RISKY_HOST_KEYWORDS, RISKY_PATH_KEYWORDS, SCORE_MED,
)
import threatbook


def host_in(host: str, domains) -> bool:
    """host 是否等于或在某个可信域的子域下。"""
    if not host:
        return False
    h = host.lower().rstrip(".")
    return any(h == d or h.endswith("." + d) for d in domains)


def registrable(host: str) -> str:
    """近似 eTLD+1（不引第三方库）：取最后两级；中国双后缀(.com.cn 等)取三级。

    m.mcloud.139.com → 139.com；go.abchina.com → abchina.com；
    wx.abchina.com.cn → abchina.com.cn（双后缀按三级取）。
    """
    h = (host or "").lower().rstrip(".")
    parts = h.split(".")
    if len(parts) <= 2:
        return h
    cn_multi = ("com.cn", "net.cn", "org.cn", "gov.cn", "edu.cn", "ac.cn", "mil.cn")
    if h.endswith(cn_multi) and len(parts) >= 3:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def check_scheme(ctx, findings, score):
    """1. 非 HTTPS"""
    if ctx["scheme"] != "https":
        score += 10
        findings.append(("warn", "http", f"非 HTTPS（{ctx['scheme']}://）——明文传输，可被中间人篡改"))
    return findings, score


def check_at_sign(ctx, findings, score):
    """2. @ 伪装（http://真实域@恶意域）——只检测 host 部分的 @，路径里的 @ 是正常路由"""
    host_part = ctx["url"].split("://", 1)[-1].split("/", 1)[0]
    if "@" in host_part:
        score += 30
        findings.append(("high", "at-sign", "URL 含 @ 伪装——前面是诱饵域名，实际访问 @ 后面的域名"))
    return findings, score


def check_ip_direct(ctx, findings, score):
    """3. IP 直连"""
    if ctx["is_ip"]:
        score += 30
        findings.append(("high", "ip-direct", f"域名是裸 IP（{ctx['host']}）——正规服务不会这么干，钓鱼/恶意站高发"))
    return findings, score


def check_port(ctx, findings, score):
    """4. 端口异常"""
    if ctx["port"] and ctx["port"] not in (80, 443):
        score += 10
        findings.append(("warn", "port", f"非常用端口（:{ctx['port']}）——可疑"))
    return findings, score


def check_punycode(ctx, findings, score):
    """5. punycode"""
    if "xn--" in ctx["host"].lower():
        score += 30
        findings.append(("high", "punycode", "punycode 编码域名——视觉上可伪装成其他域名（如中文钓鱼），需解码确认真实域名"))
    return findings, score


def check_tld(ctx, findings, score):
    """6. TLD 风险"""
    if ctx["tld"] in HIGH_RISK_TLDS:
        score += 25
        findings.append(("high", "tld", f"高危 TLD（.{ctx['tld']}）——免费/滥用高发后缀，需额外警惕"))
    return findings, score


def check_brand(ctx, findings, score):
    """7. 品牌仿冒。返回 ctx 增补：is_official_brand / is_trusted_shortener"""
    host = ctx["host"]
    host_lower = ctx["host_lower"]
    brand = ctx["brand"]
    is_official_brand = False
    is_trusted_shortener = host_lower in TRUSTED_SHORTENER_MAP
    if brand:
        bname, method, is_white = brand
        if not is_white and not is_trusted_shortener:
            score += 30
            how = "域名包含品牌词" if method == "contains" else "域名高度相似"
            findings.append(("high", "brand-impersonation",
                             f"域名疑似仿冒品牌「{bname}」（{how}，非官方域名 {host}）"))
        elif is_trusted_shortener:
            findings.append(("info", "brand", f"已验明官方短链域名（{host}，跳转需落在官方主域）"))
        else:
            is_official_brand = True
            findings.append(("info", "brand", f"官方品牌域名（{bname}）"))
    ctx["is_official_brand"] = is_official_brand
    ctx["is_trusted_shortener"] = is_trusted_shortener
    return findings, score


def check_keywords(ctx, findings, score):
    """8. 危险关键词（官方品牌域名豁免 host 关键词——"paypal" 里的 pay 是品牌名不是钓鱼词）"""
    if ctx.get("is_official_brand"):
        return findings, score
    host_hits = [w for w in RISKY_HOST_KEYWORDS if w in ctx["host"].lower()]
    path_hits = [w for w in RISKY_PATH_KEYWORDS if w in ctx["path"].lower()]
    if host_hits:
        score += 15
        findings.append(("warn", "host-keyword", f"域名含危险关键词: {host_hits}——登录/验证/支付类钓鱼套路"))
    if path_hits:
        score += 10
        findings.append(("warn", "path-keyword", f"路径含敏感词: {path_hits}——login/verify/payment 等"))
    return findings, score


def check_shortener(ctx, findings, score):
    """9. 短链识别。返回 ctx 增补：is_shortener"""
    host_lower = ctx["host_lower"]
    is_shortener = host_lower in SHORTENER_DOMAINS or any(
        host_lower.endswith("." + d) for d in SHORTENER_DOMAINS)
    if is_shortener:
        score += 5
        findings.append(("warn", "shortener", f"短链/跳转服务（{ctx['host']}）——必须展开看真实目标，不可直接信任"))
    ctx["is_shortener"] = is_shortener
    return findings, score


def check_redirect(ctx, findings, score, follow: bool):
    """10. 跳转展开。返回 ctx 增补：redirect_ok / final_host"""
    redirect_ok = False
    if not follow:
        ctx["redirect_ok"] = redirect_ok
        return findings, score

    from link_check import follow_redirects  # 延迟 import（link_check 已 import 本模块，运行时无环）
    chain = follow_redirects(ctx["url"])
    if len(chain) > 1:
        redirect_ok = True
        final = chain[-1]
        final_host = urlparse(final).hostname or ""
        final_host_lower = (final_host or "").lower()
        trusted = host_in(final_host, TRUSTED_REDIRECT_HOSTS)
        # 可信短链：host 命中映射表 → 检查落点是否在官方主域内
        trusted_shortener = False
        for short_domain, official_hosts in TRUSTED_SHORTENER_MAP.items():
            if ctx["host_lower"] == short_domain:
                if host_in(final_host, official_hosts):
                    trusted_shortener = True
                    trusted = True
                break
        if final_host and registrable(final_host_lower) != registrable(ctx["host"]) and not trusted:
            score += 40  # 跳转偏离到非可信域 = 钓鱼强信号，单条即红
            tag = "redirect" if not trusted_shortener else "redirect-mismatch"
            note = "" if not trusted_shortener else "（官方短链跳到了非官方域，可疑！）"
            findings.append(("high", tag,
                             f"跳转偏离原域: {ctx['host']} → {final_host}{note}（真实目标: {final[:80]}）"))
        elif final_host and final_host_lower != ctx["host"].lower():
            label = "官方短链" if trusted_shortener else "可信官方生态域名"
            if trusted or trusted_shortener:
                findings.append(("info", "redirect-trusted",
                                 f"跳转到{label}: {final_host}（{final[:60]}）"))
            else:
                findings.append(("info", "redirect-same-domain",
                                 f"跳转同注册域({registrable(final_host_lower)}): {final_host}（{final[:60]}）"))
        else:
            findings.append(("info", "redirect", f"跳转链 {len(chain)} 跳，最终回到原域: {final[:60]}"))
    elif len(chain) == 1 and chain[0]:
        findings.append(("info", "no-redirect", "无跳转，直连"))

    # 短链但展开失败/无结果 → 不可确认真实目标，至少提为中风险
    if ctx.get("is_shortener") and not redirect_ok:
        score = max(score, SCORE_MED)
        findings = [f for f in findings if f[1] != "no-redirect"]
        findings.append(("warn", "shortener-unresolved", "短链未能成功展开（可能失效/被拦），真实目标不可确认——建议手动核实来源"))

    ctx["redirect_ok"] = redirect_ok
    return findings, score


def check_random_domain(ctx, findings, score):
    """10b. 可疑短域名启发式：非官方随机短域名 + 直连落地（不跳转）= 高级诈骗手法
    用注册域主体判断（倒数第二级），不取第一个标签——避免 a.baox46.cn 被剥成空
    判定：短（≤6字符）且**含数字**——1rk/xsx700/k7z/baox46 全是数字+字母混合；
    纯字母短域名（github/csdn/mgtv/ppsspp）是合法品牌名，不误伤（2026-08-02 批量扫描教训）"""
    if ctx.get("is_trusted_shortener") or ctx.get("is_official_brand") or ctx.get("redirect_ok"):
        return findings, score
    host = ctx["host"]
    labels = host.split(".")
    reg_label = (labels[-2] if len(labels) >= 2 else labels[0]).lower()
    looks_random = (
        len(reg_label) <= 6
        and reg_label not in BRANDS
        and any(ch.isdigit() for ch in reg_label)  # 必须含数字——随机诈骗域特征
    )
    if looks_random:
        score = max(score, 25)
        findings.append(("warn", "suspicious-random-domain",
                         f"随机短域名（{host}）直连落地——非官方品牌域，营销/诈骗类短信高发，需人工核实"))
    return findings, score


def check_threatbook_domain(ctx, findings, score):
    """11. 微步域名威胁情报核验（可选增强：有 key 才查，无 key 静默跳过）"""
    tb_key = threatbook.get_key()
    ctx["tb_key"] = tb_key
    if not (tb_key and ctx["host"]):
        return findings, score
    drep = threatbook.domain_report(ctx["host"], tb_key)
    if not drep:
        return findings, score
    if drep["malicious"]:
        score += 40
        findings.append(("high", "threatbook",
                         f"威胁情报判定为恶意（置信度 {drep['confidence'] or '?'}）——类型: {drep['threat_types'] or drep['judgments'] or '未知'}"))
    elif drep["threat_types"] or drep["judgments"]:
        score += 20
        findings.append(("warn", "threatbook",
                         f"威胁情报有风险标签: {drep['threat_types'] or drep['judgments'][:3]}（置信度 {drep['confidence'] or '?'}）"))
    else:
        findings.append(("info", "threatbook",
                         f"威胁情报未发现恶意标记（分类: {drep['categories'] or '未知'}）"))
    return findings, score


def check_threatbook_url(ctx, findings, score, follow: bool):
    """12. 微步 URL 信誉（有 key 且 follow 才查）"""
    tb_key = ctx.get("tb_key", "")
    if not (tb_key and follow):
        return findings, score
    urep = threatbook.url_report(ctx["url"], tb_key)
    if not (urep and urep["detection"]):
        return findings, score
    hit = urep.get("engines_hit", 0)
    total = urep.get("engines_total", 0)
    if urep["detection"] not in ("clean", ""):
        score += 35
        findings.append(("high", "threatbook-url",
                         f"URL 扫描引擎检出风险（{hit}/{total} 引擎）——类型: {urep['threat_type'] or '未知'}"))
    else:
        findings.append(("info", "threatbook-url",
                         f"URL 扫描引擎判定 clean（{total} 引擎）"))
    return findings, score
