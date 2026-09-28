# 可信短链白名单 + 收藏夹扫描

## 可信短链（已逐一验明，2026-08-02）

| 短链域名 | 官方主域 | 验证记录 |
|:---------|:---------|:---------|
| `cmbt.cn` | cmbchina.com | 知乎多方确认+招行官方通告 |
| `go.abchina.com` | abchina.com | 2026-09-08 实测 302 → wx.abchina.com/webank（农行掌银H5）；已补 link_rules 品牌表 |
| `c.139.com` | 139.com / mcloud.139.com | 2026-09-08 实测 → m.mcloud.139.com 中国移动云盘（title 验证）|
| `b23.tv` | bilibili.com | B站分享链接标准格式 |
| `dx.10086.cn` | 10086.cn | 移动主域子域 |
| `s.mi.cn` | mi.cn | 小米主域子域 |
| `3.cn` | jd.com | 实测跳 www.jd.com |
| `u.jd.com` | jd.com | 京东生态确认 |
| `y.m.cn` | pizzahut.com.cn | location 头实测跳 mkt.pizzahut.com.cn |
| `t.hk.uy` | asus.com.cn | 实测跳 wap.asus.com.cn（.uy 后缀） |
| `c.didi.cn` | didi.cn | didi.cn 主域子域 |
| `c.tb.cn` | taobao.com | tb.cn 系官方 |

**判定规则：**
- 命中此表 → 跳转必须落在对应官方主域才判绿
- 官方短链跳到非官方域 → 仍报红（tag: redirect-mismatch）
- **新增候选域名必须先验证**（whois/官方通告/多方确认）再进 `TRUSTED_SHORTENER_MAP`
- 注意：官方短链不一定是常见后缀（t.hk.uy 是 .uy 乌拉圭），验证跳转落点才是关键

## 生态域名豁免（品牌词在正当生态站不算仿冒）

`BRAND_SUFFIX_WHITELIST` 覆盖：steamcommunity / steamdb / steampp / steamzg / augmentedsteam / steamreview / biligame / biligames 等。
新增生态站需手动补。

## 收藏夹扫描（配套工具）

用户的主力收藏夹归档在 `workspace/favorites/`（原档/索引/风险报告见该目录 README）。

```bash
# 解析书签 HTML → URL 清单
python3 skills/link-safety-check/scripts/parse_bookmarks.py <书签.html> --urls > urls.txt

# 批量风险扫描（静态检测，不碰目标站）
while read u; do bin/linkcheck "$u" --no-follow --json; done < urls.txt
```

### 收藏夹判定经验（2026-08-02 实测 578 域名）

- 本地/局域网 IP（127.0.0.1、192.168.x、校园网 portal）会报🔴但实际正常——自家工具（SD WebUI 7860、路由器 192.168.1.1 等）
- `.top/.xyz` 资源站报🟡但大概率正经——用时留意，不构成「别碰」
- 裸 IP 外部论坛、punycode 混搭域名、仿冒品牌跳转站才是真高风险
- 域名含数字的随机短串（xsx700.cc、45008.cn）是赌博/引流站特征

## 已知边界

- 脚本是静态特征 + 跳转展开 + 微步情报核验，不是全量病毒扫描——0day/新恶意内容可能漏
- 高危 TLD 是概率信号——`.xyz` 也有正规站，结合其他维度综合判断
- 微步 URL 扫描对未收录的新 URL 可能返回空，此时以静态检测 + 域名情报为准
- 不跳转的随机短域名只能提中风险，必须结合短信话术（见 sms-fraud-patterns.md）才能定诈骗
