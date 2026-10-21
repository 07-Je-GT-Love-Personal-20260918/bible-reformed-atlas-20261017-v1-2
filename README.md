# 圣经全景 · 救赎历史与逐卷精读

**bible-reformed-atlas-20261021-v1-4-GTstudy · 2026-10-21 · v1.4.0**

沿用同一个 GitHub 仓库（ID 1376927002）原地改名，保留全部历史；没有创建重复仓库。主线为欧陆改革宗、圣约神学、圣经神学与救赎历史。

## 三个公开站点与仓库

| 平台 | 地址 |
| --- | --- |
| GitHub Pages | https://07-je-gt-love-personal-20260918.github.io/bible-reformed-atlas-20261021-v1-4-GTstudy/ |
| Vercel | https://bible-reformed-atlas-20261021-v1-4-gtstudy.vercel.app/ |
| Surge | https://bible-reformed-atlas-20261021-v1-4-gtstudy.surge.sh/ |
| 源码仓库 | https://github.com/07-Je-GT-Love-Personal-20260918/bible-reformed-atlas-20261021-v1-4-GTstudy |

Vercel 与 Surge 的旧域名保留为兼容入口。GitHub 仓库改名后 Pages 使用上述新路径；旧 Pages 项目路径不保证自动跳转。

## v1.4 更新

- 四套可点击主题：羊皮暖金、玉色森林、云海晴蓝、深海夜读；主题跨页面保存在本机。
- 两层轻量云状浮动装饰；可以关闭，尊重系统“减少动态效果”，离开视口和切换后台时暂停。
- 三张主要配图由约 7.95 MB PNG 改为约 0.49 MB WebP；原 PNG 保留供恢复。独立书卷页移除 Google Fonts 远程依赖。
- 修复目录原生跳转与脚本平滑滚动同时执行的问题；搜索短延迟合并；支持 CSS 原生滚动进度，回退方案缓存高度并按帧更新；远处书卷卡片延后绘制，正文仍全部存在且默认展开。
- 正文选择文字后可加金色底纹、蓝色实线、玫红虚线，附个人理解；本机保存，支持定位、逐条删除和 Markdown 导出。信经原文区不叠加个人标记。升级后引用位置不匹配的旧笔记保留，不错误套用到新文字。
- 66卷统一独立精读页：背景、结构、全书论证、各卷专属重点段落与讨论答案、圣约与基督、应用、记忆路线。旧书卷文件名保留，包括《雅歌》的历史别名。
- 新增六个救赎核心问题、四层福音关系比较表、三个诸王时代因果区、五组同名与年代辨析；重点使用粗体、主题色、金底纹、虚线区分。
- 保留动态历史游标、路线图、列王表、文化地图、三份信经比较、背诵和系统语音；取消打印按钮与调用。

## 原文与解释的边界

三份既有普世信经来自 ccifellowship.org，2026-10-21 再次抓取核验，段落与已有数据逐字一致，SHA-256 不变；来源与摘要在 `assets/creeds.json`。构建验证摘要。干净阅读页为 `creeds.html`。现代标签、记忆提示与神学解释不属于原文。亚他那修信经依指定来源止于42，不重排为其他版本编号。

三项联合信条提供指定网站原文目录、条文定位和原创解释；未取得该站现代中文译文全文转载授权，不另行整站复制或声称已吸收所有文章。其他教会与神学院资源为参考入口，未浏览的内容不标为已核验依据。66卷释读不是完整逐章逐节注释；古代纪年保留约数与争议，地图是教学示意。

## 构建与持续部署

`npm run build`：先生成66卷，再合成统一主页、学习页和信经阅读页，最后输出 `dist/`。构建只用 Node 内置模块，不需要框架运行时。`python scripts/verify-static.py` 检查文件、锚点和66卷完整性。

编辑入口：`content/reader.html`、`content/core-depth.html`、`content/history.html`、`assets/books.json`、`data/study-notes-20261003.tsv`、`data/book-context.json`、`assets/experience.css` 与 `assets/experience.js`。生成页面也一并提交，方便直接恢复。

GitHub Pages 与 Surge 沿用工作流。Surge 使用仓库加密 Secret `SURGE_TOKEN`，同时发布新旧域名；Vercel 沿用现有项目 ID `prj_77MJ8md0LyZWHxv3T7QdvzWll2k4`，新增版本域名，不移除旧域名。任何 token、密码或私钥不得进入源码、提交、构建输出或公开日志。

## 固定版本与恢复

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.3.0 | 2026-10-17 | 更新前固定提交 `42b0d53f535b662dfbcd5c72062b3b24845f3683`；统一主页、三份信经与复习工具 |
| v1.4.0-GTstudy | 2026-10-21 | 性能、四主题、持久笔记、66卷独立释读与核心内容增强 |

更新前源码保存在分支 `archive/20261021-before-v1.4-GTstudy`，发布标签 `v1.3.0-20261017-before-GTstudy` 指向同一固定提交。需要恢复时从固定提交新建恢复分支，运行构建并检查，再以正常提交更新主分支；不要强推覆盖历史。

验证记录见 `docs/verification-20261021.md`。实测结论只覆盖记录中的设备与浏览器，不承诺所有终端恒定帧率。
