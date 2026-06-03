# scripts — 构建工具

输出目录：**`../docs/`**（仓库里唯一会被当成网站发布的内容）。

```bash
# 在仓库根目录
python3 scripts/build_site.py
```

| 文件 | 作用 |
|------|------|
| `routes_data.py` | 22 条路线文案（数据源） |
| `build_site.py` | 生成 `docs/data/routes.json`、`docs/assets/js/routes-data.js`，更新 `docs/travel.html` |
