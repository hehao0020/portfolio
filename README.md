# 何圣荣 AI 产品经理作品集

在线地址：https://hehao0020.github.io/portfolio/

静态 HTML 作品集。首页是项目总览，左侧目录可进入七个独立案例页：小红书笔记工作台、毕业季留言墙、小红书查词网站、阅流、张嘴就记、买前听劝，以及增长与 AI 工作流。

项目页展示需求来源、关键设计、版本演进、真实截图和结果边界。笔记工作台保留早期界面及 v0.8 至 v1.4.3 的界面截图，以及 v0.1.0 至 v1.4.7 的版本文件记录；当前产品记录为 v1.4.9；留言墙使用实机截图。简历为 `resume.pdf`。

部署在 GitHub Pages。打开 `index.html` 可本地查看，无需安装依赖或构建。源码结构：`index.html`、`projects/`、`assets/`、`site.css`、`site.js`。

## PRD

首页新增自动滚动的 PRD 展示。`prd/*.md` 是七个项目的需求与迭代记录，`prd/*.html` 是面向 HR 的阅读页；运行 `python tools/build_prd.py` 可从 Markdown 重新生成页面。页面支持点击查看完整 PRD，滚动展示在鼠标停留、键盘聚焦和减少动态效果设置下暂停。
