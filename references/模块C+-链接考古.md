---
title: 验证伞 · 模块 C+ 链接考古探测
tier: T2
---

> 本档是 SKILL.md「模块 C+」整节原文（2026-11-10 拆出，逐字未改）。

## 模块 C+ · 链接考古探测（linkprobe）

> 验证伞的另一面：不是「这链接危险吗」，是「这链接还活着吗/当年内容去哪了」。沉淀自 2026-09-08 悟饭合金弹头考古（papa91→5fun 域名线裸死、老BBS空壳、DNSPod接管页、换域名捞回2018投稿全文）。

```bash
linkprobe <url> ...                # 探测：状态码/跳转终点/页面标题/判定
linkprobe <url> --both             # http+https 都试（默认只按给定）
linkprobe <url> --wayback          # 非活链接查 web.archive.org 存档（查原始URL）
linkprobe <url> --domains d1,d2    # 非活链接换域名重试（同路径换 host，找搬家的内容）
linkprobe <url> --json             # JSON 输出
```

判定：🟢 活 / 🛡 域名接管（DNSPod/备案拦截特征，域名已死）/ 💀 404·不可达 / ⚠ 空壳疑（多 URL 同 title/同兜底页=内容已失但服务器还响应）。对 bilibili.com 自动带本机 cookie（/tmp/bili_cookies.txt）防 412。

典型考古链：`linkprobe 老链接 --both --wayback --domains 新域名` → 一条命令跑完「死→查档→换域捞回」。用途：老链接体检、历史遗留举证、md 断链深查（mdcheck 只报断，linkprobe 报死因）。

**图片直链存活校验**：镜像/中转站的 403 ≠ 图没了，要拿**原始图床直链**验（`302 → default_h_large.gif` ＝ 图不存在）→ `references/image-url-liveness.md`

**交互 H5／老活动页「还能不能用」**：`linkcheck` 判危险、`python3 skills/news-verification/scripts/h5_functional_probe.py <url> --click '#btn'` 判死活（media 起播＋`readyState>=3` 才算能用；单个 js 404 ≠ 整页坏）→ `references/ui-feature-effectiveness.md`

**执行铁律（2026-09-08 实战教训，被用户纠正）：** 访问任何外部链接（哪怕来源是可信转发）先 `linkcheck` 分级再动手抓取/解析——自己曾跳过 linkcheck 直接 curl 连管道解析，姿势不对，没出事不是理由。顺手发现 linkcheck wrapper 指向合并前旧 skill 路径（已修），验证链路平时就要保证是通的。
