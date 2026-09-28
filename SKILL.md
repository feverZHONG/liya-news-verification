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

## 三模块分流

| 场景 | 走哪个 |
|:-----|:-------|
| 用户甩图/链接/一句话「这个是真的吗」→ 快速结论 | **轻量快速核查**（并行搜，不派小队） |
| 输出前涉及比分/数字/日期/时效/基准表 → 交付前验证 | **多源核查**（2-3 独立来源一致才出手） |
| 官宣/宣传片/「正在开发中」类消息 → 是真是假/是不是画饼 | **厂商官宣核实**（厂商自家 PR 页 + 画饼三问） |
| 收到/要访问陌生链接（钓鱼/仿冒/恶意跳转） | **链接安全检查**（linkcheck） |

---

## 模块 A · 轻量快速核查（原 quick-fact-check）

**铁律：** 能自己并行搜完的绝不派小队；缩写多义先穷举候选再下判断（SD=Stable Diffusion 还是 Seedance）；隐喻式提问先换视角（「坑位」可能是营销入口）；截图溯源先抠作者名再匹配；古语先查成语本形。

**AI 声称是最高危的「单一来源」（2026-09-05 糖豆人案例）** — 甩 B站「豆包」官方号视频链接问豆包「这是不是你」，豆包答「不是正版官方号，是高仿冒充号」，编出假证据（「闪电标不是机构蓝V是个人互关徽章」+ 引用 3 关键词 15 来源）；实际该号 card API 返回 `Official role=3 title=「豆包App官方账号」`，是官方认证号。教训：**AI 的辟谣/自我指认/查证结论听起来越权威越要二次查证**——它连自己的官方号都能面不改色打成高仿。判据=权威接口原始字段（平台账号认证类判断用官方 API：B站 card API 的 Official.role/title，title 优先于 desc），AI 的话只当线索。平台结构化数据查询先查对应平台 ops skill 的定版脚本（B站→bilibili-api-ops：bili_up_auth.py 链接→UP认证一条龙），别手搓接口。

**AI 投毒残留识别（2026-09-09 Apollo-9 演习）** — 用户问「虚构产品哪里能买」=可能是投毒陷阱演习/真实受害场景。识破要点：① 内容农场软文识别特征——单账号批量、同构标题（「XX哪家强」「选XX制造商看这里」「XX品牌众多哪个可靠」）、0 赞、万金油话术（PPG传感器/50+运动模式/环保亲肤）；② 消毒分层——主流入口（百度百科第一句定性、新闻源前排）通常已清干净，残留毒在长尾平台（知乎专栏等）挂半年没人管；③ AI 分享页回答是「表现样本」不是事实（每页带「内容由AI生成，请仔细甄别」），对比各家 AI 回答走 `bin/ai-share`；④ 权威定性 ≥2 独立源一致判假（百科+315 新闻），软文残留反而是反向识别特征。

```text
接收 → 图片=视觉入口（作者环境是 `mmx vision describe`） / 链接=提取标题摘要 / 文字=提取事实点
     → 并行 搜索入口（作者环境是 `mmx search`） ×2~3 不同角度
     → 比对（date 一致 / ≥2 独立来源吻合 / 图片文字以搜索交叉校验）
     → ✅ 确认（日期/当事人/出处）或 ❌ 存疑（只找到这些，等用户确认）
```

细节/踩坑/短信钓鱼/VTuber 速查 → `references/quick-fact-check.md` + `references/pitfalls-and-special.md` + `references/sms-phishing-patterns.md` + `references/vtuber-neuro-sama.md` + `references/deepseek-official-sources.md`

**媒体贴文「框架预置」拆解（2026-09-12）** —— 甩来一条自媒体/AI 缝合稿问「这有什么会干扰你判断」时，先分清两种东西：**注入攻击**（文本里有指令让 AI 做事）vs **框架预置**（没指令，只是替你把结论排好队）。后者四件套＝① 伪装成元信息的括号注（「（AI注：…）」承载全文最关键的那次动机定性）② 预设立场菜单（一段事实配 N 份不同立场的「AI评论」，不逼你信哪条，让你从现成结论里挑一份）③ 议题替换（命题从「X 该不该担心」滑到「说这话的人图什么」）④ 流量反推动机（浏览高→必有推手）。判据与回话纪律（不跟着站队、给「要验什么」）→ `references/media-framing-deconstruction.md`

