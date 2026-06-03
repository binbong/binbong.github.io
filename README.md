# binbong.github.io

个人站点「车行天下」— 静态 HTML，托管于 GitHub Pages（tahoo.me）。

## 结构

| 文件 | 作用 |
|------|------|
| `scripts/routes_data.py` | 22 条路线文案（唯一数据源） |
| `scripts/build_site.py` | 生成 `data/routes.json`，更新 `travel.html` 卡片链接 |
| `route.html` + `route.js` | **唯一**攻略详情页，URL：`route.html?slug=chuanzang` |
| `images/routes/{slug}/` | 各路线图片 |

不再为每条路线单独生成 `routes/*.html`。

## 改内容后构建

```bash
python3 scripts/build_site.py
```

## 本地预览

**方式 A（推荐）**：双击 `本地预览.command`，或在终端执行：

```bash
./serve.sh
```

浏览器会自动打开路线列表。若 8765 被占用，脚本会自动换端口（看终端里打印的地址）。

**方式 B（无需服务器）**：在 Finder 中双击 `travel.html` 打开列表；详情页双击 `route.html` 需带参数，建议仍用方式 A。

**注意**：不要用 `http://localhost:8080`。本机 8080 常被 Spring Boot 占用，会出现 Whitelabel 404。
