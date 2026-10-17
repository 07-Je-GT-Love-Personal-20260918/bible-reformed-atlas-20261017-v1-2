# -*- coding: utf-8 -*-
"""
构建「圣经六十六卷·改革宗解读」多文件网站。
- 从 bible-66-overview.html 解析已有的书卷元数据（单一真相源）
- 叠加 content.py 中的改革宗神学层
- 生成 index.html + assets/site.css + books/NN-slug.html（内嵌 SVG 配图）
"""
import os, re, json, html
from content import EXTRA, HOME_INTRO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "bible-66-overview.html")

# ─────────────────────────────────────────────
# 1. 解析现有 JS 数据（SECTIONS / TIMELINE）
# ─────────────────────────────────────────────
def js_to_json(s):
    # 原始 JS 全部用单引号作字符串定界符、键名不带引号；
    # 因此此刻所有 ASCII 双引号都是「内容」，必须先转义。
    SENT = "\x00"
    s = s.replace("\\'", SENT)                                   # 转义的撇号占位
    s = s.replace('"', '\\"')                                    # 内容中的双引号转义
    s = re.sub(r'([\{\[,]\s*)([A-Za-z][A-Za-z0-9]*)\s*:', r'\1"\2":', s)  # 给键加引号
    s = s.replace("'", '"')                                      # 单引号定界符→双引号
    s = s.replace(SENT, "'")                                     # 还原撇号
    s = re.sub(r',(\s*[\]\}])', r'\1', s)                        # 去尾逗号
    return json.loads(s)

with open(SRC, encoding="utf-8") as f:
    HTML = f.read()

m_sec = re.search(r'const SECTIONS\s*=\s*(\[.*?\n\]);', HTML, re.S)
m_tl  = re.search(r'const TIMELINE\s*=\s*(\[.*?\n\]);', HTML, re.S)
SECTIONS = js_to_json(m_sec.group(1))
TIMELINE = js_to_json(m_tl.group(1))

# 展平成书卷有序列表，附带类别信息
BOOKS = []
for si, sec in enumerate(SECTIONS):
    for b in sec["books"]:
        b = dict(b)
        b["_sec"] = si
        b["_secid"] = sec["id"]
        b["_sectitle"] = sec["title"]
        b["_color"] = sec["color"]
        b["_gradient"] = sec["gradient"]
        b["_icon"] = sec.get("icon", "")
        BOOKS.append(b)
assert len(BOOKS) == 66, f"expected 66 books, got {len(BOOKS)}"

def slug(eng):
    return re.sub(r'[^a-z0-9]+', '-', eng.lower()).strip('-')

for i, b in enumerate(BOOKS):
    b["_idx"] = i
    b["_num"] = i + 1
    b["_slug"] = slug(b["eng"])
    b["_file"] = f"{i+1:02d}-{b['_slug']}.html"

TESTAMENT_SPLIT = 39  # 前39卷旧约

def esc(x):
    return html.escape(str(x), quote=True)

