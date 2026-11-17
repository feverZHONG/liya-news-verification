---
name: news-verification
tier: T2  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
description: 验证伞——轻量核查（图/链接真的吗）＋交付前多源验证＋链接危险识别。触发：验证新闻、核对数字。
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
| 个人自称「花了 N 亿 token／N 个月做成了 X」 | **多源核查·技术宣称三层**（成果／数字换算／归属） |
| 官宣/宣传片/「正在开发中」类消息 → 是真是假/是不是画饼 | **厂商官宣核实**（厂商自家 PR 页 + 画饼三问） |
| 收到/要访问陌生链接（钓鱼/仿冒/恶意跳转） | **链接安全检查**（linkcheck） |
| 收到「官方通知」邮件（安全/2FA/账号变更/赔付）要判真伪 | **邮件原件验真**（要 .eml，四道关；截图只能给「文案像」） |
| 想要「一段带引用的答案」（一个问题／一个链接，不想自己翻页） | `bin/ds-ask "问题" --search` 或 `--url <链接>`（服务端搜索/抓取，附 `url_citation` 来源；搜索/抓取各 5 元/千次） |

---

## 模块 A · 轻量快速核查（速记 · 全文见 `references/模块A-轻量快速核查.md`）

- **能自己并行搜完的绝不派小队**；缩写多义先穷举候选，隐喻提问先换视角。
- **图里的标识符放大逐字符读**：域名／路径／版本号裁块再读，并拿外部证据交叉。
- **「官方公告」截图先验身份三件**：主语、落款、官方渠道有没有同名贴。
- **名单类转发先判性质**（鸣谢≠股东名册），名字在名单里≠有股权。
- **多事件并置先拆后串**：「A 暴跌＋B 挤兑＋C 全面晚点」逐条定性、再问共同原因——多数只是同一周；单位口径（点数/百分比/市值）先换算再引用 → `references/multi-event-conflation.md`
- **流传数字回一手实测**；AI 声称是最高危的单一来源。
- **“技术大神”类账号看投稿史变向**：同一作者早期投稿给开源仓库（README/项目链接），后来只给打码的企鹅号／群号——这是从分享转向引流的硬信号，比粉丝数、标题吹多大都可罪；配“根域加载中→随机路径 `go-数字/?id=`”类跳转池域名＝防封常规操作。定性分三层写：事真（开源项目/技术路线存在）／人蹭（改的是别人开的源）／钱当心（加群后卖整合包/收徒）。

## 模块 D · 结论自查（速记 · 全文见 `references/模块D-结论自查.md`）

- **下否定结论前先换最硬的标识符再搜一次**（全名／编号／原文串）。
- **两次空才定案**；一次空只能写「本轮未找到」，不写「不存在」。
- 空结果要先怀疑检索手段（索引、语言、站点、登录墙），不是先怀疑事实。

## 模块 B · 交付前多源核查（速记 · 全文见 `references/模块B-交付前多源核查.md`）

**何时必查**：体育比分／统计数字／序列号／事件日期时效／改编消息／巨额头条／模型基准表。

- **比分与数字**：2–3 个独立来源一致才出手；官方口径对齐，百分比×绝对数验算，巨额金额 2 源+出处。
- **独立来源看措辞不看域名**：整段雷同＝同一次转抄，只算 1 源。
- **热度 ≠ 能力证据**：star／播放量只证声量；「N 家媒体一致」先查是不是一源 N 转。
- **技术宣称拆三层**：成果（能不能跑）／数字（自述先换算）／归属（自研 vs 拿来）。
- **时效核查先取当前时间**；相对时间（「2~3 周后」）标推算并定到期点，跳票后改活口、不再续日期。
- **「关停了」分层验**：端口行为（握手／RST／超时）＋同机前后对照，别拿一个端口下结论。
- 详细判例（厂商宣传图、驱动口径、服务故障补偿、主体归属、速通记录）全在 references。

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

**现场型官宣（演唱会/发布会）官方 SNS 先于官网 News**：官网 News 栏的最后更新日期若早于事件日，它就是滞后源——**「官网查无」不能判「未证实」**；**官方 SNS 直接抓不到时，用第三方年表／条目站的引注坐实**——同人年表 wiki 会把官方 X 的帖号连链接抄进年表正文，条目站（Bangumi 一类）的条目**建/改时间戳**＋多站同日夜间同步＝同一波官宣的硬证据（判「坐实」看多站同源时间戳，不看单站措辞）；帖文里的告知清单要逐条连名目抄，特设站路径全 404 只写「未开站」；**同一波公告的多个日期先认名目再引用**（活动日 ≠ 本体发售窗口），编号/脚注引用先回落到它标注的那一行 → `references/vendor-announcement-check.md` §7

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

