# 巴尔干旅行网页

直接打开 index.html 查看网页。每日行程共12天、77项安排，使用预计时长；点击“＋”展开简介、图片与地图入口。

21段景点简介均配有图片，其中9张为外部图片，须联网加载；其他图片内嵌在网页。外部图片无法加载时，可点击图片来源查看原图。地图链接需联网。

## 修改和生成

- page-data.json：days[].timeline 内编辑 title、activity、duration_label、duration_text、intro、place_ids；closing_note 为每日结束语。
- places：地点信息与地图链接；point_media_manifest：图片来源。
- page-template.html：整体页面布局、航班、住宿、租车和清单。
- assets：本地图片。

运行 `python render.py` 重新生成 index.html，仅依赖Python标准库。

租车金额及付款状态沿用已确认内容；每日安排未改动航班、住宿、租车或清单栏目。
