# 巴尔干旅行网页 11.6

以用户上传的11.5版为基础，删除点位详情中的“地点照片”链接，保留景点图片及地图定位。依据皮瓦湖封面统一湖绿色和云雾灰，优化桌面双栏封面、移动端排版、航班和每日行程层级。

- index.html：可直接打开的完整网页，封面位于 assets/cover。
- page-template.html：完整可编辑页面，引用 theme.css，无需数据文件或构建框架。
- theme.css：11.6版样式，按栏目组织。
- build.py：修改模板或样式后运行 python build.py 更新 index.html。

保留日期切换、+展开、地图放大、清单与备忘本地保存。
设计参考：https://github.com/Leonxlnx/taste-skill/blob/main/skills/redesign-skill/SKILL.md

底部目录调整：固定贴底、细分隔线、四项纯文字，57px高度加设备安全区；正文预留同高再加24px间距，手机封面图片自适应可用屏高。导航文字、链接及全部脚本保持原样。
