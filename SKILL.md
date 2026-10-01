---
name: news-verification
tier: T2  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
description: 验证伞——轻量快速核查（图/链接「真的吗」）+ 交付前多源验证（比分/数字/日期）+ 链接危险识别（linkcheck）。触发：验证新闻、核对数字、确认日期比分、这图真的吗、链接安全、钓鱼、短信诈骗。
---

# Verification · 事实核查与链接安全

> 2026-09-04 三件合一：news-verification（交付前核查）+ quick-fact-check（轻量快速核查）+ link-safety-check（链接危险识别）→ 本伞。
>
> **读者须知（工具与环境）**：文中 `<数据根>`＝放 `skills/` 的那层目录，`scripts/` 指本仓自带脚本
> （`link_check.py` 一族就是 `linkcheck` 命令的实现，直接 `python3 scripts/link_check.py <url>` 即可）；
> `mmx`／`read-url`／`bin/now`／`credman` 是**作者环境**的入口与工具（未单独公开），判据与它们无关。
> 实测数字里的日期与案例读作「某次实战样本」。
> 被合并技能原 SKILL.md 降级为 `references/quick-fact-check.md` + `references/link-safety-check.md`（原样保留），细节查原文件。

## 模块分流

| 场景 | 走哪个 |
|:-----|:-------|
| 下「没有／未入／不在／没找到」这类**否定结论**之前 | **结论自查**（换最硬的标识符，两次空才定案） |
| 用户甩图/链接/一句话「这个是真的吗」→ 快速结论 | **轻量快速核查**（并行搜，不派小队） |
| 输出前涉及比分/数字/日期/时效/基准表 → 交付前验证 | **多源核查**（2-3 独立来源一致才出手） |
| 官宣/宣传片/「正在开发中」类消息 → 是真是假/是不是画饼 | **厂商官宣核实**（厂商自家 PR 页 + 画饼三问） |
| 收到/要访问陌生链接（钓鱼/仿冒/恶意跳转） | **链接安全检查**（linkcheck） |

---

## 模块 A · 轻量快速核查（原 quick-fact-check）

**铁律：** 能自己并行搜完的绝不派小队；缩写多义先穷举候选再下判断（SD=Stable Diffusion 还是 Seedance）；隐喻式提问先换视角（「坑位」可能是营销入口）；截图溯源先抠作者名再匹配；古语先查成语本形。

**「有／没有」类结论 → 见下方「模块 D · 结论自查」**（空结果≠不存在；完整判例与工具改造见 `references/conclusion-self-check.md`）

**流传数字要用一手可得数据实测**（录屏抽帧 → 逐格读 → 时间序列；选片与读法）→ `references/measured-numbers.md`

**AI 声称是最高危的「单一来源」**（连自己的官方号都能打成高仿）→ `references/ai-claims.md` §1

**AI 投毒残留识别**（内容农场软文特征、消毒分层、软文残留反是反向特征）→ `references/ai-claims.md` §2

```text
接收 → 图片=视觉入口（作者环境是 `mmx vision describe`） / 链接=提取标题摘要 / 文字=提取事实点
     → 并行 搜索入口（作者环境是 `mmx search`） ×2~3 不同角度
     → 比对（date 一致 / ≥2 独立来源吻合 / 图片文字以搜索交叉校验）
     → ✅ 确认（日期/当事人/出处）或 ❌ 存疑（只找到这些，等用户确认）
```

细节/踩坑/短信钓鱼/VTuber 速查 → `references/quick-fact-check.md` + `references/pitfalls-and-special.md` + `references/sms-phishing-patterns.md` + `references/vtuber-neuro-sama.md` + `references/deepseek-official-sources.md`

**争议事件「双方材料」的读法**（事实／叙事／机制三层读、先认门牌、物料识别、许可那层）→ `references/contested-event-reading.md`

**媒体贴文「框架预置」拆解**（注入攻击 vs 框架预置；预设立场菜单、议题替换）→ `references/media-framing-deconstruction.md`

**网页交互入口「还能用吗」**：按钮还在 ≠ 有效（点击副作用 → **reload 后有没有真切过去** → 有无回程按钮）→ `references/ui-feature-effectiveness.md`

---

## 模块 D · 结论自查（否定性结论先验检索手段）

> 2026-10-01 立。铁律一句：**「没有／未入／不在／没找到」是对检索手段的断言，不是对世界的断言**——下笔前先验手段本身。

