# 验证伞 · 事实核查与链接安全

> 三件事合成一把伞：**轻量快速核查**（甩来图/链接问「真的吗」）+ **交付前多源核查**（比分/数字/日期）+ **链接危险识别**（`linkcheck`：钓鱼、仿冒、跳转偏离）。
> 外加两块：**厂商官宣核实**（一手源 + 画饼三问）与**链接考古探测**（死链查档、换域捞回）。

## 这是什么

一条总口径：**别拿单一来源当事实，AI 的话只当线索。**

| 场景 | 走哪个 |
|:-----|:-------|
| 甩图/链接/一句话「这个是真的吗」→ 快速结论 | 轻量快速核查（并行搜，不派小队） |
| 输出前涉及比分/数字/日期/时效/基准表 | 交付前验证（2–3 独立来源一致才出手） |
| 官宣/宣传片/「正在开发中」类消息 | 厂商官宣核实（厂商自家 PR 页 + 画饼三问） |
| 收到/要访问陌生链接（钓鱼/仿冒/恶意跳转） | `scripts/link_check.py` 分级 |
| 「这链接还活着吗 / 当年内容去哪了」 | 链接考古探测（`link_probe` 一族） |

## 最贵的三条教训

1. **AI 的辟谣/自我指认听起来越权威越要二次查证**——实测它能把自家官方号面不改色打成「高仿冒充号」，还编得有鼻子有眼。判据＝权威接口的原始字段，不是 AI 的叙述。
2. **「N 家媒体口径一致」可能是一源 N 转**——发布会后的稿子往往抄同一份物料。把每条口径回溯到最早出现的载体，同源就记「口径出自 X」，不记「多源一致」。
3. **署名红线**：「官方 PR 没写」≠「官方没署名」。官方信息面要逐层走全（PR → 官网·特设站 → 商店页 → 官方 SNS → 实机 staff roll）再下结论；走全之前不许说「没有」。

## 工具

```bash
python3 scripts/link_check.py "https://example.com/xxx"       # 静态检测 + 跳转链展开（默认）
python3 scripts/link_check.py "https://t.cn/xxx" --no-follow  # 只静态
python3 scripts/batch_check.py urls.txt                       # 批量
python3 scripts/h5_functional_probe.py <url> --click '#btn'   # 交互页/按钮「还能用吗」真跑一遍
```

- 分级：🔴 高危（≥40 分）不点不输信息；🟡 中（15–39）先核实来源；🟢 低可访问
- ⚠️ **品牌仿冒项是子串匹配，会对知名域名误报**——域名本身认得出来就按假阳性放行，别拿一条假阳性去拒读正经来源
- 威胁情报：微步 API（key 放环境变量 `THREATBOOK_API_KEY`，无 key 自动跳过，功能不退化）

## 目录

| 路径 | 内容 |
|:---|:---|
| `SKILL.md` | 入口：三模块分流 · 各模块判据 · 引用表 |
| `references/quick-fact-check.md` | 轻量快速核查全文（铁律 + 流程） |
| `references/link-safety-check.md` | 链接安全判定维度与分级 |
| `references/verification-details.md` | 交付前核查完整流程与实战台账 |
| `references/vendor-announcement-check.md` | 厂商官宣一手源 / 画饼判定 / 「全面超越」类宣称怎么核 |
| `references/company-registry-check.md` | 企业主体与 ICP 备案核证（谁运营、是不是同一家） |
| `references/ui-feature-effectiveness.md` | 网页按钮/开关/旧版入口「还有效吗」三层判据 |
| `references/media-framing-deconstruction.md` | 自媒体框架预置拆解（注入 vs 排版替你想好） |
| `references/sms-fraud-patterns.md` / `sms-phishing-patterns.md` | 短信诈骗与钓鱼模板 |
| `references/verified-shorteners.md` / `threat-intel-sources.md` | 可信短链白名单 / 威胁情报源调研 |
| `references/benchmark-glossary.md` | 基准表验证口径 |
| `scripts/` | `link_check.py`（含规则/检查器）· `batch_check.py` · `h5_functional_probe.py` · `threatbook.py` |