**网页交互入口「还能用吗」核查（实测沉淀）** —— 有人问「X 页面那个 Y 按钮/开关起作用吗」时，**按钮还在 ≠ 按钮有效**：入口留着多半是前端没删干净，服务端早不认了。三层判据缺一不可：① 点击有没有副作用（cookie/localStorage/请求）；② **reload 后页面有没有真的切过去**（这层才是成败）；③ 切换类开关成功时会出现回程按钮（「回到新版」之类）。只答①＝把「举手」当成「开门」。配方、dump 清单与 `t.bilibili.com` 回旧版实测 → `references/ui-feature-effectiveness.md`

---

## 模块 B · 交付前多源核查（原 news-verification）

**何时必查：** 体育比分（最高风险，2 独立来源）/ 统计数据 / 序列号 / 事件日期时效 / 动漫游戏改编 / 巨额头条 / 模型基准表。

- 比分：搜索词写 `球队A vs 球队B 比分`，snippet 无明确比分不编造；罕见高比分 3 源确认
- 数字：官方公告对齐；百分比×绝对数验算；口径一致（乘用车 vs 汽车）；巨额金额 2 源+出处
- 时效：date 字段比对；B站吃瓜看 pubdate 不看标题播放量；多 docid 取最早=首发；GitHub/官网看 pushed_at/meta description
- 红线：类别时效（新闻今日~昨日 / 科技 2 天内 / 报告 1 周内标日期）
- **时效核查前先取当前时间**：判断「这日期是不是未来／是不是假消息」之前先跑 宿主的时间命令（作者环境是 `bin/now`）。长会话跨天时**早先读到的时间锚点全部作废**——拿前一天的「今天」去判，会把今晨的报道当成不可能存在的未来新闻，白绕一圈；日期不确定就用工具读，别用推理填时间空缺
- **讣闻/生死类核查链**（名人「去世」是谣言高发区，单来源一律不算）：① 一手＝**官方讣告**（当事人单位/家属发布）② 央媒跟进＝新华社、央视新闻（独立采写而非转载）③ 百科生卒（`1933年9月16日—2026年9月24日` 这种写法可当交叉验证）④ 回答口径：**不用娱乐化语气**，给生卒＋身份定语＋代表作＋信源链；讣告里没写的后事安排不推断、不编 ⑤ **长年被周期性造谣的当事人（生前本人/经纪人都辟过谣）尤其只认讣告**——这类名字的搜索前排会混进旧谣言与自媒体「晚景凄凉」稿，一律不作数；反过来，**拿到一手讣告（单位＋关联基金/机构两份更好）就不必再疑**，直接定案。用户常在热搜之前先问一句「某某还健在？」，核完答上，条目留「后续」等热搜到场补记即可
- 多源冲突取共识主流值+约数，精确差异进待验证区
- **版本号 ↔ 年份是最容易错的一类对应关系，必须现查官方日期**：游戏/软件/硬件的大版本序列跨度可达一年以上（同一序列里 3.0 与 3.6 可能隔近一年），凭记忆或凭当事人口述写「X 版本＝X 年」必错。取法＝**官方发版/更新公告页**（游戏：BWIKI 各版本「更新专题」页 grep「停服更新补偿：YYYY/MM/DD」；软件：release notes / changelog）；落档时**版本号与上线日期成对写**，只写版本号的引用等于没核。己方推断与对方口述都只当线索，核完再落档——报底时一并给来源，别顺着原来的说法写下去

**「N 家媒体口径一致」可能是一源 N 转，不是多源印证** —— 发布会后的媒体稿、通稿转载、预热物料的二次报道，**往往抄的是同一份物料**：四家媒体数字完全一致，只能证明那份物料存在过。判据：把每条口径回溯到**最早出现的那个载体**（官方公众号／预热视频／PR 页／商店页），同源就记「口径出自 X」，**不记「多源一致」**。同理，**物料发布时间 ≠ 事件发生时间**（预热片可提前数天发布，会后稿件只是复读）；引用时把「哪天发布的物料」和「哪天的稿子引了它」分开写。

**事件有「现场」而手上只有二手转述时，开口要一手观察，别用推演填空** —— 发布会／直播／线下这类事件，媒体稿和官方口径提供的只有「对外说了什么」，「现场到底什么样」只有一手观察者能给。**禁止用听起来顺的结构性解释把空白填圆**：解释越圆，越容易把「核的是预热视频」写成「发布会核实」。收尾自查一句——有没有该问而没问的问题。