- **回表用最硬的标识符**（appid／登记号／ID／一手页面原文），名称只当辅助线索；名称匹配不到时**先换标识符**，别换措辞再试。
- **两次空才敢说「没有」**：一个标识符查空 → 换另一个再查一次。只查一次就写「未入／不存在」，是把工具的**空结果**当成了事实。
- **落档时结论带标识符**（「已入，appid X，时长 Y」），别只写中文名——否则下次同一坑原样重踩，看档案的人也无法复核。
- **同一毛病的家族＝用副本核对原件**：译名、别名、缩写、单位（小时读成分钟）、二手转述都属这一类。凡用「更间接的表示」核对事实，先问一句：这个表示与事实一一对应吗？
- **检索工具自己也要改**：查空静默返回「没有」，人就会把空结果当结论——给工具加告警与相似候选（判例见下），比在文档里写一句「别这么查」管用。
- **同族红线**：官方信息面逐层走完之前，不下「没有」的结论（见「模块 B+」署名红线）。

判例、事故经过与工具改造（译名查空 → 误写「未入」→ 全库同类扫描）→ `references/conclusion-self-check.md`

---

## 模块 B · 交付前多源核查（原 news-verification）

**何时必查：** 体育比分（最高风险，2 独立来源）/ 统计数据 / 序列号 / 事件日期时效 / 动漫游戏改编 / 巨额头条 / 模型基准表。

- 比分：搜索词写 `球队A vs 球队B 比分`，snippet 无明确比分不编造；罕见高比分 3 源确认
- 数字：官方公告对齐；百分比×绝对数验算；口径一致（乘用车 vs 汽车）；巨额金额 2 源+出处
- 时效：date 字段比对；B站吃瓜看 pubdate 不看标题播放量；多 docid 取最早=首发；GitHub/官网看 pushed_at/meta description
- 红线：类别时效（新闻今日~昨日 / 科技 2 天内 / 报告 1 周内标日期）
- **时效核查前先取当前时间**：判断「这日期是不是未来／是不是假消息」之前先跑 宿主的时间命令（作者环境是 `bin/now`）。长会话跨天时**早先读到的时间锚点全部作废**——拿前一天的「今天」去判，会把今晨的报道当成不可能存在的未来新闻，白绕一圈；日期不确定就用工具读，别用推理填时间空缺
- **讣闻/生死类核查链**：一手＝官方讣告 → 央媒独立采写 → 百科生卒；单来源不算，口径不用娱乐化语气 → `references/verification-details.md`
- 多源冲突取共识主流值+约数，精确差异进待验证区
- **版本号 ↔ 年份：必须现查官方发版公告，版本号与日期成对写**（凭记忆或口述必错）→ `references/verification-details.md`

**「N 家媒体口径一致」可能是一源 N 转**（回溯到最早载体；物料发布时间 ≠ 事件时间）→ `references/verification-details.md`

**事件有「现场」而手上只有二手转述时**：开口要一手观察，别用推演填空（解释越圆越可疑）→ `references/verification-details.md`

完整核查流程/搜索封锁对策/陷阱/基准口径 → `references/verification-details.md` + `references/benchmark-glossary.md`（验证日志属本机运行记录，不入本仓）

**「这产品归谁运营 / A 和 B 是不是同一家」类主体主张** → 官网页脚 ICP（一手）→ 隐私政策原文（「由 XX 运营」= 运营方实锤）→ 第三方备案查询补主体名与审核日 → 工商关联；争论当事人说辞只当线索。命令与坑（JS 渲染站点怎么绕、频控、法人≠运营方）见 `references/company-registry-check.md`（2026-09-12 沉淀，尘白×剑侠4 实例）。

---

## 模块 B+ · 厂商官宣核实（一手源 + 画饼判定）

> 沉淀自 2026-09-10 合金弹头 30 周年（用户怀疑宣传片结尾那句英文「还在画大饼」）。

**一手源铁律：官宣类消息先找厂商自家 press release 索引页**，别停在新闻聚合站（PR 给官方口径、聚合站给解读；各语种官方渠道不同步）→ `references/vendor-announcement-check.md` §1

**画饼判定三问（预告卡 / 「正在开发中」类官宣）：**

| # | 问什么 | 判据 |
|:--|:-------|:-----|
| 1 | 这是第几张卡？ | 拉时间线——同一件事 5 个月发 3 张标语卡（MISSION REBOOT → 双新作 → A NEW METAL SLUG…），零新增信息 = 这张卡是空的 |
| 2 | 有没有具名的人/组织在推？ | 采访人证（品牌经理、项目监督、跨部门例会）> 只有标语；有资源投入 = 项目本身是真的 |
| 3 | 同期有没有能交付的实物？ | 有实物（合集 2027）≠ 承诺都兑现；实物还是别人代做的话更要分开记 |

**结论写法：** 分开下判——「项目是真的」与「这张卡是空的」可以同时成立，别揉成一句「是/不是画饼」。

**动机/意图类结论：时间线吻合只算线索，不坐实**（事实层列事件、推断层标【推断】＋验证点）→ `references/vendor-announcement-check.md` §3

**署名红线：「官方 PR 没写」≠「官方没署名」**——官方信息面（PR → 特设站 → 商店页 → 官方 SNS → staff roll）**走全之前不许下「没有」的结论**，也不许凭「名声对得上」补名字 → `references/vendor-announcement-check.md` §4