# ─────────────────────────────────────────────
# 2. 共享 CSS
# ─────────────────────────────────────────────
CSS = r"""
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  color-scheme:light dark;
  --parch:#FAF6F0; --parch2:#F3ECE0; --ink:#2C2416; --ink2:#5A5040;
  --gold:#B8860B; --gold-l:#D4A843; --line:rgba(184,134,11,.22);
  --card:#FFFDF9; --prose:#39311f; --shadow:0 4px 24px rgba(44,36,22,.08);
  --serif:'Noto Serif SC','Source Han Serif SC','Songti SC','STSong','SimSun',Georgia,serif;
  --sans:'Noto Sans SC','PingFang SC','Microsoft YaHei',system-ui,sans-serif;
}
/* 深色主题（皮革+烫金的夜间形态）——令牌级切换 */
@media (prefers-color-scheme:dark){:root{
  --parch:#171310; --parch2:#20190f; --ink:#ECE3D2; --ink2:#A99A7C;
  --line:rgba(184,134,11,.30); --card:#221a12; --prose:#ddd0b8;
  --shadow:0 6px 26px rgba(0,0,0,.45);
}}
:root[data-theme="dark"]{
  --parch:#171310; --parch2:#20190f; --ink:#ECE3D2; --ink2:#A99A7C;
  --line:rgba(184,134,11,.30); --card:#221a12; --prose:#ddd0b8;
  --shadow:0 6px 26px rgba(0,0,0,.45);
}
:root[data-theme="light"]{
  --parch:#FAF6F0; --parch2:#F3ECE0; --ink:#2C2416; --ink2:#5A5040;
  --line:rgba(184,134,11,.22); --card:#FFFDF9; --prose:#39311f;
  --shadow:0 4px 24px rgba(44,36,22,.08);
}
html{scroll-behavior:smooth;font-size:16px}
body{font-family:var(--sans);background:var(--parch);color:var(--ink);
  line-height:1.85;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
::selection{background:rgba(184,134,11,.22)}
::-webkit-scrollbar{width:8px;height:8px}
::-webkit-scrollbar-thumb{background:var(--gold);border-radius:4px}
::-webkit-scrollbar-track{background:var(--parch2)}

.wrap{max-width:960px;margin:0 auto;padding:0 1.4rem}
.wrap-wide{max-width:1240px;margin:0 auto;padding:0 1.4rem}

/* top bar */
.topbar{position:sticky;top:0;z-index:50;background:rgba(250,246,240,.9);
  backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.topbar-in{max-width:1240px;margin:0 auto;padding:.7rem 1.4rem;display:flex;
  align-items:center;gap:1rem;justify-content:space-between}
.brand{font-family:var(--serif);font-weight:700;letter-spacing:.04em;font-size:1.02rem}
.brand span{color:var(--gold)}
.topnav{display:flex;gap:1.2rem;font-size:.86rem;color:var(--ink2)}
.topnav a:hover{color:var(--gold)}

/* hero (home) */
.hero{position:relative;overflow:hidden;color:#FAF6F0;
  background:linear-gradient(160deg,#1a1510,#2C2416 45%,#3d2e1a);
  padding:5.5rem 1.4rem 4.5rem;text-align:center}
.hero::before{content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse at 50% 25%,rgba(184,134,11,.18),transparent 60%)}
.hero-in{position:relative;z-index:1;max-width:820px;margin:0 auto}
.hero .cross{font-size:2.4rem;color:var(--gold-l)}
.hero h1{font-family:var(--serif);font-weight:900;letter-spacing:.08em;
  font-size:clamp(2.1rem,5.5vw,3.4rem);margin:.6rem 0}
.hero .sub{color:var(--gold-l);letter-spacing:.14em;font-size:clamp(.9rem,2vw,1.1rem)}
.hero .persp{margin-top:1.4rem;color:rgba(250,246,240,.72);font-size:.94rem;
  max-width:640px;margin-inline:auto}
.hero-stats{display:flex;gap:2.4rem;justify-content:center;margin-top:2.2rem;flex-wrap:wrap}
.hero-stats div{font-size:.78rem;color:rgba(250,246,240,.65);letter-spacing:.05em}
.hero-stats strong{display:block;font-family:var(--serif);font-size:1.7rem;color:var(--gold-l)}

/* section headings */
.sec{padding:3.4rem 0}
.sec-title{font-family:var(--serif);font-weight:700;font-size:1.6rem;text-align:center}
.sec-sub{text-align:center;color:var(--ink2);font-size:.92rem;margin-top:.35rem}
.rule{width:60px;height:3px;background:var(--gold);border-radius:2px;margin:1rem auto 2rem}

/* intro cards (home) */
.intro-grid{display:grid;gap:1.2rem}
.intro-card{background:var(--card);border:1px solid var(--line);border-radius:14px;
  padding:1.6rem 1.7rem;box-shadow:var(--shadow);position:relative;overflow:hidden}
.intro-card::before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;
  background:linear-gradient(var(--gold),var(--gold-l))}
.intro-card h3{font-family:var(--serif);font-size:1.15rem;margin-bottom:.55rem;color:var(--ink)}
.intro-card p{font-size:.96rem;color:var(--prose)}
.chips{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.9rem}
.chip{font-size:.74rem;background:var(--parch2);border:1px solid var(--line);
  color:var(--ink2);padding:.2rem .6rem;border-radius:100px}

/* category groups + book cards */
.catgroup{margin-top:2.6rem}
.cat-head{display:flex;align-items:center;gap:.7rem;margin-bottom:1rem;
  padding-bottom:.6rem;border-bottom:2px solid var(--line)}
.cat-badge{width:40px;height:40px;border-radius:11px;display:grid;place-items:center;
  color:#fff;font-size:1.2rem;flex-shrink:0}
.cat-head h3{font-family:var(--serif);font-size:1.22rem}
.cat-head .en{color:var(--ink2);font-size:.8rem;letter-spacing:.06em}
.cat-head .cnt{margin-left:auto;font-size:.78rem;color:var(--ink2)}
.book-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(178px,1fr));gap:.9rem}
.bcard{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:1rem 1.05rem;box-shadow:var(--shadow);transition:transform .18s,box-shadow .18s;
  display:flex;flex-direction:column;gap:.3rem;position:relative;overflow:hidden;min-height:118px}
.bcard::after{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;
  background:var(--c,var(--gold))}
.bcard:hover{transform:translateY(-3px);box-shadow:0 10px 28px rgba(44,36,22,.15)}
.bcard .bn{font-family:var(--serif);font-weight:700;font-size:1.05rem}
.bcard .be{font-size:.72rem;color:var(--ink2);letter-spacing:.04em}
.bcard .bt{font-size:.8rem;color:var(--prose);margin-top:.25rem;line-height:1.5}
.bcard .bnum{position:absolute;right:.7rem;top:.55rem;font-family:var(--serif);
  font-size:1.1rem;color:var(--line);font-weight:700}

/* timeline strip */
.figbox{background:#FBF7F0;border:1px solid var(--line);border-radius:14px;
  box-shadow:var(--shadow);padding:1.3rem;overflow-x:auto}
.figcap{text-align:center;color:#8a7a55;font-size:.82rem;margin-top:.7rem}

/* ===== book page ===== */
.bhero{position:relative;overflow:hidden;color:#fff;padding:3.4rem 1.4rem 2.8rem}
.bhero-in{max-width:960px;margin:0 auto;position:relative;z-index:1}
.bhero .kicker{font-size:.8rem;letter-spacing:.18em;opacity:.85;text-transform:uppercase}
.bhero h1{font-family:var(--serif);font-weight:900;font-size:clamp(2rem,6vw,3rem);
  letter-spacing:.06em;margin:.3rem 0 .1rem}
.bhero .en{font-family:var(--serif);opacity:.75;letter-spacing:.1em;font-size:1.05rem}
.bhero .meta{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.1rem}
.bhero .meta span{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.25);
  padding:.28rem .7rem;border-radius:100px;font-size:.8rem;backdrop-filter:blur(4px)}
.bhero .watermark{position:absolute;right:-.5rem;bottom:-2.5rem;font-family:var(--serif);
  font-weight:900;font-size:9rem;opacity:.08;z-index:0;line-height:1;white-space:nowrap}

.bmain{max-width:960px;margin:0 auto;padding:2.4rem 1.4rem 3rem}
.verse-hero{font-family:var(--serif);font-size:1.25rem;line-height:1.9;text-align:center;
  color:var(--ink);padding:1.6rem 1.4rem;border-top:1px solid var(--line);
  border-bottom:1px solid var(--line);margin:0 0 2.2rem;position:relative}
.verse-hero::before{content:'“';font-size:2.4rem;color:var(--gold);opacity:.5;
  font-family:Georgia,serif;line-height:0;vertical-align:-.4em;margin-right:.1em}

.block{margin:2.2rem 0}
.block-h{display:flex;align-items:center;gap:.6rem;margin-bottom:.9rem}
.block-h .idx{width:30px;height:30px;border-radius:8px;display:grid;place-items:center;
  color:#fff;font-size:.9rem;font-weight:700;flex-shrink:0}
.block-h h2{font-family:var(--serif);font-size:1.32rem;font-weight:700}
.block-h .en{color:var(--ink2);font-size:.76rem;letter-spacing:.08em;margin-left:.2rem}
.prose{font-size:1rem;color:var(--prose)}
.prose p{margin:.5rem 0}

.callout{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--gold);
  border-radius:10px;padding:1.1rem 1.3rem;box-shadow:var(--shadow)}
.twocol{display:grid;grid-template-columns:1fr 1fr;gap:1.1rem}
@media(max-width:680px){.twocol{grid-template-columns:1fr}}
.minicard{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:1.1rem 1.2rem;box-shadow:var(--shadow)}
.minicard h4{font-family:var(--serif);font-size:1rem;margin-bottom:.5rem;
  display:flex;align-items:center;gap:.4rem}
.minicard h4 .dot{width:9px;height:9px;border-radius:50%;background:var(--gold)}

ul.ticks{list-style:none;display:flex;flex-direction:column;gap:.6rem}
ul.ticks li{position:relative;padding-left:1.5rem;font-size:.96rem;color:var(--prose)}
ul.ticks li::before{content:'';position:absolute;left:0;top:.55em;width:8px;height:8px;
  border-radius:50%;background:var(--gold)}
ul.arrows li::before{content:'→';background:none;color:var(--gold);font-weight:700;
  top:0;left:0;width:auto;height:auto}

.outline-list{list-style:none;counter-reset:o;display:flex;flex-direction:column;gap:.5rem}
.outline-list li{position:relative;padding:.55rem .8rem .55rem 2.6rem;background:var(--card);
  border:1px solid var(--line);border-radius:9px;font-size:.92rem;counter-increment:o}
.outline-list li::before{content:counter(o);position:absolute;left:.7rem;top:50%;
  transform:translateY(-50%);width:22px;height:22px;border-radius:6px;color:#fff;
  display:grid;place-items:center;font-size:.72rem;font-weight:700;
  background:var(--c,var(--gold))}

/* prev/next */
.pager{display:flex;justify-content:space-between;gap:1rem;margin-top:2.6rem;
  border-top:1px solid var(--line);padding-top:1.6rem}
.pager a{flex:1;background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:.9rem 1.1rem;box-shadow:var(--shadow);transition:transform .16s}
.pager a:hover{transform:translateY(-2px)}
.pager .lbl{font-size:.72rem;color:var(--ink2);letter-spacing:.06em}
.pager .nm{font-family:var(--serif);font-weight:700;font-size:1.02rem;margin-top:.15rem}
.pager .next{text-align:right}
.pager .empty{visibility:hidden}

.backhome{display:inline-flex;align-items:center;gap:.4rem;font-size:.85rem;
  color:var(--ink2);margin-bottom:.4rem}
.backhome:hover{color:var(--gold)}

footer{background:#211b12;color:rgba(250,246,240,.66);text-align:center;
  padding:2.4rem 1.4rem;font-size:.82rem;line-height:1.8}
footer .verse{font-family:var(--serif);color:var(--gold-l);font-size:1rem;margin-bottom:.6rem}

.fade{opacity:0;transform:translateY(18px);transition:opacity .7s,transform .7s}
.fade.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.fade{transition:none}*{scroll-behavior:auto!important}}

/* 单文件版（Artifact）视图切换 */
.view{display:none}
.view.active{display:block}
"""

