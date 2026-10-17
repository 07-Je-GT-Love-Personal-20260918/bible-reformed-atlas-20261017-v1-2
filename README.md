# 圣经全景 · 欧陆改革宗学习图谱

版本：2026-10-17 / v1.2。

现有66卷速览与独立书卷页，新增历史与圣约学习台（`study.html`）：时间坐标、完整南北列王顺序、古代近东方位示意、圣约进展、三大信经对照和主动回忆卡。列王表左右仅表示各国先后顺序，不是同步纪年表。

动画学习台已同时接入首页和学习台：可播放、暂停、拖动的年代游标，南北列王随年代联动，六个事件跳转，以及可切换被掳／归回方向的 SVG 地图路线动画。默认不自动播放，页面离开前台时暂停，并尊重系统减少动态效果设置。

## 本地构建

运行 `npm run build`，将首页、学习台、66卷页面及资源完整复制到 `dist/`。以任意静态服务器提供该目录。Vercel 使用 `vercel.json`，GitHub Pages 使用 `.github/workflows/pages.yml`。无需安装依赖即可构建。

## 公开部署状态

三个平台采用统一版本名 `bible-reformed-atlas-20261017-v1-2`。2026-10-17 已公开访问核验首页均返回 HTTP 200，且包含 v1.2 动画脚本；Vercel 与 Surge 的学习台页也已核验 HTTP 200。

| 平台 | 公开地址 | 状态 |
| --- | --- | --- |
| GitHub Pages | https://07-je-gt-love-personal-20260918.github.io/bible-reformed-atlas-20261017-v1-2/ | 已发布并核验 |
| Surge | https://bible-reformed-atlas-20261017-v1-2.surge.sh | 已发布并核验 |
| Vercel | https://bible-reformed-atlas-20261017-v1-2.vercel.app | 已发布并核验 |

已沿用用户指定的旧仓库 `bible-reformed-atlas-20260919`，原地改名为 [bible-reformed-atlas-20261017-v1-2](https://github.com/07-Je-GT-Love-Personal-20260918/bible-reformed-atlas-20261017-v1-2)，保留已有提交历史。本地 origin 保留既有 Sites 源仓库，目标 GitHub 仓库通过官方 API 增量更新，非强制覆盖。

## 验证与维护

已通过真实 Chromium 在 360、390、768、1440 像素宽度对首页及学习台执行检查：无页面横向溢出、无 JavaScript 异常；年代跳转、王国状态、播放暂停、地图切换、目录开关和答案揭晓均通过。检查脚本：`scripts/verify-browser.mjs`；需将 Playwright 安装在 `.deploy/tools` 并安装 Chromium。构建本身不依赖此工具。

GitHub Pages 随 `main` 或 `master` 分支提交自动发布。Vercel 已连接上述 GitHub 仓库，后续提交由 Git 集成触发构建；也可运行 `vercel deploy --prod`。Surge 自动发布工作流位于 `.github/workflows/surge.yml`，使用仓库加密 Secret `SURGE_TOKEN`；也可手动运行 `surge dist bible-reformed-atlas-20261017-v1-2.surge.sh`。GitHub 发布助手读取隐藏令牌，不保存凭据，基于远端当前提交创建新提交，保留远端其他文件。

## 编辑与来源状态

指定原文来源为 [ccifellowship.org](https://ccifellowship.org)。学习台的信经与信条说明均为编辑概述，原文阅读链接指向该网站。尚未完成六份文件全文逐字校勘、转载授权核查、三份独立原文背诵页，也未完成指定网站全站资料吸收。内容不是66卷逐章注释的完成版。地图为非比例方位示意；古代纪年及有争议的解释应继续核对一手资料。

禁止将任何账号密码、访问令牌或部署密钥提交到仓库。部署认证应通过平台凭据管理完成。
