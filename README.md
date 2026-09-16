# 巴尔干旅行网页

直接打开 index.html；照片已内嵌，无需联网加载。地图和地点照片链接需要联网。

修改每日安排：编辑 page-data.json 的 days[].timeline（time、title、activity、place_ids）；点位简介位于 places，照片位于 assets。

运行 `python render.py` 重新生成 index.html（仅使用Python标准库）。page-template.html 保存整体布局、航班、住宿及清单；修改这些栏目时请同步模板和数据。

每日时间为用户提供的计划。还车卡显示10月3日07:30–08:00行程安排，原订单时间保留在数据中，不表示车行已修改订单。

18处点位有内嵌实景图；其余点位提供地图照片入口。图片来源与许可见卡片及point-media-manifest.json。