# ─────────────────────────────────────────────
# 3. SVG 生成器
# ─────────────────────────────────────────────
def svg_canonbar(active_sec):
    """圣经全景条：10 大类别，高亮当前书卷所属类别。"""
    W, H = 900, 118
    n = len(SECTIONS)
    seg = (W - 40) / n
    parts = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
             f'aria-label="圣经全景定位条" font-family="var(--sans)">']
    # testament labels
    ot_w = seg * 5
    parts.append(f'<text x="{20+ot_w/2:.0f}" y="16" text-anchor="middle" '
                 f'font-size="12" fill="#8a7a55" letter-spacing="4">旧约 · 应许</text>')
    parts.append(f'<text x="{20+ot_w+seg*5/2:.0f}" y="16" text-anchor="middle" '
                 f'font-size="12" fill="#8a7a55" letter-spacing="4">新约 · 成全</text>')
    for i, sec in enumerate(SECTIONS):
        x = 20 + i * seg
        act = (i == active_sec)
        col = sec["color"]
        op = "1" if act else ".30"
        parts.append(f'<rect x="{x:.1f}" y="30" width="{seg-4:.1f}" height="46" rx="7" '
                     f'fill="{col}" opacity="{op}"/>')
        if act:
            parts.append(f'<rect x="{x:.1f}" y="30" width="{seg-4:.1f}" height="46" rx="7" '
                         f'fill="none" stroke="{col}" stroke-width="2.5"/>')
        tcol = "#fff" if act else "#6b5f45"
        parts.append(f'<text x="{x+(seg-4)/2:.1f}" y="58" text-anchor="middle" '
                     f'font-size="11.5" fill="{tcol}" font-weight="{700 if act else 400}">'
                     f'{esc(sec["title"])}</text>')
    # divider旧新约
    dx = 20 + ot_w - 2
    parts.append(f'<line x1="{dx:.0f}" y1="26" x2="{dx:.0f}" y2="84" '
                 f'stroke="#c9b98f" stroke-dasharray="4 4"/>')
    parts.append(f'<text x="{dx:.0f}" y="98" text-anchor="middle" font-size="10.5" '
                 f'fill="#a08a5a">基督</text>')
    parts.append('</svg>')
    return "".join(parts)