完整核查流程/搜索封锁对策/陷阱/基准口径 → `references/verification-details.md` + `references/benchmark-glossary.md`（验证日志属本机运行记录，不入本仓）

**「这产品归谁运营 / A 和 B 是不是同一家」类主体主张** → 官网页脚 ICP（一手）→ 隐私政策原文（「由 XX 运营」= 运营方实锤）→ 第三方备案查询补主体名与审核日 → 工商关联；争论当事人说辞只当线索。命令与坑（JS 渲染站点怎么绕、频控、法人≠运营方）见 `references/company-registry-check.md`（2026-09-12 沉淀，尘白×剑侠4 实例）。

---

## 模块 B+ · 厂商官宣核实（一手源 + 画饼判定）

> 沉淀自 2026-09-10 合金弹头 30 周年（用户怀疑宣传片结尾那句英文「还在画大饼」）。

**一手源铁律：官宣类消息先找厂商自家 press release 索引页，别停在新闻聚合站。**

```bash
curl -s <厂商站>/press/ -H "User-Agent: Mozilla/5.0" | grep -oE 'href="[^"]*press/<年>[^"]*"'
# 拿当期 PR URL → `read-url`（作者环境的正文提取命令） 读全文
```

- 实测对比（SNK）：厂商 PR 页 curl 直取可用，一次给全硬字段（收录清单逐作+原平台、功能、价格「未定」、平台、愿望单、周边企划期限）；同日 gematsu / 知乎专栏 / insider-gaming **全部 403，只有二手转述**
- 聚合站给的是「谁的解读」，PR 给的是「官方口径」——口径差异（官方叫「传说中的试玩版」vs 商店文案「Location Test 版」）只有 PR 能定
- ⚠️ **各语种官方渠道不同步**：别因为某个官方号没有就当没官宣过（SNK 中国 B站号本轮只有 4/19、9/9 两条，6 月「双新作」是从日文/英文渠道发的）

**画饼判定三问（预告卡 / 「正在开发中」类官宣）：**

| # | 问什么 | 判据 |
|:--|:-------|:-----|
| 1 | 这是第几张卡？ | 拉时间线——同一件事 5 个月发 3 张标语卡（MISSION REBOOT → 双新作 → A NEW METAL SLUG…），零新增信息 = 这张卡是空的 |
| 2 | 有没有具名的人/组织在推？ | 采访人证（品牌经理、项目监督、跨部门例会）> 只有标语；有资源投入 = 项目本身是真的 |
| 3 | 同期有没有能交付的实物？ | 有实物（合集 2027）≠ 承诺都兑现；实物还是别人代做的话更要分开记 |

**结论写法：** 分开下判——「项目是真的」与「这张卡是空的」可以同时成立，别揉成一句「是/不是画饼」。

**动机/意图类结论：时间线吻合只算线索，不坐实（2026-09-10 合金弹头清场线实例）。** 可查事件（SNK 自家从 Google Play 撤架 + 游聚被版权清场，2025.12~2026.03）与后续官宣（合集 2026.09）排在一起「太整齐了」——但「清场是为了把玩家赶进合集」仍是**推断**：官方对外口径始终是维权/版权，**没人认这个动机**。写法：事实层列事件，推断层标【推断】并写明验证点（例：合集发售后旧作会不会重新上架、还有没有别家跟进下架），别把「恶心到了」写成为「已证实」。同理，找不到独立源的细节（某平台是否同步下架）标待核，只有标题点名的视频**不算坐实**。

**署名红线（2026-09-10 当日二改，本条自身就是案例）：** 「官方 PR 没写」**≠**「官方没署名」——**官方信息面要逐层走全再下结论**：PR/新闻稿 → **产品官网·特设站** → 商店页（appdetails 的 developers/publishers） → 官方 SNS（各语种） → 实机 staff roll。合金弹头合集自己曾**只翻中文 PR** 就判「SNK×M2 查无出处」并撤回，事后官方特设站 Feature 02 白纸黑字「**エムツーが移植開発を担当**」——**误撤，当日二改**。走全仍无 → 才标「待核」；走全之前**不许**下「没有」的结论，也仍**不许**凭「名声对得上」补工作室名；具名人物要连**人+职+来源+年月**一起记。

