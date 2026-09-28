# DeepSeek 官方一手信息渠道速查

> 验证 DeepSeek 发布/价格/版本信息时用。2026-08-13 V4-Pro-0813 发布验证实战沉淀（官方 news 页 + 定价页 + IT之家三源实锤）。
> 归属说明：本想进另一个记录类 skill（未单独公开，手动创建禁改），放这里做「验证 DeepSeek 消息」的快速核查参考。

## 渠道（按可靠度）

1. **官方 API 文档 news 页** — `https://api-docs.deepseek.com/zh-cn/news/newsYYMMDD`（**两位年份 + 月日**，如 news260813 = 2026-08-13、news260910 = 2026-09-10）。⚠️ 2026-09-10 实测：省略年份的 `news0813` 是**无效页**（回落到「Your First API Call」导航），必须带年份。Docusaurus 站点，curl 直接可抓。想看某天发布→按此格式拼 URL
2. **官方定价页** — `https://api-docs.deepseek.com/zh-cn/quick_start/pricing`。含「模型版本」字段（如 `DeepSeek-V4-Pro-0813`）+ 价格表 + 上下文/输出长度 + 并发限制 + 公告（如「计划近期整体上调 API 定价」）。⚠️ 必须 `curl -sL` + `User-Agent: Mozilla/5.0`，纯 grep 抓价格页会空手而归（标签/脚本干扰）
3. **/models 实测** — 有 API key 时 `GET /models` 看实际模型 ID（0731 实战用过）
4. **第三方报道交叉** — IT之家（首页标题可 grep 出文章链接，`<a href="...">标题</a>` 正则），腾讯新闻 new.qq.com/rain/a/...

## 解析配方（Docusaurus HTML）

```bash
curl -sL "https://api-docs.deepseek.com/zh-cn/quick_start/pricing" -m 20 \
  -H "User-Agent: Mozilla/5.0" -o <临时目录>/ds.html
# 然后 python: 去 <script>/<style> → 去标签 → html.unescape → 压缩空白
# → find 关键词（deepseek-flash / 模型版本 / 百万tokens）截上下文
```

整页落盘再清洗，别直接管道 grep。

## 版本号判定

- **模型 ID 不变、后训练更新**是 DeepSeek 惯例：`deepseek-v4-pro` 保持原 ID 指向新版，用户无需改调用
- news 页 + 定价页「模型版本」字段为第一手（Flash-0731 / Pro-0813 就是这里读出来的）
- 官方说的「正式版 / Preview」以 news 页为准，别信二手截图版本号

## 调价公告直接读定价页（2026-08-13 实战）

- 涨价/调价公告**就写在定价页正文**——「我们将对 DeepSeek API 价格进行更新调整……新价格将于北京时间 X 月 X 日 00:00 开始生效，具体如下：」+ 新旧价格表。curl 定价页 + python 清洗（去 script/style/标签 → html.unescape → 压缩空白）后 `find('价格进行更新调整')` 截上下文即可拿到完整方案，不用等媒体
- news 页（newsMMDD）**不会**放调价公告——08-13 抓 news0810~0813 都是「Your First API Call」教程导航，纯定价页
- 峰谷定价关键词：`高峰时段` / `空闲时段` / `缓存命中` / `百万tokens输出`。价格表按「模型 × 项目 × 时段」三层，清洗后是平铺文本，抓 `deepseek-flash` 起始的连续段（2026-09-10 模型名换代；旧名 `deepseek-v4-flash` 段落在新版页面已消失）

## 第三方交叉渠道实测（2026-08-13）

- ✅ **IT之家首页标题 grep 有效** — `curl https://www.ithome.com/` 后正则 `<a[^>]+href="(https://www\.ithome\.com/0/\d+/\d+\.htm)"[^>]*>([^<]+)</a>` 扫标题，关键词（DeepSeek/涨价/调价）过滤即可命中相关文章（如「DeepSeek API 峰谷定价方案公布，8 月 17 日生效」）。文章正文抓 `线索投递` 后面的段落即可，Docusaurus 式清洗后 `find('线索投递')` 截上下文
- ❌ **IT之家搜索接口死** — `so.ithome.com/api/search` / `www.ithome.com/search` 都返回 ~50 字节空壳，别走搜索，直接抓首页
- ❌ **Bing 中文科技新闻无效** — `bing.com/search?q=DeepSeek+涨价` 返回的全是官网/仿冒站广告块，`li.b_algo` 无新闻；腾讯新闻 search API 也返回 56 字节空壳。中文科技圈新闻交叉验证 = IT之家首页 grep 最快

## 迭代期公告核对（2026-09-10 V4 Pro 下线实战）

同一事件常连出多版公告，**改口才是信号**：9/9 版「V4.1 Flash 上线之后、**V4.1 Pro 上线之前**把 V4 Pro 请求路由到 V4.1 Flash」（留口子）；9/10 版「**2026-09-14 12:00 下线 V4 Pro 服务**」（定死期）。同句「经内部、外部多方测试……性能/费用/速度/总用时全面超越」为模板复用，不能用来判「是不是同一份」。

- **开放平台通知先于媒体**：9/9 版公告当天 15:24 起被 IT之家/财联社/每经/腾讯转走；9/10 版的「9月14日」截止 9/10 上午全网（mmx/B站/知乎/IT之家首页/微信 AI 早报）零覆盖。→ 核对时若「方向多源印证、具体时间点无公开源」，判**官方一手待确认**：不当假消息，也不当已证实。
- **定价页更新滞后于公告，但会在当日追上**：9/10 上午抓定价页仍列 `deepseek-v4-pro` / `DeepSeek-V4-Pro-0813`；**同日 17:4x 复核已全面更新**——模型名 `deepseek-flash`（版本 `DeepSeek-V4.1-Flash`）、新价格表、脚注(2) 明写「9 月 14 日 12:00 之后访问 deepseek-v4-pro 的请求将全部路由到 V4.1 Flash 并按 Flash 价格计费」。→ 观察窗口按「公告当日」计，别用过期的「定价页未变」下结论。
- **news 页：格式对了就有内容**。当日上午 news260910 页仍是导航（因为正式发布未落地）；**当日下午该页已有完整发布文**（标题「DeepSeek V4.1 Flash：更强、更快、更普惠」，含改名、定价、Pro 下线三件事）。→ 别把「news 页是导航」当成「news 页不放公告」的证据，先确认 URL 带年份、再确认是否已过发布时间点。

## 收图读表注意（2026-08-13 V4-Pro 基准图实战）

- 基准对比表 vision 一次读会**漏格**（NL2Repo/DeepSWE/ALE 等列空着，但关键数字 Terminal Bench 87.9 / CyberGym 83.3 拿到了）——**空值标 `—` 绝不脑补填数**
- 与文字报道交叉：IT之家「多项测试接近 Fable 5」与读出的数字吻合 → 结论可信
- 归档注明「vision 有漏值，完整表以官方大图为准」
- 完整视觉陷阱拆解见 vision-recognition-traps「通用对策 4」