def svg_outline_flow(book):
    """结构流程图：依大纲自动生成纵向段落。"""
    items = book["outline"]
    col = book["_color"]
    rowh, gap, top = 46, 14, 14
    W = 900
    H = top*2 + len(items)*rowh + (len(items)-1)*gap
    parts = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
             f'aria-label="{esc(book["name"])}结构图" font-family="var(--sans)">']
    cx = 40
    # spine
    parts.append(f'<line x1="{cx}" y1="{top+rowh/2:.0f}" x2="{cx}" '
                 f'y2="{H-top-rowh/2:.0f}" stroke="{col}" stroke-width="2" opacity=".35"/>')
    for i, it in enumerate(items):
        y = top + i*(rowh+gap)
        parts.append(f'<circle cx="{cx}" cy="{y+rowh/2:.0f}" r="15" fill="{col}"/>')
        parts.append(f'<text x="{cx}" y="{y+rowh/2+4:.0f}" text-anchor="middle" '
                     f'font-size="13" fill="#fff" font-weight="700">{i+1}</text>')
        parts.append(f'<rect x="{cx+28}" y="{y}" width="{W-cx-28-16}" height="{rowh}" rx="9" '
                     f'fill="#FFFDF9" stroke="{col}" stroke-opacity=".28"/>')
        parts.append(f'<text x="{cx+46}" y="{y+rowh/2+5:.0f}" font-size="14" fill="#39311f">'
                     f'{esc(it)}</text>')
    parts.append('</svg>')
    return "".join(parts)

