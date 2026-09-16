# 巴尔干旅行计划

打开 index.html 浏览，地图和图片已内嵌。

- page-data.json：页面资料。
- travel-data.json：完整旅行资料。
- travel-routes.json：每日路线与分时安排。
- maps/overall.svg：可编辑矢量地图；PNG为图片导出。

网页展示完整旅行计划，不设置修改日志。修改JSON需同步更新静态HTML和地图。勾选和备忘仅保存在当前浏览器。尚未发布公网链接。

地图采用 Natural Earth 1:10m 国界、水系及 OSRM 基于 OpenStreetMap 计算的道路线路；计算路线不含实时交通、口岸排队或未来封路信息。maps/road-routes.geojson 保存地图线路。
