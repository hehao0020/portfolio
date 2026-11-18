"""Wire the seven PRD pages into the portfolio and add the version evidence."""

from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = [
    ("note-studio", "小红书笔记工作台", "从一键拆卡到三档排版", "最新 v1.4.9"),
    ("mailbox", "毕业季留言墙", "从个人信箱到公开广场", "已上线 · 2000+ 用户"),
    ("word-check", "小红书查词网站", "从自己查词到团队使用", "团队日常使用"),
    ("yueliu", "阅流公众号创作台", "从写作经验到创作流程", "两个月涨粉 1500"),
    ("voice", "张嘴就记", "把四类记录收进一句话", "微信小程序已上线"),
    ("buy", "买前听劝", "从公开投票转向个人自检", "本地版本"),
    ("practice", "增长与 AI 工作流", "从一线问题到复用方法", "业务实践"),
]


def card(item, duplicate=False):
    slug, name, idea, state = item
    tabindex = ' tabindex="-1"' if duplicate else ""
    return (f'<a class="prd-rail-card" href="prd/{slug}.html"{tabindex}>'
            f'<span class="rail-overline">PRODUCT NOTE / {PROJECTS.index(item)+1:02d}</span>'
            f'<strong>{escape(name)}</strong><span class="rail-idea">{escape(idea)}</span>'
            f'<span class="rail-state">{escape(state)}</span><span class="rail-link">阅读完整 PRD ↗</span></a>')


index = ROOT / "index.html"
text = index.read_text(encoding="utf-8")
if 'prd-shelf.css' not in text:
    text = text.replace('<link rel="stylesheet" href="site-polish.css">', '<link rel="stylesheet" href="site-polish.css"><link rel="stylesheet" href="prd-shelf.css">', 1)
if 'id="prd-showcase"' not in text:
    group = ''.join(card(item) for item in PROJECTS)
    duplicate = ''.join(card(item, True) for item in PROJECTS)
    shelf = (f'<section class="home-prd-showcase" id="prd-showcase" aria-label="项目 PRD 展示">'
             f'<div class="prd-shelf-head"><span class="rail-kicker">THE THINKING BEHIND THE WORK</span>'
             f'<h2>每个项目，<em>都有一份完整的思考记录。</em></h2>'
             f'<p>从最初的想法到版本取舍。展示会自动滚动，鼠标停留即可暂停，点击卡片阅读完整 PRD。</p></div>'
             f'<div class="prd-rail-window"><div class="prd-rail-track">'
             f'<div class="prd-rail-group">{group}</div>'
             f'<div class="prd-rail-group" aria-hidden="true">{duplicate}</div>'
             f'</div></div></section>')
    text = text.replace('<section class="home-projects"', shelf + '<section class="home-projects"', 1)
text = text.replace('01 / 桌面工具 · Windows · v1.4.3', '01 / 桌面工具 · Windows · 最新 v1.4.9')
index.write_text(text, encoding="utf-8")

for slug, *_ in PROJECTS:
    path = ROOT / "projects" / f"{slug}.html"
    text = path.read_text(encoding="utf-8")
    if 'prd-shelf.css' not in text:
        text = text.replace('<link rel="stylesheet" href="../site-polish.css">', '<link rel="stylesheet" href="../site-polish.css"><link rel="stylesheet" href="../prd-shelf.css">', 1)
    if 'class="case-prd-link"' not in text:
        cta = (f'<div class="case-prd-cta"><span>想看这件事怎么从想法变成产品？</span>'
               f'<a class="case-prd-link" href="../prd/{slug}.html">阅读完整 PRD · 需求、取舍与迭代 <span aria-hidden="true">↗</span></a></div>')
        text = text.replace('<div class="story-layout">', cta + '<div class="story-layout">', 1)
    if slug == 'note-studio':
        text = text.replace('Windows 桌面工具 · v1.4.3', 'Windows 桌面工具 · 最新 v1.4.9', 1)
        text = text.replace('v1.4.3 当前界面 · 点击下方录屏看实际操作', 'v1.4.3 界面实拍 · 当前项目已迭代至 v1.4.9', 1)
        if 'note-version-list.png' not in text:
            figure = ('<div class="version-evidence"><div><span>VERSION EVIDENCE</span><h3>从 v0.1.0 到 v1.4.7，版本文件留下了迭代的轨迹</h3>'
                      '<p>这张图记录了便携版的多轮发布。截图止于 v1.4.7；本机项目 README 还记录了 v1.4.8 的导出与排序修复，以及当前 v1.4.9 的位置锁定、文字控制和纸张底板。每一步都在处理真实使用中遇到的问题。</p></div>'
                      '<figure class="shot"><button type="button" class="shot-open" data-image="../assets/note-version-list.png" data-caption="笔记工作台便携版版本文件记录：v0.1.0 至 v1.4.7" aria-label="放大查看笔记工作台版本文件记录">'
                      '<img src="../assets/note-version-list.png" alt="笔记工作台便携版从 v0.1.0 到 v1.4.7 的版本记录" width="1170" height="1710" loading="lazy"></button>'
                      '<figcaption>真实版本记录 · 点击放大查看</figcaption></figure></div>')
            text = text.replace('<section class="story-section" id=result>', figure + '<section class="story-section" id=result>', 1)
        text = text.replace('<h2>当前产品能力</h2><p>Windows v1.4.3', '<h2>当前产品能力</h2><p>Windows 当前 v1.4.9', 1)
        text = text.replace('支持项目备份、导入和导出前检查；暂无可核实的用户规模或节省工时数据。', '当前版本已加入整篇总览、页面排序、跨页移动、工程文件、位置锁定和更细的文字控制。', 1)
    path.write_text(text, encoding="utf-8")

readme = ROOT / 'README.md'
text = readme.read_text(encoding='utf-8')
text = text.replace('v0.8 至 v1.4.3 的版本截图', 'v0.8 至 v1.4.3 的界面截图，以及 v0.1.0 至 v1.4.7 的版本文件记录；当前产品记录为 v1.4.9')
if '## PRD' not in text:
    text += '\n## PRD\n\n首页新增自动滚动的 PRD 展示。`prd/*.md` 是七个项目的需求与迭代记录，`prd/*.html` 是面向 HR 的阅读页；运行 `python tools/build_prd.py` 可从 Markdown 重新生成页面。页面支持点击查看完整 PRD，滚动展示在鼠标停留、键盘聚焦和减少动态效果设置下暂停。\n'
readme.write_text(text, encoding='utf-8')
