---
tier: T2  # 随 news-verification 主 skill
---

# 图片直链存活校验（图床 / 镜像站）

> 2026-10-01 从 SKILL.md「模块 C+」拆出，内容一条未删。

---

### I · 图片直链存活校验（镜像站 403 ≠ 图没了）

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
