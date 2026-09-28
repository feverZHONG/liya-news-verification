---
name: link-safety-check
tier: T2  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
description: 链接危险识别——收到/查阅链接时快速判断是否钓鱼、仿冒、恶意跳转。静态特征 + 跳转链展开。
---

# link-safety-check · 链接危险识别

> 用户给链接、或自己需要查阅链接时，先过一遍安全检查再点/再访问。

## 什么时候用

- 用户甩来一条链接问「这个能信吗 / 帮我看下」
- 自己要打开一个陌生链接（短链、未知域名、疑似钓鱼）
- 链接来自不可信来源（陌生人转发、广告、弹窗）

## 快速使用

```bash
linkcheck "https://example.com/xxx"       # 静态检测 + 跳转链展开（默认）
linkcheck "https://t.cn/xxx" --no-follow  # 只静态检测（不想碰目标站时）
linkcheck "https://x.com/" --json          # JSON 输出（程序化处理）

# 批量扫描（收藏夹/URL清单）
python3 skills/link-safety-check/scripts/batch_check.py urls.txt            # 文件
cat urls.txt | python3 skills/link-safety-check/scripts/batch_check.py -   # stdin
python3 skills/link-safety-check/scripts/batch_check.py urls.txt --no-follow  # 只静态
```

包装器：`<数据根>/bin/linkcheck`（脚本：`scripts/link_check.py` + `link_checks.py` 检查器 + `link_rules.py` 数据 + `threatbook.py` 情报）。

## 判定维度

| 维度 | 识别什么 | 风险 |
|:-----|:---------|:-----|
| @ 伪装 | `http://真域名@恶意域名`——实际访问 @ 后的 | 🔴 高 |
| 裸 IP 直连 | `http://192.168.x.x/`——正规服务不这么干 | 🔴 高 |
| punycode | `xn--` 开头——视觉伪装（中文钓鱼） | 🔴 高 |
| 品牌仿冒 | leetspeak 替换（ta0ba0→taobao）+ fuzzy 相似 | 🔴 高 |
| 高危 TLD | .tk/.xyz/.top/.icu 等免费滥用后缀 | 🔴 高 |
| 跳转偏离 | 短链展开后真实目标 ≠ 原域（且非可信）——**单条即红** | 🔴 高 |
| 非 HTTPS | http:// 明文传输 | 🟡 中 |
| 危险关键词 | login/verify/payment 等出现在陌生域名 | 🟡 中 |
| 短链未展开 | t.cn/dwz.cn/bit.ly 等，真实目标不可确认 | 🟡 中 |
| 随机短域名 | 注册域 ≤6 字符随机串（1rk/xsx700 类）直连落地 | 🟡 中 |
| 官方品牌+可信跳转 | taobao.com / cmbt.cn→cmbchina.com | ℹ️ 正常 |

## 分级与建议

| 级别 | 评分 | 处理 |
|:-----|:----:|:-----|
| 🔴 高 | ≥40 | 不要点击/不输入任何信息；已访问过则立即改相关账号密码 |
| 🟡 中 | 15~39 | 谨慎——先核实来源，短链看真实目标，陌生站不输凭据 |
| 🟢 低 | <15 | 未见明显风险特征，可正常访问 |

## 流程（脚本之外还要做的）

1. `linkcheck <url>` 拿分级
2. **🔴/🟡 → 结合上下文判断**：来源是谁？为什么发？是否符合常理？可疑就报告「有风险，建议不点」
3. **短链 → 让 linkcheck 展开**（默认就展开），看真实目标域
4. 涉及仿冒品牌 → 提示「疑似仿冒 XXX，官方域名是 XXX」
5. **收到短信 → 先对模板表**（见 references），再跑 linkcheck

## 参考

| 要看什么 | 打开 |
|:---------|:-----|
| 短信诈骗模板全量（6类+话术+速查表） | `references/sms-fraud-patterns.md` |
| 可信短链白名单（10个已验明）+ 收藏夹扫描 | `references/verified-shorteners.md` |
| 威胁情报源调研（微步接入/淘汰项） | `references/threat-intel-sources.md` |
| **收藏夹精选**（私档：AI项目/产品/工具/MOD/ACG/教程/关联） | 不在本仓 |

## 威胁情报增强（可选）

配置**微步在线云 API key**（放环境变量 `THREATBOOK_API_KEY`；作者环境用凭据工具 `credman` 存取，未单独公开。无 key 自动跳过，功能不退化）：
- 域名分析（`/v3/domain/query`）— 恶意标记、威胁类型、judgments
- URL 信誉报告（`/v3/url/report`）— 多引擎扫描判定

详见 `references/threat-intel-sources.md`。