def svg_timeline(items):
    """首页救赎历史时间轴。"""
    W = 1180
    n = len(items)
    seg = (W - 60) / (n - 1)
    H = 150
    baseY = 74
    parts = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
             f'aria-label="救赎历史时间轴" font-family="var(--sans)">']
    # base line gradient
    parts.append('<defs><linearGradient id="tlg" x1="0" y1="0" x2="1" y2="0">'
                 '<stop offset="0" stop-color="#1B4332"/><stop offset=".33" stop-color="#5B3A8C"/>'
                 '<stop offset=".55" stop-color="#9B2226"/><stop offset=".72" stop-color="#0A3D62"/>'
                 '<stop offset="1" stop-color="#922B21"/></linearGradient></defs>')
    parts.append(f'<line x1="30" y1="{baseY}" x2="{W-30}" y2="{baseY}" '
                 f'stroke="url(#tlg)" stroke-width="4" stroke-linecap="round"/>')
    for i, it in enumerate(items):
        x = 30 + i*seg
        up = (i % 2 == 0)
        col = it["color"]
        parts.append(f'<circle cx="{x:.0f}" cy="{baseY}" r="7" fill="{col}" '
                     f'stroke="#FAF6F0" stroke-width="2.5"/>')
        ly = baseY-16 if up else baseY+16
        anchor = 'text-anchor="middle"'
        parts.append(f'<line x1="{x:.0f}" y1="{baseY}" x2="{x:.0f}" '
                     f'y2="{ly + (7 if up else -7):.0f}" stroke="{col}" stroke-width="1.5" opacity=".5"/>')
        ty = baseY-24 if up else baseY+34
        yy = baseY-38 if up else baseY+50
        parts.append(f'<text x="{x:.0f}" y="{ty:.0f}" {anchor} font-size="12.5" '
                     f'fill="#2C2416" font-weight="700">{esc(it["label"])}</text>')
        parts.append(f'<text x="{x:.0f}" y="{yy:.0f}" {anchor} font-size="10.5" '
                     f'fill="#8a7a55">{esc(it["year"])}</text>')
    parts.append('</svg>')
    return "".join(parts)

# ─────────────────────────────────────────────
# 4. 页面模板
# ─────────────────────────────────────────────
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700;900&'
         'family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">')

REVEAL_JS = """
<script>
const io=new IntersectionObserver((es)=>{es.forEach(e=>{if(e.isIntersecting){
e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.12});
document.querySelectorAll('.fade').forEach(el=>io.observe(el));
</script>
"""

def page_head(title, css_href, extra=""):
    return (f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(title)}</title>{FONTS}'
            f'<link rel="stylesheet" href="{css_href}">{extra}</head><body>')

def topbar(prefix):
    return (f'<div class="topbar"><div class="topbar-in">'
            f'<a class="brand" href="{prefix}index.html">圣经六十六卷 · <span>改革宗解读</span></a>'
            f'<nav class="topnav">'
            f'<a href="{prefix}index.html">首页</a>'
            f'<a href="{prefix}index.html#intro">整全导论</a>'
            f'<a href="{prefix}index.html#books">书卷</a>'
            f'<a href="{prefix}bible-66-overview.html">速览总览</a>'
            f'</nav></div></div>')

FOOTER = ('<footer><div class="verse">'
          '「于是从摩西和众先知起，凡经上所指着自己的话，都给他们讲解明白了。」——路加福音 24:27'
          '</div>圣经六十六卷 · 欧陆改革宗正统神学解读 &nbsp;|&nbsp; '
          '愿荣耀唯独归于神（Soli Deo Gloria）</footer>')

