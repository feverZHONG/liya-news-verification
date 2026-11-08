# 邮件原件验真（.eml 头 + 全链接域名）

> 适用：收到「官方通知」类邮件——安全提醒、强制 2FA、账号变更、订单/赔付、封号警告——要判**这封是不是真从官方发出的**。
> 铁律一句：**截图能看文案，看不了身份**。文案可以逐字照抄，发件人和链接域名抄不了。要判真伪必须拿 `.eml` 原件。

## 0. 先要原件

```bash
bin/eml --raw-headers -f <file>.eml      # 头 + 正文 + 链接 + 注意点
bin/eml --json <file>.eml                # 管道用
bin/eml -d /tmp/att <file>.eml           # 附件落盘
```

QQ/Outlook 里「显示原文/下载邮件」，落到 `cache/documents/` 的 `.eml` 直接喂。**只有截图时**：可以给出「文案像真的」这半句结论，身份层写「未核」，别把「模板一致」说成「邮件为真」。

## 1. 四道判据（缺一条就只说「存疑」）

| # | 看什么 | 判据 |
|:--|:-------|:-----|
| 1 | `From:` 地址域 | 显示名随便填（`GitHub <noreply@github.com>` 里前面的 GitHub 不算证据），**只认 `@` 后面的域** |
| 2 | `Authentication-Results:` | **SPF / DKIM / DMARC 三个都 pass**，且 DKIM 的 `d=` 与 From 域**对齐**（`d=github.com` ↔ `@github.com`）。任一 fail / softfail / none = 红灯 |
| 3 | 发信 IP 是否属服务商官方网段 | SPF pass 已代表「该 IP 在对方的 SPF 授权表内」，再加一层硬核对：拿 IP 去对服务商自己公布的网段。GitHub 用 `curl -s https://api.github.com/meta`（`hooks`/`web` 数组，例 `192.30.252.0/22`） |
| 4 | **全部** URL 的域名 | 从 raw MIME 抽，不从渲染后的正文抽（锚文本可伪装，`Click here` 后面可能是任意域）。只认服务商主域及官方子域；出现 `github.com.evil.com`、`github-support.*`、`github.io` 这类一律红 |

抽全链接 + 查外部资源（顺手一跑，不用写脚本落盘）：

```bash
python3 - <<'EOF'
import re,sys
raw=open(sys.argv[1],'rb').read().decode('utf-8','replace')
for d in sorted({re.match(r'https?://([^/]+)',u).group(1) for u in set(re.findall(r'https?://[^\s"\'<>)]+',raw))}):
    print(d)
print('-- img src --')
for s in re.findall(r'<img[^>]+src="?([^"\s>]+)',raw)[:10]: print(s[:160])
EOF
```

- **无外部图片 / 无追踪像素**是加分项，**不是判据**——很多正常官方邮件也带追踪像素，别拿它单条定真。
- 图片若指向陌生域，即使正文全对也要标出来（像素回传 = 你点开就报活）。

## 2. 内容层交叉：模板日期算得出来才是真模板

官方通知类邮件常带**自动计算的期限**（「N 天内」「by <日期>」）。拿它跟发信时间对一遍：

- 算得上（例：GitHub 强制 2FA = 入选日 00:00 UTC **+45 天**，45 天整）⇒ 内容来自真模板，加分
- 算不整（差几天又没解释、日期比发信还早）⇒ 模板被改过或来自旧批次，转存疑
- 换算到 +8 再出口：`12-04 00:00 UTC` = `12-04 08:00 CST`，报给用户时连宽限期一起写

## 3. 判真之后：仍然不从邮件里跳

**验真 ≠ 以后可以点邮件链接。** 结论里要写「这封是真的」，同时写「操作照旧从地址栏手打官方入口」（如 `github.com/settings/security`）。理由不是这一封，是让「安全操作只从地址栏走」变成条件反射——防的是下次做得一模一样的假货。

## 4. 落档

把验真证据一起写进台账（发件人、SPF/DKIM/DMARC、发信 IP 与网段来源、全部链接域名、发出时间换算 +8、截止与宽限日期）。下次同一件事只需回看台账，不用重跑一遍。台账里**别只写「已验真」**——那是结论没有依据，下一个人无法复核。

## 5. 处置口径：GitHub 强制 2FA 通知（验真之后怎么答）

（本段属 GitHub 账号安全，`github-ops` 为用户自有技能不可自动写入，先落在这里；日后归档可搬过去。）

- **程序**：GitHub 自 2023-03 起要求贡献代码的账号开 2FA。入选 → 通知邮件 → **45 天注册期 → 7 天宽限 → 限制访问 github.com（push 一并断）**。入选条件：发 release、为他人发 Action、高重要性仓库维护者/管理员、组织 owner、软件包仓库贡献者等
- **截止算法**：截止 = 入选日 `00:00 UTC` + 45 天整；出口换 +8（例：`12-04 00:00 UTC` = `12-04 08:00 CST`），宽限再 +7 天。**邮件到达时间 ≠ 窗口起点**（窗口按 UTC 日期整点起算），落档两行分开写
- **方法选型**：TOTP 应用首选（官方明确「美国以外 SMS 不如 TOTP 可靠」，+86 送达不稳）；SMS 仅补救；passkey / GitHub Mobile 作**第二方法**，防单设备丢失
- **recovery codes 必须下载并加密存档**（`credman`，不落明文）——丢了就是账号锁死，没有第二条路
- **开通后 28 天 checkup 期**：期间成功过一次 2FA 即通过，否则第 28 天要求现存会话验一次
- **启用 2FA 不吊销已颁发的 token / SSH key**：PAT、`gitpush`、`gh` 照常工作，唯一变化是浏览器登录多一步——**别拿「怕 push 断」当拖延理由**，真正会断的是宽限期满还没开
- **本机查不出 2FA 状态**：细粒度 PAT 调 `GET /user` 不返回 `two_factor_authentication`（该字段需 classic token + `user` scope）。**字段缺失只能写「查不到」，既不能读成 false 也不能读成 true**
- 操作入口手打：`github.com/settings/security` → Password and authentication → Enable two-factor authentication

## 常见误判

- **「正文跟官方模板逐句一致」当铁证**：钓鱼最爱照抄模板，文案层永远可复制。
- **只看 From 显示名**：`GitHub Team <xxx@evil.com>` 在手机邮件列表里长得一模一样。
- **拿 QQ/邮箱客户端的「安全」标当验证**：客户端只复述 SPF/DKIM 结果，仍要看原始头。
- **把缺字段读成否定**：头部缺失/字段不返回 ≠ false。查不到就写「查不到」。