**特设站是 SPA、`read-url` 只出首屏片段时**（本轮 Feature 01 有、02/03 缺）：`curl -s -L <url> -H "User-Agent: Mozilla/5.0"` 存原 HTML → Python 正则剥 `<script>/<style>` 与标签 + `html.unescape` 逐行去重输出——实测一次拿回全部 Feature 段（含署名那条）与规格字段。快照成 `scripts/fetch-spa-page.py` 亦可（详见 references/vendor-announcement-check.md §2.5）。

**游戏新作「商店信息」核实（一款游戏刚官宣商店页时必走）**

预告一出，「上哪几台／多少钱／什么时候」到处是二手转述——能当一手源的只有**商店页字段**和**官方公告**两处：

1. **先拉商店页的完整 appdetails JSON，别只摘速查输出**（免 key）。速查输出是人工挑的字段，**`pc_requirements`（系统需求）就被整块漏过**。名字→appid：`curl -s --max-time 20 "https://store.steampowered.com/api/storesearch/?term=<名字>&l=schinese&cc=cn"`；全字段：`curl -s --max-time 25 "https://store.steampowered.com/api/appdetails?appids=<id>&l=schinese&cc=cn"`。要核的：`release_date` / `price_overview` / `platforms`（看清 mac·linux 有无）/ `supported_languages`（分清「界面+字幕」还是含完整音频）/ **`pc_requirements`（最低+推荐）** / `ratings` / `content_descriptors` / `categories` / `dlc` / `package_groups`。**「即将推出」+ 无价格 + `package_groups` 空 = 连本体都还没开卖**，别把一堆标签当成已发售信息。两个坑：① store 域请求**一律带 `--max-time`**（偶发挂到外层超时，白等一轮）；② 手搓取 appdetails 时**人工挑字段必漏**——要么用现成 CLI（`steam store <appid>`，注意它的输出不含系统需求），要么先把字段表列全再摘。
2. **官方公告优先于商店页**：`curl -s --max-time 20 "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=<id>&count=10&maxlength=8000"` 拿官方公告全文（`steam news <appid>` 只列标题+链接，要看正文得取 `contents` 字段）。公告常带商店页没有的硬信息——**发售窗口收窄到半年内、平台间发售时间差、原型渊源、下一篇放料时间**。公告是主源，商店页是登记表；两者冲突时以时间在后的官方公告为准。
3. **⚠️ 预告海报上的平台 logo 只是「目标声明」，不是「已上架」**：要断言「上了哪几台」必须去各平台商店各自搜一次（PS Store / Microsoft Store / Nintendo eShop 都有查询入口）。**检索不到就写「仅有目标声明，商店页未开」**——海报列 4 个平台标、其中 3 家商店查无此作，是新作官宣期的常态。把海报标成「全平台」是最容易让用户误判的写法。
4. **⚠️ 商店分类标签不是官方对商业模式的宣布**：读者（和模型）会把「应用内购买」这类标签直接读成「官方要卖内购」。**「标签属实」≠「形态已知」**——标签只是商店后台的登记项，在售项为空时更谈不上形态。报出去前做三源复核：① appdetails 换 2~3 个语言/区（中/日/韩）看该 category id 是否稳定出现（排除语言包错译）；② 商店页 HTML 里该 chip 的链接是否指向 `search/?category2=<id>`；③ 用 `search/?term=<名>&category2=<id>` 搜一次，**命中才说明平台侧真这么归类**。落档时把「标签属实」与「形态已知」分两行写，别合成一句「有内购」。

5. **⚠️ 未发售游戏的字段常是占位符，「未定」不等于「填错了」**：系统需求（`pc_requirements` 的内存/存储）、价格这类未公布字段，商店后台必填就随手填（实测有把内存填 `8MB`、存储填 `16MB` 的）。**不当真实配置转述，也别当商店页出错来调侃**——转述时标「未定/占位」；判读商业模式靠正文（版本如何划分售卖、有没有内购/DLC 公告、卡牌等资源靠什么获取），未定字段零信息量。

细节/URL 模式/复用清单 → `references/vendor-announcement-check.md`