# ---- 共享：首页正文（hero + 三大区块）----
def home_body(bookhref):
    """bookhref: 函数 b -> 链接地址。返回不含 topbar/footer 的首页正文。"""
    p = []
    p.append('<header class="hero"><div class="hero-in">'
             '<div class="cross">✝</div>'
             '<h1>圣经六十六卷</h1>'
             '<div class="sub">欧陆改革宗 · 正统神学 · 逐卷解读</div>'
             '<p class="persp">一部书，一个故事，一位中心。先从整本圣经与神学核心鸟瞰全局，'
             '再逐卷剖析其本质：真实背景、写作缘由、核心信息与今日应用。</p>'
             '<div class="hero-stats">'
             '<div><strong>66</strong>卷书</div>'
             '<div><strong>10</strong>大类别</div>'
             '<div><strong>1</strong>位基督</div>'
             '<div><strong>5</strong>个唯独</div>'
             '</div></div></header>')
    # intro
    p.append('<section class="sec" id="intro"><div class="wrap">')
    p.append(f'<h2 class="sec-title">{esc(HOME_INTRO["title"])}</h2>')
    p.append(f'<div class="sec-sub">{esc(HOME_INTRO["subtitle"])}</div><div class="rule"></div>')
    p.append(f'<div class="callout fade" style="margin-bottom:1.6rem">'
             f'<div class="prose">{esc(HOME_INTRO["lead"])}</div></div>')
    p.append('<div class="intro-grid">')
    for s in HOME_INTRO["sections"]:
        chips = "".join(f'<span class="chip">{esc(t)}</span>' for t in s["tags"])
        p.append(f'<div class="intro-card fade"><h3>{esc(s["h"])}</h3>'
                 f'<p>{esc(s["p"])}</p><div class="chips">{chips}</div></div>')
    p.append('</div></div></section>')
    # timeline
    p.append('<section class="sec" style="background:var(--parch2)"><div class="wrap-wide">')
    p.append('<h2 class="sec-title">救赎历史时间轴</h2>')
    p.append('<div class="sec-sub">从创造到新天新地——一条贯穿全书的救赎主线</div><div class="rule"></div>')
    p.append(f'<div class="figbox fade">{svg_timeline(TIMELINE)}'
             f'<div class="figcap">图：圣经救赎历史的十六个里程碑（约略年代）</div></div>')
    p.append('</div></section>')
    # books by category
    p.append('<section class="sec" id="books"><div class="wrap-wide">')
    p.append('<h2 class="sec-title">六十六卷 · 逐卷解读</h2>')
    p.append('<div class="sec-sub">点击任一书卷，进入从整体到局部的深度解读</div><div class="rule"></div>')
    for si, sec in enumerate(SECTIONS):
        secbooks = [b for b in BOOKS if b["_sec"] == si]
        p.append('<div class="catgroup fade">')
        p.append(f'<div class="cat-head">'
                 f'<div class="cat-badge" style="background:{sec["color"]}">{sec.get("icon","")}</div>'
                 f'<div><h3>{esc(sec["title"])}</h3>'
                 f'<div class="en">{esc(sec["subtitle"])}</div></div>'
                 f'<div class="cnt">{len(secbooks)} 卷</div></div>')
        p.append('<div class="book-grid">')
        for b in secbooks:
            p.append(f'<a class="bcard" href="{bookhref(b)}" style="--c:{b["_color"]}">'
                     f'<span class="bnum">{b["_num"]:02d}</span>'
                     f'<span class="bn">{esc(b["name"])}</span>'
                     f'<span class="be">{esc(b["eng"])} · {b["ch"]}章</span>'
                     f'<span class="bt">{esc(b["theme"])}</span></a>')
        p.append('</div></div>')
    p.append('</div></section>')
    return "".join(p)

