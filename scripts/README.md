# scripts — 构建工具（会进 Git，不会作为网页发布）

| 文件 | 作用 |
|------|------|
| `routes_data.py` | 22 条路线文案（**唯一数据源**） |
| `build_site.py` | 生成 `docs/` 下的 JSON、JS，并更新 `travel.html` 卡片 |
| `generate_routes.py` | 同 `build_site.py` 的入口别名 |
| `sync_route_images.py` | 可选：同步路线图片 |
| `redownload_images.py` | 可选：从 Wikimedia 重新下载图片 |

```bash
# 在仓库根目录执行
python3 scripts/build_site.py
```

输出目录：仓库根目录（`index.html`、`assets/`、`data/` 等，见根 README）。
