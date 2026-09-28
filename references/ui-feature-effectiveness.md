# 网页交互入口实效核查（按钮/开关/旧版回退入口「还能用吗」）

> 触发：有人问「X 页面那个 Y 按钮起作用吗 / 还能用吗」。
> 核心判据：**按钮还在 ≠ 按钮有效。** 页面上留着入口，多半是前端没删干净，服务端早就不认那条通道了。

## 一、三层判据（缺一层不下结论）

| 层 | 看什么 | 判法 |
|:--|:-------|:-----|
| ① 副作用 | 点击后有没有写 cookie / 改 localStorage / 发新请求 | 有 = 前端逻辑还活着（不是死链） |
| ② 落点 | **reload 或二次进入后，页面有没有真的切过去**（URL / 布局 / DOM 状态） | 没变 = 服务端不认，功能已失效 |
| ③ 反向入口 | 切换类开关成功时一般会出现回程按钮（「回到新版」之类） | 回程按钮不出现 = 没切成 |

**只做①最容易误判**：把结论写成「按钮确实写了 cookie X 并重发了请求」，会被当成「有用」。结论必须落到②——一句话概括：**它举手了，但没开门。**

## 二、配方（Playwright）

1. 探测脚本落宿主 agent 允许的写目录（作者环境是「工作目录下的 tmp/」）——写系统临时目录常被拒。
2. `Executable doesn't exist` 时：`find / -name chrome-headless-shell 2>/dev/null | head -1` 拿实际路径，`chromium.launch(headless=True, executable_path=...)`——版本目录号会变，**别写死**（同坑见 vision-recognition-traps、platform-content-extraction `references/weibo.md §五`）。
3. **两种身份各测一次**：访客态 + 登录态。访客页上的入口可能本来就不给访客用，DOM 容器名会不同（如 `xxx--visitor` vs `xxx--member`），只测一种得出的是半截结论。带登录态＝把 Netscape 格式 cookie 解析成 `{name,value,domain,path,secure}` 喂 `ctx.add_cookies()`；本机 B 站 cookie 文件用 `bin/bili-cookie-path --file <path>` 生成。
4. 一次 dump 齐：目标元素的**祖先链**（`span → .xxx__btn → .xxx-sidebar → …`，看清挂在哪个容器）、点击前后 `ctx.cookies()` 与 `localStorage` 的 diff、点击后新发的请求、**reload 后的 URL / 首段文字 / 入口是否还在**。
5. 报结论分两层写：「按钮做了什么」（副作用）＋「结果是什么」（落点没变），别只报前半段。

## 三、实测档案

**B 站动态页 `t.bilibili.com` 的「回到旧版」按钮**（实测沉淀）：访客态与登录态各点一次，均写入 cookie `go-back-dyn=1` 并重发 `GET https://t.bilibili.com/`；reload 后 URL 不变、仍是新版信息流布局、「回到旧版」四字原地不动 → **不生效**。`go-back-dyn` 是官方旧通道名（早期靠它回旧动态页），现服务端不再返回旧版模板。旁证：站内「回旧版」类入口在陆续下线（专栏旧版按钮更早就没了），真要回旧版只剩第三方脚本/插件那条路。

## 四、纪律

- 别拿「按钮写 cookie 了」当「按钮有效」——那只是①。
- 别只跑一次未登录请求就下结论——未登录页常是另一套模板。
- **登录态测出来的账号信息不许进结论、更不许进群聊**（账号＝用户隐私）。