# ---- 共享：书卷正文（hero + main）----
def book_body(b, href_home, href_prev, href_next):
    col = b["_color"]; grad = b["_gradient"]
    ex = EXTRA.get(b["eng"], {})
    p = []
    p.append(f'<header class="bhero" style="background:{grad}">'
             f'<div class="watermark">{esc(b["eng"])}</div>'
             f'<div class="bhero-in">'
             f'<div class="kicker">{b["_num"]:02d} / 66 · {esc(b["_sectitle"])}</div>'
             f'<h1>{esc(b["name"])}</h1>'
             f'<div class="en">{esc(b["eng"])}</div>'
             f'<div class="meta">'
             f'<span>✍ {esc(b["author"])}</span>'
             f'<span>📅 {esc(b["date"])}</span>'
             f'<span>📖 {b["ch"]} 章</span>'
             f'<span>🎯 {esc(b["theme"])}</span>'
             f'</div></div></header>')
    p.append('<main class="bmain">')
    p.append(f'<a class="backhome" href="{href_home}">← 返回目录</a>')
    p.append(f'<div class="verse-hero fade">{esc(b["verse"])}</div>')

    def block(idx, zh, en, inner):
        return (f'<section class="block fade"><div class="block-h">'
                f'<span class="idx" style="background:{col}">{idx}</span>'
                f'<h2>{esc(zh)}<span class="en">{esc(en)}</span></h2></div>{inner}</section>')

    ov = (f'<div class="callout"><div class="prose"><p>{esc(b["summary"])}</p></div></div>')
    p.append(block("★", "本卷核心", "The Heart of the Book", ov))

    rh = ex.get("rh", ""); cov = ex.get("covenant", "")
    inner = (f'<div class="figbox" style="margin-bottom:1rem">{svg_canonbar(b["_sec"])}'
             f'<div class="figcap">图：本卷在圣经全景中的位置（{esc(b["_sectitle"])}）</div></div>'
             f'<div class="prose"><p>{esc(rh)}</p></div>')
    if cov:
        inner += (f'<div class="minicard" style="margin-top:1rem;border-left:4px solid {col}">'
                  f'<h4><span class="dot" style="background:{col}"></span>盟约定位</h4>'
                  f'<div class="prose">{esc(cov)}</div></div>')
    p.append(block("壹", "整体视角 · 救赎历史中的定位", "Big Picture", inner))

    inner = (f'<div class="figbox" style="margin-bottom:1rem">{svg_outline_flow(b)}'
             f'<div class="figcap">图：{esc(b["name"])}结构脉络</div></div>')
    inner += '<ol class="outline-list">'
    for it in b["outline"]:
        inner += f'<li style="--c:{col}">{esc(it)}</li>'
    inner += '</ol>'
    p.append(block("贰", "局部视角 · 结构与脉络", "Structure & Outline", inner))

    why = ex.get("why", "")
    inner = (f'<div class="twocol">'
             f'<div class="minicard"><h4><span class="dot" style="background:{col}"></span>真实背景 · 情境</h4>'
             f'<div class="prose">{esc(b["bg"])}</div></div>'
             f'<div class="minicard"><h4><span class="dot" style="background:{col}"></span>为什么写</h4>'
             f'<div class="prose">{esc(why)}</div></div></div>')
    p.append(block("叁", "前因后果 · 背景与写作缘由", "Context & Purpose", inner))

    reformed = ex.get("reformed", []); christ = ex.get("christ", "")
    lis = "".join(f'<li>{esc(x)}</li>' for x in reformed)
    inner = (f'<div class="minicard" style="border-left:4px solid {col}">'
             f'<h4><span class="dot" style="background:{col}"></span>正统 · 改革宗神学要点</h4>'
             f'<ul class="ticks">{lis}</ul></div>')
    if christ:
        inner += (f'<div class="callout" style="margin-top:1rem;border-left-color:{col}">'
                  f'<h4 style="font-family:var(--serif);margin-bottom:.4rem;color:{col}">✝ 基督中心 · 预表与成全</h4>'
                  f'<div class="prose">{esc(christ)}</div></div>')
    p.append(block("肆", "神学核心 · 从改革宗看本卷", "Reformed Theology", inner))

    apply = ex.get("apply", [])
    lis = "".join(f'<li>{esc(x)}</li>' for x in apply)
    inner = (f'<div class="minicard" style="border-left:4px solid {col}">'
             f'<h4><span class="dot" style="background:{col}"></span>今日应用</h4>'
             f'<ul class="arrows ticks">{lis}</ul></div>')
    p.append(block("伍", "回应 · 今日的应用", "Application", inner))

    pv = (f'<a href="{href_prev[0]}"><div class="lbl">← 上一卷</div>'
          f'<div class="nm">{esc(href_prev[1])}</div></a>') if href_prev else '<a class="empty"></a>'
    nx = (f'<a class="next" href="{href_next[0]}"><div class="lbl">下一卷 →</div>'
          f'<div class="nm">{esc(href_next[1])}</div></a>') if href_next else '<a class="empty"></a>'
    p.append(f'<div class="pager">{pv}{nx}</div>')
    p.append('</main>')
    return "".join(p)