**特设站是 SPA、只出首屏片段时**（curl 存 HTML → 正则剥标签 → 逐行去重）→ `references/vendor-announcement-check.md` §2.5

**游戏新作「商店信息」核实**（一手源＝商店页字段 + 官方公告；海报 logo 只是目标声明；分类标签≠商业模式；未定字段常是占位符）→ `references/vendor-announcement-check.md` §5

细节/URL 模式/复用清单 → `references/vendor-announcement-check.md`

**「全面超越」类宣称**（自家 harness vs 中立 harness；分差 30+ 或排名翻转＝尺子被适配过）→ `references/vendor-announcement-check.md` §6

---

## 模块 C · 链接安全检查（原 link-safety-check）

```bash
linkcheck "https://example.com/xxx"       # 静态检测 + 跳转链展开（默认）
linkcheck "https://t.cn/xxx" --no-follow  # 只静态
python3 skills/news-verification/scripts/batch_check.py urls.txt   # 批量
```

包装器：`<数据根>/bin/linkcheck`（脚本在 `scripts/`）。

- 🔴 高（≥40 分）：不点/不输信息；@ 伪装、裸 IP、punycode、品牌仿冒、高危 TLD、跳转偏离（单条即红）
- ⚠️ **品牌仿冒项是子串匹配，会对知名域名误报**（2026-09-12 实测：`m.weibo.cn` 命中品牌词「boc」亮 🔴，实为微博官方域）。**域名本身认得出来 = 按假阳性放行**，照常看跳转链；别拿一条假阳性红项去拒读正经来源，也别因此不看分级
- 🟡 中（15~39）：先核实来源，短链看真实目标
- 🟢 低：可访问
- 流程：`linkcheck` 拿分级 → 🔴/🟡 结合上下文（来源/动机）→ 短链展开看真实目标 → 仿冒提示官方域名 → 短信先对模板表
- 威胁情报：微步 API（key 放环境变量 `THREATBOOK_API_KEY`，或由作者环境的凭据工具 `credman` 提供——**无 key 自动跳过**，功能不退化）

短信诈骗模板 → `references/sms-fraud-patterns.md`；可信短链白名单 → `references/verified-shorteners.md`；威胁情报源调研 → `references/threat-intel-sources.md`；收藏夹精选属私档，不在本仓

---

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

## 引用表

| 要查什么 | 打开 |
|:---------|:-----|
| 原 quick-fact-check 全文（铁律+流程） | `references/quick-fact-check.md` |
| 原 link-safety-check 全文（判定维度/分级） | `references/link-safety-check.md` |
| 轻量核查踩坑/特殊场景 | `references/pitfalls-and-special.md` |
| 交付前核查完整流程 | `references/verification-details.md` |
| 企业主体 / ICP 备案核证（谁运营、是不是同一家） | `references/company-registry-check.md` |
| 基准表验证口径 | `references/benchmark-glossary.md` |
| 厂商官宣一手源/画饼判定/「全面超越」宣称核对 | `references/vendor-announcement-check.md`（§6＝性能宣称：自家 vs 中立 harness） |
| 网页按钮/开关/旧版入口「还有效吗」 | `references/ui-feature-effectiveness.md` |
| **否定性结论的自查（没找到≠不存在）** | `references/conclusion-self-check.md` |
| 流传数字实测（录屏抽帧读时间序列） | `references/measured-numbers.md` |
| AI 声称 / AI 投毒残留 | `references/ai-claims.md` |
| 争议事件「双方材料」的读法（长图/大字报） | `references/contested-event-reading.md` |
| 图片直链存活校验（图床/镜像站） | `references/image-url-liveness.md` |
| 老交互页/H5 真跑一遍（媒体是否起播、资源是否 404） | `scripts/h5_functional_probe.py` |
| linkcheck 工具族 | `scripts/`（link_check/link_checks/link_rules/batch_check/threatbook/parse_bookmarks） |

---

## 拆分记录

- **2026-10-01 拆薄**：232 行 / 15.5K 字符 → **166 行 / 7.4K 字符（-53%）**；搬出 71 条 / 21.5KB，新增 5 档（`references/conclusion-self-check.md` / `references/measured-numbers.md` / `references/ai-claims.md` / `references/contested-event-reading.md` / `references/image-url-liveness.md`），4 档并入既有档（`references/verification-details.md` / `references/vendor-announcement-check.md` / `references/media-framing-deconstruction.md` / `references/ui-feature-effectiveness.md`）；逐条守恒校验 0 丢失 / 0 残留（整篇复核见同日提交说明）。同日**新增「模块 D · 结论自查」**（由模块 A 的 2026-10-01 沉淀升格为独立模块，判据留正文、判例进 references）。

