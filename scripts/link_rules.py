#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""link_rules.py — 链接风险判定规则库（纯数据，无逻辑）

被 link_check.py import。维护规则只改这里，不碰判定逻辑。

更新记录：
  2026-08-02 短信实战 40 条 + 收藏夹 578 域名校准
"""

# ───────────────── 域名风险 ─────────────────

# 免费/滥用高发 TLD（无需备案、廉价注册，钓鱼/恶意站点占比高）
HIGH_RISK_TLDS = {
    "tk", "ml", "ga", "cf", "gq", "top", "xyz", "icu", "click", "link",
    "buzz", "work", "loan", "date", "win", "men", "mom", "site", "online",
    "rest", "country", "stream", "download", "racing", "accountant", "party",
    "review", "faith", "science", "live",
}

# ───────────────── 品牌仿冒 ─────────────────

# 常见仿冒目标品牌（域名模糊匹配用）
BRANDS = [
    "taobao", "tmall", "aliyun", "alibaba", "1688",
    "paypal", "pay", "alipay",
    "amazon", "apple", "microsoft", "google", "facebook", "netflix",
    "qq", "wechat", "weixin", "tencent", "jd", "jingdong", "pinduoduo",
    "bank", "icbc", "ccb", "abc", "abchina", "boc", "cmb", "citic", "cib", "psbc",
    "steam", "bilibili", "bili", "douyin", "tiktok", "zhihu", "weibo", "139", "mcloud",
    # 生态主域（子域会被识别为官方品牌，避免 snsyun.baidu.com 误判随机域）
    "baidu", "modian", "mihoyo", "miyoushe", "pizzahut", "didi",
    "kuaishou", "taobao", "pinduoduo",
]

# 高价值品牌域名白名单（同品牌词出现但不在白名单 → 仿冒嫌疑）
BRAND_DOMAINS = {
    "taobao": "taobao.com", "tmall": "tmall.com", "aliyun": "aliyun.com",
    "alibaba": "alibaba.com", "alipay": "alipay.com",
    "paypal": "paypal.com", "amazon": "amazon.com", "apple": "apple.com",
    "microsoft": "microsoft.com", "google": "google.com", "netflix": "netflix.com",
    "qq": "qq.com", "wechat": "weixin.qq.com", "weixin": "weixin.qq.com",
    "tencent": "tencent.com", "jd": "jd.com", "jingdong": "jd.com",
    "steam": "steampowered.com", "bilibili": "bilibili.com", "bili": "bilibili.com",
    "douyin": "douyin.com", "tiktok": "tiktok.com", "zhihu": "zhihu.com",
    "weibo": "weibo.com", "bank": "", "pay": "", "live": "",
 "abc": "abchina.com", "abchina": "abchina.com",   # 农行：go.abchina.com 官方短链域（2026-09-08 校准）
 "139": "139.com", "mcloud": "mcloud.139.com",     # 移动云盘生态（c.139.com / m.mcloud.139.com）
 "baidu": "baidu.com", "modian": "modian.com", "mihoyo": "mihoyo.com",
    "miyoushe": "miyoushe.com", "pizzahut": "pizzahut.com.cn", "didi": "didi.cn",
    "kuaishou": "kuaishou.com", "pinduoduo": "pinduoduo.com",
}

# 生态域名豁免（品牌词出现在这些后缀里不算仿冒——steamdb/steampp/steamcommunity/biligame 是正当生态站）
BRAND_SUFFIX_WHITELIST = [
    "steamcommunity.com", "steamdb.info", "steampp.net", "steamzg.com",
    "augmentedsteam.com", "steamreview.org", "steamcardexchange.net",
    "steamgifts.com", "steamcharts.com", "steamunlocked.net",
    "biligame.com", "biligames.com", "biligame.net",
]

# ───────────────── 短链与跳转 ─────────────────

# 短链/跳转服务（命中必须展开）
SHORTENER_DOMAINS = {
    "t.cn", "dwz.cn", "url.cn", "bit.ly", "goo.gl", "tinyurl.com", "is.gd",
    "u.nu", "k.cn", "s.weibo.com", "v.douyin.com", "v.kuaishou.com", "u.jd.com",
    "tb.cn", "m.tb.cn", "c.tb.cn", "ktt.mgtv.com", "weixin.qq.com",
}

# 可信短链映射（已逐一验证过：短链域名 → 官方主域）
# 判定规则：host 命中此表，且跳转最终落在对应主域 → 🟢官方短链；跳偏 → 照报红
# 验证记录 2026-08-02：
#   cmbt.cn → cmbchina.com（招行，知乎多方确认+官方通告）
#   b23.tv → bilibili.com（B站，分享链接标准格式）
#   dx.10086.cn → 10086.cn（中国移动主域子域）
#   s.mi.cn → mi.cn（小米主域子域）
#   3.cn → jd.com（京东官方短链，实测跳 www.jd.com）
#   t.hk.uy → asus.com.cn（华硕官方短链，.uy 后缀，实测跳 wap.asus.com.cn）
#   u.jd.com → jd.com（京东官方短链，搜索确认京东生态）
#   y.m.cn → pizzahut.com.cn（必胜客官方短链，location 头实测）
#   c.didi.cn → didi.cn（滴滴官方短链，主域子域）
#   c.tb.cn → taobao.com（淘宝/菜鸟官方短链，tb.cn 系官方）
TRUSTED_SHORTENER_MAP = {
    "cmbt.cn": ["cmbchina.com"],
    "b23.tv": ["bilibili.com"],
    "dx.10086.cn": ["10086.cn"],
    "s.mi.cn": ["mi.cn"],
    "3.cn": ["jd.com"],
    "t.hk.uy": ["asus.com.cn"],
    "u.jd.com": ["jd.com"],
    "y.m.cn": ["pizzahut.com.cn"],
    "c.didi.cn": ["didi.cn"],
    "c.tb.cn": ["taobao.com"],
}

# 可信跳转目标（短链跳转到这些官方生态域名不算风险）
TRUSTED_REDIRECT_HOSTS = {
    "iesdouyin.com", "www.iesdouyin.com", "douyin.com", "www.douyin.com",
    "kuaishou.com", "www.kuaishou.com",
    "weixin.qq.com", "mp.weixin.qq.com",
    "tb.cn", "item.taobao.com", "detail.tmall.com", "m.tb.cn",
    "jd.com", "item.jd.com", "u.jd.com",
    "weibo.com", "m.weibo.cn",
    "pan.baidu.com", "baidu.com", "www.baidu.com", "snsyun.baidu.com",
    "modian.com", "m.modian.com",
    "mhyurl.cn", "miyoushe.com", "bbs.mihoyo.com", "mihoyo.com",
    "pizzahut.com.cn", "mkt.pizzahut.com.cn",
    "139.com", "mcloud.139.com", "m.mcloud.139.com",   # 中国移动云盘（c.139.com 官方短链入口，2026-09-08）
    "abchina.com", "go.abchina.com", "wx.abchina.com", # 农行官方（go. 短链 → wx. 掌银H5）
}

# ───────────────── 危险关键词 ─────────────────

# 危险关键词（陌生域名 + 这些词 = 钓鱼典型套路）
RISKY_HOST_KEYWORDS = ["login", "signin", "verify", "secure", "account",
                       "update", "confirm", "auth", "password", "bank",
                       "wallet", "payment", "pay", "gift", "lottery", "bonus"]
RISKY_PATH_KEYWORDS = ["login", "signin", "verify", "secure", "account",
                       "update", "confirm", "password", "bank", "wallet",
                       "payment", "transfer", "gift", "lottery", "reward",
                       "红", "包", "中奖", "转账", "实名", "认证", "安全中心"]

# ───────────────── 评分阈值 ─────────────────

SCORE_HIGH = 40   # ≥40 高风险
SCORE_MED = 15    # ≥15 中风险