# ---- 多文件版：首页 ----
def build_index():
    p = [page_head("圣经六十六卷 · 改革宗正统神学解读", "assets/site.css")]
    p.append(topbar(""))
    p.append(home_body(lambda b: f'books/{b["_file"]}'))
    p.append(FOOTER)
    p.append(REVEAL_JS)
    p.append('</body></html>')
    return "".join(p)

# ---- 多文件版：书卷页 ----
def build_book(b):
    prev_b = BOOKS[b["_idx"]-1] if b["_idx"] > 0 else None
    next_b = BOOKS[b["_idx"]+1] if b["_idx"] < 65 else None
    hp = (prev_b["_file"], prev_b["name"]) if prev_b else None
    hn = (next_b["_file"], next_b["name"]) if next_b else None
    p = [page_head(f'{b["name"]} · 改革宗解读', "../assets/site.css")]
    p.append(topbar("../"))
    p.append(book_body(b, "../index.html", hp, hn))
    p.append(FOOTER)
    p.append(REVEAL_JS)
    p.append('</body></html>')
    return "".join(p)

# ─────────────────────────────────────────────
# 4b. 单文件版（Claude Artifact，body-only，哈希路由）
# ─────────────────────────────────────────────
BUNDLE_ROUTER = """
<script>
(function(){
  function show(hash){
    var id=(hash||'').replace('#','')||'home', scrollTo=null, view=id;
    if(id==='intro'||id==='books'){view='home';scrollTo=id;}
    var views=document.querySelectorAll('.view');
    for(var i=0;i<views.length;i++)views[i].classList.remove('active');
    var el=document.getElementById('view-'+view)||document.getElementById('view-home');
    el.classList.add('active');
    var f=el.querySelectorAll('.fade');for(var j=0;j<f.length;j++)f[j].classList.add('in');
    if(scrollTo){var t=document.getElementById(scrollTo);if(t)t.scrollIntoView({behavior:'auto'});}
    else window.scrollTo(0,0);
  }
  window.addEventListener('hashchange',function(){show(location.hash);});
  show(location.hash);
})();
</script>
"""

def bundle_topbar():
    return ('<div class="topbar"><div class="topbar-in">'
            '<a class="brand" href="#home">圣经六十六卷 · <span>改革宗解读</span></a>'
            '<nav class="topnav">'
            '<a href="#home">首页</a>'
            '<a href="#intro">整全导论</a>'
            '<a href="#books">书卷</a>'
            '</nav></div></div>')

def build_bundle():
    """返回 body-only 内容（含 <title>/<style>/<script>），用于 Artifact 发布。"""
    p = []
    p.append('<title>圣经六十六卷 · 改革宗正统神学解读</title>')
    p.append(f'<style>{CSS}</style>')
    p.append(bundle_topbar())
    # home view
    p.append('<div class="view active" id="view-home">')
    p.append(home_body(lambda b: f'#{b["_slug"]}'))
    p.append(FOOTER)
    p.append('</div>')
    # book views
    for b in BOOKS:
        prev_b = BOOKS[b["_idx"]-1] if b["_idx"] > 0 else None
        next_b = BOOKS[b["_idx"]+1] if b["_idx"] < 65 else None
        hp = (f'#{prev_b["_slug"]}', prev_b["name"]) if prev_b else None
        hn = (f'#{next_b["_slug"]}', next_b["name"]) if next_b else None
        p.append(f'<div class="view" id="view-{b["_slug"]}">')
        p.append(book_body(b, "#home", hp, hn))
        p.append(FOOTER)
        p.append('</div>')
    p.append(BUNDLE_ROUTER)
    return "".join(p)

# ─────────────────────────────────────────────
# 5. 写出
# ─────────────────────────────────────────────
def main():
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "books"), exist_ok=True)
    with open(os.path.join(ROOT, "assets", "site.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index())
    for b in BOOKS:
        with open(os.path.join(ROOT, "books", b["_file"]), "w", encoding="utf-8") as f:
            f.write(build_book(b))
    # 单文件版（用于 Artifact 部署）
    with open(os.path.join(ROOT, "bundle.html"), "w", encoding="utf-8") as f:
        f.write(build_bundle())
    missing = [b["eng"] for b in BOOKS if b["eng"] not in EXTRA]
    sz = os.path.getsize(os.path.join(ROOT, "bundle.html"))
    print(f"OK: index.html + {len(BOOKS)} book pages + assets/site.css")
    print(f"    bundle.html ({sz//1024} KB, single-file for Artifact)")
    print("missing EXTRA:", missing if missing else "none")

if __name__ == "__main__":
    main()
