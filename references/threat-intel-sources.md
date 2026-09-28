# 威胁情报源调研（2026-08-02）

> 链接危险识别的外部情报源调研结论。`link_check.py` 已接入微步在线（可选增强，无 key 自动降级）。

## 接入：微步在线云 API（ThreatBook）

**为什么选它**：国内可达、免费试用、域名+URL 双接口、响应为结构化中文威胁情报。

### 端点（实测有效）

| 用途 | 端点 | 参数 |
|:-----|:-----|:-----|
| 域名分析 | `https://api.threatbook.cn/v3/domain/query` | `apikey`, `resource=<域名>`, `lang=zh`, 可选 `exclude` |
| URL 信誉 | `https://api.threatbook.cn/v3/url/report` | `apikey`, `url=<完整URL>` |

**参数坑**：
- `domain/query` 用 `resource` 参数；`url/report` 用 `url` 参数（不是 `resource`——传错报 `Required:url.`）
- 域名分析响应在 `data` 对象：`is_malicious`, `confidence_level`, `judgments`, `threat_types`, `tags`, `categories`, `cur_whois.registrar`
- URL 信誉响应在 `data` 对象：`detection`, `total_engines`, `detected_engines`, `threat_type`, `categories`
- 错误码：无效 key → `response_code:-1 Invalid API Key`；方法/参数错 → `-2 Invalid Api method` / `-3 Required:xxx`

### 免费额度与 key

- x.threatbook.com 注册 → 申请试用 → API Key（新用户有免费额度；免费版有 QPS/日配额限制）
- key 优先读环境变量 `THREATBOOK_API_KEY`（作者环境另用凭据工具 `credman` 存取），无 key 静默跳过

## 调研淘汰项（实测）

| 源 | 实测 | 淘汰原因 |
|:---|:-----|:---------|
| urlscan.io | 搜索 API 可直连 HTTP 200 | 需 key；偏历史扫描，对未收录新域名意义小 |
| Google Safe Browsing | 需 key | 无 Google 账号/国内访问受限 |
| PhishTank checkurl | HTTP 403 | 被拦 |
| VirusTotal | 国内访问不稳 | 需 key + 网络不稳 |

## 踩坑：官方文档是 SPA，端点格式怎么找

微步 x.threatbook.com/v5/apiDocs 是 SPA（内容在 JS 里，curl 拿不到正文）。
解法：搜 GitHub 上现成的 API 封装 → 直接读源码里的端点和参数。
本例：NAXG/ThreatMCP → `threatbook_mcp/server.py` 里 `THREATBOOK_API_BASE = "https://api.threatbook.cn/v3"`，
`get_domain_analysis` / `get_url_report` 给出完整参数格式。比猜接口快得多。