**「全面超越」类宣称（性能/基准，2026-09-10 V4 Pro 下线沉淀）** —— 官宣的「超越」是话术不是结论，去**换把尺子**：① 自家 harness vs 中立 harness（CoderSera / Artificial Analysis / 社区横评）——**分差 30+ 或排名翻转 = 尺子被适配过**；② 改动量对得上跑分涨幅吗（只改 serving 效率却单项 +50 分 = 红旗）；③ 时间线闭合（上线当晚就撤回 + 长期零解释 + 「被新款全面超越」收场 = 止损叙事）。判读：**「全面超越」的信息量取决于被超越方**；程度保留（泛化失败 ≠ 全线归零）；厂商/第三方/用户判断**三层分源**别混。配方 → `references/vendor-announcement-check.md §6`

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

**图片直链存活校验（2026-09-11 微博图床实测）** — 甩来的图 URL 打不开时，**中转/镜像站的 403 不等于图没了**，要拿**原始图床直链**验：

```bash
# 镜像 youzirou.org/cdn/weibo/large/<id>.jpg  →  换成官方图床直连
curl -sIL --max-time 15 -H "Referer: https://weibo.com/" -H "User-Agent: Mozilla/5.0" \
  "https://ww1.sinaimg.cn/large/<图id>.jpg" | grep -Ei "^(HTTP|content-type|content-length|location)"
```

- 真图：`200 image/jpeg` + 正常 content-length（实测 204907）
- **死图：`302 → //ww1.sinaimg.cn/images/default_h_large.gif`**（8.8KB 占位 gif）= 微博「图片不存在」（已删/被夹/链接是拼的）
- 交叉验证：域名 `ww1/wx1/ww4.sinaimg.cn` + 尺寸前缀 `large/bmiddle/mw2000/orj1080/thumb300/small`——全尺寸都占位才下「不存在」的结论
- 判读纪律：① 镜像站整站 403（连另一张能读的图一起拒）= 站级风控，与单张图死活无关；② 同一博主前缀、时间码相邻的两张，前一张 200、后一张占位 → 后一张确已不在源站；③ `vision_analyze` 遇到这种 URL 会跟随 302 到占位 gif 后报 403——**报错里那个 `default_h_large.gif` 就是「图不存在」的铁证**，先校验再对图下结论
- 微博侧细节（图 id 前缀/评论接口）→ 一个姊妹 skill（未单独公开）的微博文档 §六

**交互 H5／老活动页「还能不能用」的功能实测（2026-09-24 央视「习近平邀请你视频通话」H5）** — 有人转来一条老互动页（「这链接是真的吗／点开是什么」）时，**`linkcheck` 只判危险不判死活**，还要再跑一层真浏览器：

```bash
linkcheck <url>                                             # 第一层：域名/跳转/威胁情报分级
python3 skills/news-verification/scripts/h5_functional_probe.py <url> --click '#btn'   # 第二层：无头浏览器真跑
```

判读：**media 请求出现 + `paused=false`、`readyState>=3` = 真能用**；只有 HTML/CSS 200、媒体请求永不出现 = 空壳或接口已废（「按钮还在 ≠ 按钮有效」的同一判据）。**单个 js 404（如 `share.js`）不等于整页坏**——curl 的 404 在浏览器里可能拿到 200（CDN 变体），以浏览器实测为准。

- ⚠️ **本机 playwright 坑：包与已装浏览器版本号常对不上**（包要找 `chromium_headless_shell-1228`，实际只装了 `-1243`）→ `launch` 直接报 `Executable doesn't exist`。**别去下浏览器**，列出 `/opt/hermes/.playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell` 用真实路径传 `executable_path`（脚本已自动探测）。
- 报「是什么」时要落到**一手出处**：H5 页面本身不给上下文，去搜同名官方稿（例：`news.cctv.com 2023-01-18《习近平邀请你视频通话》`，署名「监制丨策划丨编导丨交互」齐全）才算定案；页面上的 `last-modified` 只是上传时间，不是事件时间。
- **判「是不是真的」看域名 + 一手官方稿，不看内容离谱不离谱**：越看越怪的页面（模拟来电、写着「请关闭手机静音」这种）反而更可能是官方的创意互动——别被「这也能发？」的直觉带着走，那是转发者的情绪，不是风险证据。

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
| 老交互页/H5 真跑一遍（媒体是否起播、资源是否 404） | `scripts/h5_functional_probe.py` |
| linkcheck 工具族 | `scripts/`（link_check/link_checks/link_rules/batch_check/threatbook/parse_bookmarks） |
