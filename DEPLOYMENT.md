# Cloudflare 部署

项目仍为原纯静态网页，Python 3 构建不依赖第三方 Python 包。`theme.css` 与原有 JavaScript 不变。

## 构建

```sh
npm ci
npm run build
```

也可直接执行 `python3 build.py`。每日行程从 `itinerary-content-verified.md` 的“每日行程”章节生成；修改后必须重新构建。

- `index.html`：原文件夹版入口。
- `offline.html`：保留的离线单文件版，不进入部署目录。
- `dist/`：唯一部署目录，仅含网站入口和实际引用的本地资源。样式、交互及原地图仍内嵌于入口中。
- `page-template.html`：原页面模板，每日行程位置使用构建占位符；需运行构建后查看 `index.html`。

## Workers（对应本次报错）

`wrangler.toml` 已指定 `[assets] directory = "./dist"`，`[build] command = "python3 build.py"`。

```sh
npm run deploy:check
npm run deploy
```

Cloudflare Git 构建设置：根目录选择本项目目录，构建命令 `npm run build`，部署命令 `npm run deploy`。不要在 Dashboard 命令中继续保留 `--assets .`、`--assets /opt/buildhome/repo` 等覆盖参数。

`name = "balkan-travel"` 来自当前项目名。若现有 Cloudflare Worker 名称不同，应改为该现有名称；本压缩包未包含账户、项目绑定或原 Dashboard 设置。

## Pages（备选，不与 Workers 配置混用）

Pages Git 集成：构建命令 `npm run build`，输出目录 `dist`。

CLI 方式使用独立的 `wrangler.pages.toml`，其中 `pages_build_output_dir = "./dist"`：

```sh
npm run deploy:pages
```

使用现有 Pages 项目时，配置中的 name 应与现有项目名称一致。

## 本次验证结果

- 已运行标准构建和 Workers dry-run；静态目录明确为 `dist/`，没有 `.git`、依赖、开发文档或缓存。
- 已执行真实 Workers 部署命令；构建成功后因缺少 `CLOUDFLARE_API_TOKEN` 而退出，未发布线上。
- 在已登录 Cloudflare 的本地终端或已有授权的 CI 环境运行 `npm run deploy` 完成发布。无需删除 Git 历史或 pack 文件。

配置依据：[Cloudflare Static Assets](https://developers.cloudflare.com/workers/static-assets/) 与 [Wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)。