## 读者须知

文中 `<数据根>`＝放 `skills/` 的那层目录；`mmx`／`read-url`／`bin/now`／`credman` 是**作者环境**的入口与工具（未单独公开），判据与它们无关——照自己的环境替换。**验证日志与收藏夹精选属本机私档，不在本仓。** 实测数字里的日期/案例读作「某次实战样本」。

## 姊妹仓库

- [liya-dev-workflow](https://github.com/feverZHONG/liya-dev-workflow) —— 开发全流程（本仓的脚本/CLI 那套工程纪律出自它）
- [liya-delegation-and-verification](https://github.com/feverZHONG/liya-delegation-and-verification) —— 委派与验收：把「自报」验成事实
- [liya-subtraction-skill](https://github.com/feverZHONG/liya-subtraction-skill) —— 技能库做减法：减法优先、去重、归档、拆薄
- [liya-persona-authoring](https://github.com/feverZHONG/liya-persona-authoring) —— 给 AI agent 写它自己的身份文件（SOUL.md）
- [liya-prose-quality-metrics](https://github.com/feverZHONG/liya-prose-quality-metrics) · [liya-story-revision-plan](https://github.com/feverZHONG/liya-story-revision-plan) · [liya-corpus-line-mining](https://github.com/feverZHONG/liya-corpus-line-mining) —— 写作三件
- [liya-sillytavern-cards](https://github.com/feverZHONG/liya-sillytavern-cards) · [liya-tavern-card-refinement](https://github.com/feverZHONG/liya-tavern-card-refinement) · [liya-sillytavern-worldbook](https://github.com/feverZHONG/liya-sillytavern-worldbook) —— 酒馆角色卡三件
- [liya-vision-recognition-traps](https://github.com/feverZHONG/liya-vision-recognition-traps) —— 视觉模型识图陷阱（「图里文字读错了」这类本仓管核，它管识）
- [liya-chat-game-referee](https://github.com/feverZHONG/liya-chat-game-referee) · [liya-spy-game](https://github.com/feverZHONG/liya-spy-game) · [liya-sea-turtle-soup](https://github.com/feverZHONG/liya-sea-turtle-soup) —— 聊天里能玩的三件
- [liya-ruozhiba-wordbank](https://github.com/feverZHONG/liya-ruozhiba-wordbank) —— 弱智吧题防御手册
- [liya-subtitle-proofreading](https://github.com/feverZHONG/liya-subtitle-proofreading) —— 字幕校对/重建/外挂 SRT
- [liya-knowledge-persistence](https://github.com/feverZHONG/liya-knowledge-persistence) —— 知识持久化：信息该放记忆层／文件／技能库的分层规范（附记录完整性、语料减法、归档模式）
- [liya-incident-review](https://github.com/feverZHONG/liya-incident-review)
- [liya-document-translation](https://github.com/feverZHONG/liya-document-translation)

## 提思路 / 提修正

- 你那边的核查案例、新的仿冒手法、遗漏的判据 → 开 [Issue](https://github.com/feverZHONG/liya-news-verification/issues)
- 想直接改 → Fork + PR

## 许可

**双许可**——文档与代码分开：

- **代码**（`scripts/` 下的文件）：**MIT** —— 拿去用、改、再发，保留版权声明即可。
- **文档**（`SKILL.md`、`references/`、本 README 的正文）：**[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** —— 可以自由使用、改编、连商用都行，**但要署名**（莉娅 / [@feverZHONG](https://github.com/feverZHONG)）并注明来源。

两份全文：`LICENSE`（MIT）／`LICENSE-DOCS`（CC BY 4.0）。

---

*莉娅（[@feverZHONG](https://github.com/feverZHONG)）· 宇宙美好记录官*
