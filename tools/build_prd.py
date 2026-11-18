"""Build readable static PRD pages from the Markdown kept in this repository."""

from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PRD = ROOT / "prd"
NAMES = {
    "note-studio": ("01", "小红书笔记工作台", "从文字到图卡，把效率与控制权放进同一条工作流"),
    "mailbox": ("02", "毕业季留言墙", "让毕业前想说的话有一个轻而安全的入口"),
    "word-check": ("03", "小红书查词网站", "把发稿前反复查词的动作变成顺手的检查流程"),
    "yueliu": ("04", "阅流公众号创作台", "把公众号写作、审稿与排版经验收进工具"),
    "voice": ("05", "张嘴就记", "一句话记下生活里零碎但重要的事"),
    "buy": ("06", "买前听劝", "在付款前给自己一次看清理由的机会"),
    "practice": ("07", "增长与 AI 工作流", "从运营现场提炼能重复使用的方法"),
}


def inline(text: str) -> str:
    value = escape(text)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"`(.+?)`", r"<code>\1</code>", value)
    return value


def render(markdown: str):
    blocks = []
    toc = []
    section_open = False
    paragraph = []
    items = []

    def flush():
        if paragraph:
            blocks.append("<p>" + inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()
        if items:
            blocks.append("<ul>" + "".join("<li>" + inline(item) + "</li>" for item in items) + "</ul>")
            items.clear()

    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            flush()
        elif line.startswith("# "):
            flush()
        elif line.startswith("## "):
            flush()
            if section_open:
                blocks.append("</section>")
            title = line[3:]
            anchor = f"section-{len(toc) + 1}"
            toc.append((anchor, title))
            blocks.append(f'<section class="prd-section" id="{anchor}"><h2><span>{len(toc):02d}</span>{inline(title)}</h2>')
            section_open = True
        elif line.startswith("### "):
            flush()
            blocks.append("<h3>" + inline(line[4:]) + "</h3>")
        elif line.startswith("> "):
            flush()
            blocks.append('<p class="prd-lede">' + inline(line[2:]) + "</p>")
        elif line.startswith("- "):
            if paragraph:
                flush()
            items.append(line[2:])
        elif match := re.fullmatch(r"!\[(.+?)\]\((.+?)\)", line):
            flush()
            alt, src = match.groups()
            blocks.append(f'<figure class="prd-figure"><img src="{escape(src, quote=True)}" alt="{escape(alt, quote=True)}" loading="lazy"><figcaption>{inline(alt)}</figcaption></figure>')
        else:
            if items:
                flush()
            paragraph.append(line)
    flush()
    if section_open:
        blocks.append("</section>")
    return "".join(blocks), toc


for slug, (number, name, subtitle) in NAMES.items():
    body, toc = render((PRD / f"{slug}.md").read_text(encoding="utf-8"))
    nav = "".join(f'<a href="#{anchor}"><span>{i:02d}</span>{inline(title)}</a>' for i, (anchor, title) in enumerate(toc, 1))
    page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#071218"><meta name="description" content="{escape(name, quote=True)}的完整产品需求与迭代记录">
<title>{escape(name)} · PRD｜何圣荣作品集</title><link rel="stylesheet" href="../prd.css"></head>
<body><div class="reading-progress" aria-hidden="true"></div><a class="skip" href="#content">跳到正文</a>
<header class="topbar"><a class="brand" href="../index.html"><b>何</b><span>何圣荣 <small>/ 产品作品集</small></span></a><nav><a href="../projects/{slug}.html">项目案例</a><a href="../index.html#projects">全部项目</a></nav></header>
<main id="content"><div class="hero"><div class="eyebrow">PRODUCT REQUIREMENTS · {number} / 07</div><p class="hero-kind">项目需求与迭代记录</p><h1>{escape(name)}</h1><p class="hero-sub">{escape(subtitle)}</p><div class="hero-actions"><a href="../projects/{slug}.html">返回项目案例 ↗</a><span>向下阅读完整 PRD</span></div></div>
<div class="reading-layout"><article class="document">{body}<div class="endnote">写下需求，也写下后来改变主意的原因。产品记录会随实际版本更新。</div></article>
<aside class="chapter-nav" aria-label="文档章节"><div class="chapter-head">本页目录 <span>PRD / {number}</span></div>{nav}</aside></div></main>
<footer><a href="../index.html">何圣荣 · AI 产品经理作品集</a><span>从真实问题到可用产品</span></footer>
<script src="../prd.js" defer></script></body></html>'''
    (PRD / f"{slug}.html").write_text(page, encoding="utf-8")
    print(f"built {slug}: {len(toc)} sections")
