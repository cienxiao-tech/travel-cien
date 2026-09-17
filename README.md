# 巴尔干山海之旅 · 12.3视觉升级

解压后打开 index.html。请保持 assets 文件夹与 index.html 相邻。

- index.html：完整可直接打开的网页，样式已内嵌。
- page-template.html：可编辑模板，引用 theme.css。
- theme.css：唯一全站设计系统；按组件组织，不叠加历史 patch。
- assets/cover/cover-hero.jpg：原版皮瓦湖封面，未修改。
- build.py：编辑模板或样式后，运行 python build.py 更新 index.html。
- review/：修改前后审计、全标题计算样式记录、内容保护验证和手机/桌面截图。

保留全部旅行正文、业务链接、图片地址与原有 JavaScript。底部导航按本次要求改为五项，航班/总览/租车/行装入口在“更多”。

部分原有照片为联网资源，当前测试环境中9张外链照片加载失败，详见 review/02-修改后审计.md。清单与备忘继续保存在当前浏览器；请在原来的访问地址使用更新页面以延续原有 localStorage 数据。