**邮件类「官方通知」验真（铁律）：截图能看文案，看不了身份。** 判真伪必须拿 `.eml` 原件走 `bin/eml --raw-headers`，四道关缺一条就只说「存疑」：① `From:` 的 `@` 后域（显示名不算证据）② `Authentication-Results` 的 SPF／DKIM／DMARC 全 pass 且 DKIM `d=` 与 From 域对齐 ③ 发信 IP 落在服务商公布的官方网段（GitHub＝`api.github.com/meta`；SPF pass 只是第一层，网段是第二层）④ **全文件**所有 URL 的域名（从 raw MIME 抽，不能只看渲染正文的锚文本）。内容层加一道：通知里的期限算得出来才算真模板（如截止＝起算日 +45 天整）；**判真之后照样不从邮件里跳，手打官方入口**——防的是下次一模一样的假货。流程与抽链接片段→ `references/email-authenticity-eml.md`

**群里转的「立冬礼物／神秘礼物」类 H5：按三层扒，别一棍子打成木马**（2026-11-09 实测）

- **① 门帘**：短域名 + 路径页常常只有几十字节，内容就一句 `<meta http-equiv="refresh" content="0;url=http://…">`——跳转还从 https 降级到 http。别在门帘上停，记下目标路径继续走。
- **② 钩子**：目标页多是纯前端整活（「收下」→ 弹「恭喜获得 XX」→ 放一段抖音神曲并允许把倍速翻到 8x），挂第三方统计（`v1.cnzz.com/z.js?id=`）和 `weixin://dl/business/?appid=` 小程序跳转。**页面无表单、不收集输入**是分水岭：钩子层定性「诱饵」，不是木马。
- **③ 落地**：再往上一级（根域常是「加载中」→ `iid.<另一域>/go-<随机数>/?id=NN` 的跳转池，标准防封做法）才是生意页——卖整蛊 APK／代做表白页，条款写「虚拟商品概不退款」，免责声明全甩给用户；**多个域名解析到同一批 IP ＝ 同一运营方**。
- **结论写法**：分「诱饵页（无害）／落地页（卖货）／交付物（来源不明的 APK）」三层，只拦最后一项，出口一句「看可以，别买别装」。把整条链一律写成木马会误伤无害整活页；反过来，钩子无害也不等于替落地页背书——转发的人以为在发整蛊，实际在替它发传单。

短信诈骗模板 → `references/sms-fraud-patterns.md`；可信短链白名单 → `references/verified-shorteners.md`；威胁情报源调研 → `references/threat-intel-sources.md`；收藏夹精选属私档，不在本仓

---

## 模块 C+ · 链接考古探测（速记 · 全文见 `references/模块C+-链接考古.md`）

- **问「还活着吗／当年内容去哪了」走 `linkprobe`**：`linkprobe <url>` 出状态码／跳转终点／标题／判定。
- `--both` 双协议、`--wayback` 查存档、`--domains d1,d2` 换域名找搬家内容、`--json` 机器读。
- 裸死域名、空壳 BBS、停放页、换域名——先判形态再下结论。

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
| 邮件原件验真（.eml 四道关 / 官方通知类，附 GitHub 强制 2FA 处置口径） | `references/email-authenticity-eml.md` |
| 速通类主张（作弊封号／世界纪录被下架）的一手核法 | `references/speedrun-record-claims.md` |
| 老交互页/H5 真跑一遍（媒体是否起播、资源是否 404） | `scripts/h5_functional_probe.py` |
| linkcheck 工具族 | `scripts/`（link_check/link_checks/link_rules/batch_check/threatbook/parse_bookmarks） |

---

## 拆分记录

- **2026-11-10 模块 B 拆薄**：整节 5,266 字符逐字搬进 `references/模块B-交付前多源核查.md`；本文 16,603 → 11,786 字符，守恒 0 缺失。
- **2026-10-01 拆薄**：232 行 / 15.5K 字符 → **166 行 / 7.4K 字符（-53%）**；搬出 71 条 / 21.5KB，新增 5 档（`references/conclusion-self-check.md` / `references/measured-numbers.md` / `references/ai-claims.md` / `references/contested-event-reading.md` / `references/image-url-liveness.md`），4 档并入既有档（`references/verification-details.md` / `references/vendor-announcement-check.md` / `references/media-framing-deconstruction.md` / `references/ui-feature-effectiveness.md`）；逐条守恒校验 0 丢失 / 0 残留（整篇复核见同日提交说明）。同日**新增「模块 D · 结论自查」**（由模块 A 的 2026-10-01 沉淀升格为独立模块，判据留正文、判例进 references）。

- **2026-11-10 二轮压到 8K 下**：模块 A／D／C+ 整节逐字搬 `references/模块A-轻量快速核查.md`、`模块D-结论自查.md`、`模块C+-链接考古.md`；本文 11,886 → 7,505 字符，守恒 0 缺失。
