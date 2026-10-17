# 圣经全景 · 欧陆改革宗学习图谱

内容版本：2026-10-17 / v1.3.0。沿用现有仓库和公开域名，避免历史链接失效。

主页现已整合全景神学、历史时间线、列王、地理文化、圣约、三大信经和66卷导读；正文默认平铺展开。已取消顶部快捷链接与跳转横幅，采用“主题 → 小节 → 书卷”多级目录。桌面目录可隐藏以扩展正文，手机使用支持 Escape 关闭及键盘焦点约束的抽屉。

保留可播放、暂停、拖动的年代游标、列王联动和地图路线动画，并加入思维图、五步释经流程、故事线、分类色块、夜读、字号调节、阅读进度及设备系统语音朗读。地图和比较表在窄屏内使用独立横向视口，不撑破页面。列王顺序表不是同步纪年表，地图不是比例或精确路线图。

三份普世信经分别从指定网站提取正文，保留字词、标点和编号，数据文件附 SHA-256；构建时验证摘要，浏览器检查主页和干净版段落文本一致。`creeds.html` 提供独立干净阅读与单篇／三篇打印；主页提供遮文背诵和逐段揭示。82张回忆卡可按历史、信经神学、66卷分类；复习记录只存在本设备。

## 本地构建

运行 `npm run build`，先合成统一主页、学习台兼容页与干净信经页，再重建 `dist/` 并复制66卷独立页面及资源。以任意静态服务器提供该目录。Vercel 使用 `vercel.json`，GitHub Pages 使用 `.github/workflows/pages.yml`。构建只用 Node 内置模块，无需安装依赖。

可编辑源文件：`content/reader.html`（主页结构与核心讲解）、`content/history.html`（历史与圣约）、`assets/books.json`（66卷导读）、`assets/creeds.json`（来源原文与摘要）、`assets/reader.css` 和 `assets/reader.js`（阅读界面）。`index.html`、`study.html`、`creeds.html` 由 `scripts/compose-reader.mjs` 合成。旧 `build/build_site.py` 保留作历史工具，不是当前主页生成入口。

## 公开部署状态

三个平台继续使用稳定名称 `bible-reformed-atlas-20261017-v1-2`；页面内以 v1.3.0 标记本次内容更新。下列站点已上线，本次版本由同一提交触发三平台同步更新。

| 平台 | 公开地址 | 状态 |
| --- | --- | --- |
| GitHub Pages | https://07-je-gt-love-personal-20260918.github.io/bible-reformed-atlas-20261017-v1-2/ | 已发布并核验 |
| Surge | https://bible-reformed-atlas-20261017-v1-2.surge.sh | 已发布并核验 |
| Vercel | https://bible-reformed-atlas-20261017-v1-2.vercel.app | 已发布并核验 |

已沿用用户指定的旧仓库 `bible-reformed-atlas-20260919`，原地改名为 [bible-reformed-atlas-20261017-v1-2](https://github.com/07-Je-GT-Love-Personal-20260918/bible-reformed-atlas-20261017-v1-2)，保留已有提交历史。本地 origin 保留既有 Sites 源仓库，目标 GitHub 仓库通过官方 API 增量更新，非强制覆盖。

## 验证与维护

已通过真实 Chromium 在 320、360、390、768、1024、1440、1920 像素宽度执行检查：无页面横向溢出、无 JavaScript 异常、固定阅读控件无互相重叠；多级目录定位、手机抽屉、66卷筛选、原文段落一致性、背诵揭示、打印范围、动画、字号放大、夜读和复习记录均通过。检查脚本：`scripts/verify-browser.mjs`；需将 Playwright 安装在 `.deploy/tools` 并安装 Chromium。构建本身不依赖此工具。

GitHub Pages 随 `main` 或 `master` 分支提交自动发布。Vercel 已连接上述 GitHub 仓库，后续提交由 Git 集成触发构建；也可运行 `vercel deploy --prod`。Surge 自动发布工作流位于 `.github/workflows/surge.yml`，使用仓库加密 Secret `SURGE_TOKEN`；也可手动运行 `surge dist bible-reformed-atlas-20261017-v1-2.surge.sh`。GitHub 发布助手读取隐藏令牌，不保存凭据，基于远端当前提交创建新提交，保留远端其他文件。

## 编辑与来源状态

三份历史信经原文来自 [ccifellowship.org](https://ccifellowship.org)，具体页面及提取日期见数据文件与正文来源栏。正文外的历史和神学解释为编辑内容。亚他那修信经来源正文编号止于42，本版保持来源编号，不按其他版本重排。现代段落标签、记忆口诀、讲解和操作控件不属于信经原文。

三项联合信条目前提供主题概述及原文入口，尚未完整收录其全文；未声称吸收指定网站全部文章。66卷内容是导读，尚不是逐章逐节注释。历史争议应结合一手资料继续核读。修正了旧列王纪页将前966年误写为圣殿完成年份的问题：常见重建以前966年为开工、前959年为建成。

禁止将任何账号密码、访问令牌或部署密钥提交到仓库。部署认证应通过平台凭据管理完成。
